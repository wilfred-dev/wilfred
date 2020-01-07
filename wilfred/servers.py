# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

import click
import docker

from tabulate import tabulate
from pathlib import Path
from shutil import rmtree
from os import remove as remove_file

from wilfred.message_handler import error
from wilfred.keyboard import KeyboardThread
from wilfred.container_variables import ContainerVariables


class Servers(object):
    def __init__(self, database, docker_client, configuration, images):
        self._database = database
        self._images = images
        self._configuration = configuration
        self._docker_client = docker_client

        self._get_db_servers()

    def pretty(self, server=None):
        self._running_docker_sync()

        headers = {
            "id": "ID",
            "name": "Name",
            "image_uid": "Image UID",
            "memory": "Memory (RAM)",
            "port": "Port",
            "status": "Status",
        }

        return tabulate(
            [server] if server else self._servers,
            headers=headers,
            tablefmt="fancy_grid",
        )

    def set_status(self, server, status):
        self._database.query(
            f"UPDATE servers SET status = '{status}' WHERE id = '{server['id']}'"
        )
        self._get_db_servers()

    def sync(self, db_update=False):
        if db_update:
            self._get_db_servers()

        with click.progressbar(
            self._servers, label="Syncing servers", length=len(self._servers)
        ) as servers:
            for server in servers:
                start = False
                if server["status"] == "created":
                    self._install(server)
                    self.set_status(server, "running")
                    start = True

                # stopped
                if server["status"] == "stopped":
                    self._stop(server)

                # start
                if server["status"] == "running" or start:
                    try:
                        self._docker_client.containers.get(f"wilfred_{server['id']}")
                    except docker.errors.NotFound:
                        self._start(server)

    def get_by_name(self, name):
        self._get_db_servers()

        server = list(filter(lambda x: x["name"] == name, self._servers))

        return server[0] if server else None

    def remove(self, server):
        path = f"{self._configuration['data_path']}/{server['id']}"

        self._database.query(f"DELETE FROM servers WHERE id='{server['id']}'")
        self._database.query(f"DELETE FROM variables WHERE server_id='{server['id']}'")

        try:
            container = self._docker_client.containers.get(f"wilfred_{server['id']}")
            container.stop()
        except docker.errors.NotFound:
            pass

        rmtree(path, ignore_errors=True)

    def console(self, server):
        try:
            container = self._docker_client.containers.get(f"wilfred_{server['id']}")
        except docker.errors.NotFound:
            error("server is not running", exit_code=1)

        KeyboardThread(self._console_input_callback, params=server)

        for line in container.logs(stream=True, tail=200):
            click.echo(line.strip())

    def _console_input_callback(self, payload, server):
        self._command(server, payload)

    def _command(self, server, command):
        try:
            container = self._docker_client.containers.get(f"wilfred_{server['id']}")
        except docker.errors.NotFound:
            error("server is not running", exit_code=1)

        try:
            s = container.attach_socket(params={"stdin": 1, "stream": 1})
            s._sock.send(f"{command}\n".encode("utf-8"))
            s.close()
        except Exception as e:
            error(
                f"unable to send command '{command}' on server {server['id']}, err {click.style(str(e), bold=True)}",
                exit_code=1,
            )

    def _get_db_servers(self):
        self._servers = self._database.query("SELECT * FROM servers")

    def _running_docker_sync(self):
        for server in self._servers:
            try:
                self._docker_client.containers.get(f"wilfred_{server['id']}")
            except docker.errors.NotFound:
                self.set_status(server, "stopped")

        self._get_db_servers()

    def _parse_startup_command(self, cmd, server, image):
        return ContainerVariables(server, image, self._database).parse_startup_command(
            cmd.replace("{{SERVER_MEMORY}}", str(server["memory"])).replace(
                "{{SERVER_PORT}}", str(server["port"])
            )
        )

    def _install(self, server):
        path = f"{self._configuration['data_path']}/{server['id']}"
        image = self._images.get_image(server["image_uid"])

        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            error(
                f"unable to create server data directory, {click.style(str(e), bold=True)}",
                exit_code=1,
            )

        with open(f"{path}/install.sh", "w") as f:
            f.write("cd /server\n" + "\n".join(image["installation"]["script"]))

        try:
            self._docker_client.containers.run(
                image["installation"]["docker_image"],
                f"{image['installation']['shell']} /server/install.sh",
                volumes={path: {"bind": "/server", "mode": "rw"}},
                name=f"wilfred_{server['id']}",
                environment=ContainerVariables(
                    server, image, self._database, install=True
                ).get_env_vars(),
                remove=True,
            )
        except Exception as e:
            self._database.query(f"DELETE FROM servers WHERE id='{server['id']}'")
            error(
                f"unable to create installation Docker container, server removed {click.style(str(e), bold=True)}",
                exit_code=1,
            )

        remove_file(f"{path}/install.sh")

    def _start(self, server):
        path = f"{self._configuration['data_path']}/{server['id']}"
        image = self._images.get_image(server["image_uid"])

        try:
            self._docker_client.containers.run(
                image["docker_image"],
                f"{self._parse_startup_command(image['command'], server, image)}",
                volumes={path: {"bind": "/server", "mode": "rw"}},
                name=f"wilfred_{server['id']}",
                remove=True,
                ports={f"{server['port']}/tcp": server["port"]},
                detach=True,
                working_dir="/server",
                mem_limit=f"{server['memory']}m",
                oom_kill_disable=True,
                stdin_open=True,
                environment=ContainerVariables(
                    server, image, self._database
                ).get_env_vars(),
            )
        except Exception as e:
            error(
                f"unable to start Docker container {click.style(str(e), bold=True)}",
                exit_code=1,
            )

    def kill(self, server):
        try:
            container = self._docker_client.containers.get(f"wilfred_{server['id']}")
        except docker.errors.NotFound:
            return

        container.kill()

    def _stop(self, server):
        image = self._images.get_image(server["image_uid"])

        try:
            container = self._docker_client.containers.get(f"wilfred_{server['id']}")
        except docker.errors.NotFound:
            return

        if not image["stop_command"]:
            try:
                container.stop()
            except Exception as e:
                exit(
                    f"could not stop container {click.style(str(e), bold=True)}",
                    exit_code=1,
                )

            return

        self._command(server, image["stop_command"])

        stopped = False

        while not stopped:
            try:
                self._docker_client.containers.get(f"wilfred_{server['id']}")
            except docker.errors.NotFound:
                stopped = True
