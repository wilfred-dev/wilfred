# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

import click
import docker

from tabulate import tabulate
from pathlib import Path
from shutil import rmtree, get_terminal_size
from os import remove as remove_file
from time import sleep

from wilfred.database import session, Server, EnvironmentVariable
from wilfred.message_handler import error
from wilfred.keyboard import KeyboardThread
from wilfred.container_variables import ContainerVariables


class Servers(object):
    def __init__(self, docker_client, configuration, images):
        self._images = images
        self._configuration = configuration
        self._docker_client = docker_client

    def pretty(self, server=None):
        self._running_docker_sync()

        servers = (
            [
                dict(
                    (col, getattr(server, col))
                    for col in server.__table__.columns.keys()
                )
            ]
            if server
            else [u.__dict__ for u in session.query(Server).all()]
        )

        for server in servers:
            try:
                del server["_sa_instance_state"]
            except Exception:
                pass

            server.update(
                (
                    k,
                    str(v)
                    .replace("running", click.style("running", fg="green"))
                    .replace("stopped", click.style("stopped", fg="red"))
                    .replace("installing", click.style("installing", fg="yellow")),
                )
                for k, v in server.items()
            )

            _term_diff = get_terminal_size((80, 20))[0] - 75

            if len(str(server["custom_startup"])) > _term_diff:
                server.update(
                    {
                        "custom_startup": f"{str(server['custom_startup'])[:_term_diff]}..."
                    }
                )

        headers = {
            "id": click.style("ID", bold=True),
            "name": click.style("Name", bold=True),
            "image_uid": click.style("Image UID", bold=True),
            "memory": click.style("RAM", bold=True),
            "port": click.style("Port", bold=True),
            "status": click.style("Status", bold=True),
            "custom_startup": click.style("Custom startup", bold=True),
        }

        return tabulate(
            servers,
            headers=headers,
            tablefmt="plain" if get_terminal_size((80, 20))[0] < 96 else "fancy_grid",
        )

    def set_status(self, server, status):
        server.status = status
        session.commit()

    def sync(self):
        with click.progressbar(
            session.query(Server).all(),
            label="Syncing servers",
            length=len(session.query(Server).all()),
        ) as servers:
            for server in servers:
                if server.status == "installing":
                    try:
                        self._docker_client.containers.get(f"wilfred_{server.id}")
                    except docker.errors.NotFound:
                        self.set_status(server, "stopped")

                # stopped
                if server.status == "stopped":
                    self._stop(server)

                # start
                if server.status == "running":
                    try:
                        self._docker_client.containers.get(f"wilfred_{server.id}")
                    except docker.errors.NotFound:
                        self._start(server)

    def remove(self, server):
        path = f"{self._configuration['data_path']}/{server.id}"

        session.delete(
            session.query(EnvironmentVariable).filter_by(server_id=server.id).first()
        )
        session.delete(server)
        session.commit()

        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
            container.stop()
        except docker.errors.NotFound:
            pass

        rmtree(path, ignore_errors=True)

    def console(self, server, disable_user_input=False):
        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            error("server is not running", exit_code=1)

        if not disable_user_input:
            KeyboardThread(self._console_input_callback, params=server)

        for line in container.logs(stream=True, tail=200):
            click.echo(line.strip())

    def install(self, server, skip_wait=False, spinner=None):
        path = f"{self._configuration['data_path']}/{server.id}"
        image = self._images.get_image(server.image_uid)

        try:
            Path(path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            error(
                f"unable to create server data directory, {click.style(str(e), bold=True)}",
                exit_code=1,
            )

        with open(f"{path}/install.sh", "w") as f:
            f.write("cd /server\n" + "\n".join(image["installation"]["script"]))

        if spinner:
            spinner.write(
                "> Pulling Docker image and creating installation container, do not exit"
            )

        try:
            self._docker_client.containers.run(
                image["installation"]["docker_image"],
                f"{image['installation']['shell']} /server/install.sh",
                volumes={path: {"bind": "/server", "mode": "rw"}},
                name=f"wilfred_{server.id}",
                environment=ContainerVariables(
                    server, image, install=True
                ).get_env_vars(),
                remove=True,
                detach=True,
            )
        except Exception as e:
            session.delete(server)
            session.commit()
            error(
                f"unable to create installation Docker container, server removed {click.style(str(e), bold=True)}",
                exit_code=1,
            )

        if skip_wait and spinner:
            spinner.write(
                "> Installation will continue in background, use `wilfred servers` to see if process has finished."
            )

        if not skip_wait:
            if spinner:
                spinner.write(
                    "> You can safely press CTRL+C, the installation will continue in the background."
                )
                spinner.write(
                    "> Run `wilfred servers` too see when the status changes from `installing` to `stopped`."
                )
                spinner.write(
                    f"> You can also follow the installation log using `wilfred console {server.name}`"
                )
            while self._container_alive(server):
                sleep(1)

    def kill(self, server):
        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            return

        container.kill()

    def _console_input_callback(self, payload, server):
        self.command(server, payload)

    def command(self, server, command):
        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            error("server is not running", exit_code=1)

        try:
            s = container.attach_socket(params={"stdin": 1, "stream": 1})
            s._sock.send(f"{command}\n".encode("utf-8"))
            s.close()
        except Exception as e:
            error(
                f"unable to send command '{command}' on server {server.id}, err {click.style(str(e), bold=True)}",
                exit_code=1,
            )

    def _running_docker_sync(self):
        for server in session.query(Server).all():
            try:
                self._docker_client.containers.get(f"wilfred_{server.id}")
            except docker.errors.NotFound:
                self.set_status(server, "stopped")

    def _parse_startup_command(self, cmd, server, image):
        return ContainerVariables(server, image).parse_startup_command(
            cmd.replace("{{SERVER_MEMORY}}", str(server.memory)).replace(
                "{{SERVER_PORT}}", str(server.port)
            )
        )

    def _container_alive(self, server):
        try:
            self._docker_client.containers.get(f"wilfred_{server.id}")
        except docker.errors.NotFound:
            return False

        return True

    def _start(self, server):
        path = f"{self._configuration['data_path']}/{server.id}"
        image = self._images.get_image(server.image_uid)

        try:
            remove_file(f"{path}/install.sh")
        except Exception:
            pass

        try:
            self._docker_client.containers.run(
                image["docker_image"],
                self._parse_startup_command(server.custom_startup, server, image)
                if server.custom_startup is not None
                else f"{self._parse_startup_command(image['command'], server, image)}",
                volumes={path: {"bind": "/server", "mode": "rw"}},
                name=f"wilfred_{server.id}",
                remove=True,
                ports={f"{server.port}/tcp": server.port},
                detach=True,
                working_dir="/server",
                mem_limit=f"{server.memory}m",
                oom_kill_disable=True,
                stdin_open=True,
                environment=ContainerVariables(server, image).get_env_vars(),
                user=image["user"] if image["user"] else "root",
            )
        except Exception as e:
            error(
                f"unable to start Docker container {click.style(str(e), bold=True)}",
                exit_code=1,
            )

    def _stop(self, server):
        image = self._images.get_image(server.image_uid)

        try:
            container = self._docker_client.containers.get(f"wilfred_{server.id}")
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

        self.command(server, image["stop_command"])

        stopped = False

        while not stopped:
            try:
                self._docker_client.containers.get(f"wilfred_{server.id}")
            except docker.errors.NotFound:
                stopped = True
