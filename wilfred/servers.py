# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import click
import docker

from tabulate import tabulate
from pathlib import Path
from shutil import rmtree
from subprocess import call

from wilfred.core import random_string
from wilfred.message_handler import error


class Servers(object):
    def __init__(self, database, docker_client, configuration, images):
        self._database = database
        self._images = images
        self._configuration = configuration
        self._docker_client = docker_client

        self._get_db_servers()

    def create(self, name, image_uuid, memory, port):
        self._database.query(
            " ".join(
                (
                    "INSERT INTO servers",
                    "(id, name, image_uuid, memory, port, status)"
                    f"VALUES ('{random_string()}', '{name}', '{image_uuid}', '{memory}', '{port}', 'created')",
                )
            )
        )

        self._get_db_servers()
        self.sync()

    def pretty(self):
        self._running_docker_sync()

        headers = {
            "id": "ID",
            "name": "Name",
            "image_uuid": "Image UUID",
            "memory": "Memory (RAM)",
            "port": "Port",
            "status": "Status",
        }

        return tabulate(self._servers, headers=headers, tablefmt="fancy_grid")

    def set_status(self, server, status):
        self._database.query(
            f"UPDATE servers SET status = '{status}' WHERE id = '{server['id']}'"
        )
        self._get_db_servers()

    def sync(self):
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
                    self._kill(server)

                # start
                if server["status"] == "running" or start:
                    try:
                        self._docker_client.containers.get(server["id"])
                    except docker.errors.NotFound:
                        self._start(server)

    def get_by_name(self, name):
        self._get_db_servers()

        return list(filter(lambda x: x["name"] == name, self._servers))

    def remove(self, server):
        path = f"{self._configuration['data_path']}/{server['id']}"

        self._database.query(f"DELETE FROM servers WHERE id='{server['id']}'")

        try:
            container = self._docker_client.containers.get(server["id"])
            container.stop()
        except docker.errors.NotFound:
            pass

        rmtree(path, ignore_errors=True)

    def console(self, server):
        try:
            container = self._docker_client.containers.get(server["id"])
        except docker.errors.NotFound:
            error("server is not running", exit_code=1)

        click.echo(container.logs())
        call(["docker", "attach", server["id"], "--detach-keys", "ctrl-c"])

    def command(self, server, command):
        try:
            self._docker_client.containers.get(server["id"])
        except docker.errors.NotFound:
            error("server is not running", exit_code=1)

    def _get_db_servers(self):
        self._servers = self._database.query("SELECT * FROM servers")

    def _running_docker_sync(self):
        for server in self._servers:
            try:
                self._docker_client.containers.get(server["id"])
            except docker.errors.NotFound:
                self.set_status(server, "stopped")

        self._get_db_servers()

    def _parse_cmd(self, cmd, server):
        return cmd.replace("{{SERVER_MEMORY}}", f"{server['memory']}").replace(
            "{{SERVER_PORT}}", f"{server['port']}"
        )

    def _install(self, server):
        path = f"{self._configuration['data_path']}/{server['id']}"
        image = self._images.get_image(server["image_uuid"])[0]

        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            error(
                f"unable to create server data directory, {click.style(str(e), bold=True)}",
                exit_code=1,
            )

        with open(f"{path}/install.sh", "w") as f:
            f.write("cd /server\n" + "\n".join(image["installation"]["script"]))

        self._docker_client.containers.run(
            image["installation"]["docker_image"],
            f"{image['installation']['shell']} /server/install.sh",
            volumes={path: {"bind": "/server", "mode": "rw"}},
            name=server["id"],
            remove=True,
        )

    def _start(self, server):
        path = f"{self._configuration['data_path']}/{server['id']}"
        image = self._images.get_image(server["image_uuid"])[0]

        self._docker_client.containers.run(
            image["docker_image"],
            f"{self._parse_cmd(image['command'], server)}",
            volumes={path: {"bind": "/server", "mode": "rw"}},
            name=server["id"],
            remove=True,
            ports={f"{server['port']}/tcp": server["port"]},
            detach=True,
            working_dir="/server",
            mem_limit=f"{server['memory']}m",
            oom_kill_disable=True,
            stdin_open=True,
        )

    def _kill(self, server):
        try:
            container = self._docker_client.containers.get(server["id"])
        except docker.errors.NotFound:
            return

        container.stop()
