# -*- coding: utf-8 -*-

# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

import click
import codecs
import locale
import os
import sys

from yaspin import yaspin
from pathlib import Path

from wilfred.docker_conn import docker_client
from wilfred.version import version
from wilfred.config_parser import Config
from wilfred.database import Database
from wilfred.servers import Servers
from wilfred.images import Images
from wilfred.message_handler import warning, error
from wilfred.core import is_integer, random_string

if sys.platform.startswith("win"):
    click.echo("Wilfred does not support Windows")
    sys.exit(1)

config = Config()
database = Database()
images = Images()
servers = Servers(database, docker_client(), config.configuration, images)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(
        "✨ wilfred version {}".format(
            "development (0.0.0.dev0)" if version == "0.0.0.dev0" else version
        )
    )
    ctx.exit()


def main():
    # snap packages raise some weird ASCII codec errors, so we just force C.UTF-8
    if (
        codecs.lookup(locale.getpreferredencoding()).name == "ascii"
        and os.name == "posix"
    ):
        os.environ["LC_ALL"] = "C.UTF-8"
        os.environ["LANG"] = "C.UTF-8"

    cli()


@click.group()
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
def cli():
    """
    Wilfred

    🐿️  A CLI for managing game servers using Docker.

    ⚠️  Wilfred is currently under development and should not be considered stable.
    Features may brake or may not beimplemented yet. Use with caution.
    """

    pass


@cli.command()
def setup():
    """Setup wilfred, create configuration."""

    if config.configuration:
        warning("A configuration file for Wilfred already exists.")
        click.confirm("Are you sure you wan't to continue?", abort=True)

    data_path = click.prompt(
        "Path for storing server data", default=f"{str(Path.home())}/wilfred/servers"
    )

    config.write(data_path)


@cli.command("servers")
def servers_list():
    """List all existing servers."""

    click.echo(servers.pretty())


@cli.command("images")
@click.option("--refresh", help="Download the default images from GitHub", is_flag=True)
def list_images(refresh):
    """List images available on file."""

    if refresh:
        with yaspin(text="Refreshing images", color="yellow") as spinner:
            images.download_default()

            spinner.ok("✅")

    click.echo(images.pretty())


@cli.command()
@click.option(
    "--console",
    help="Attach to server console immediately after creation.",
    is_flag=True,
)
@click.option(
    "--detach", help="Immediately detach during install.", is_flag=True,
)
@click.pass_context
def create(ctx, console, detach):
    """Create a new server."""

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    click.secho("Available Images", bold=True)
    click.echo(images.pretty())

    name = click.prompt("Name").lower()

    if " " in name:
        error("space not allowed in name", exit_code=1)

    image_uid = click.prompt("Image UID", default="minecraft-vanilla")

    if " " in image_uid:
        error("space not allowed in image_uid", exit_code=1)

    if not images.get_image(image_uid):
        error("image does not exist", exit_code=1)

    port = click.prompt("Port", default=25565)
    memory = click.prompt("Memory", default=1024)

    click.secho("Environment Variables", bold=True)

    # create
    database.query(
        " ".join(
            (
                "INSERT INTO servers",
                "(id, name, image_uid, memory, port, status)"
                f"VALUES ('{random_string()}', '{name}', '{image_uid}', '{memory}', '{port}', 'installing')",
            )
        )
    )

    server = database.query(
        f"SELECT * FROM servers WHERE name = '{name}'", fetchone=True
    )

    # environment variables available for the container
    for v in images.get_image(image_uid)["variables"]:
        value = click.prompt(v["prompt"], default=v["default"])

        database.query(
            f"INSERT INTO variables (server_id, variable, value) VALUES ('{server['id']}', '{v['variable']}', '{value}')"
        )

    with yaspin(text="Creating server", color="yellow") as spinner:
        if not detach:
            spinner.write(
                "> You can safely press CTRL+C, the installation will continue in the background."
            )
            spinner.write(
                "> Run `wilfred servers` too see when the status changes from `installing` to `stopped`."
            )
            spinner.write(
                f"> You can also follow the installation log using `wilfred console {server['name']}`"
            )

        if detach:
            spinner.write(
                "> Installation will continue in background, use `wilfred servers` to see if process has finished."
            )

        servers.install(server, skip_wait=True if detach else False)
        spinner.ok("✅ ")

    if console:
        ctx.invoke(start, name=name)
        ctx.invoke(server_console, name=name)


@cli.command("sync")
def sync_cmd():
    """
    Sync all servers on file with Docker (start/stop/kill/create).
    """

    with yaspin(text="Docker sync", color="yellow") as spinner:
        if not config.configuration:
            spinner.fail("💥 Wilfred has not been configured")

        servers.sync()

        spinner.ok("✅ ")


@cli.command()
@click.argument("name")
@click.option(
    "--console", help="Attach to server console immediately after start.", is_flag=True
)
@click.pass_context
def start(ctx, name, console):
    """
    Start server by specifiying the
    name of the server as argument.
    """

    servers.sync(db_update=True)

    with yaspin(text="Server start", color="yellow") as spinner:
        if not config.configuration:
            spinner.fail("💥 Wilfred has not been configured")
            sys.exit(1)

        server = servers.get_by_name(name.lower())

        if not server:
            spinner.fail("💥 Server does not exit")
            sys.exit(1)

        if server["status"] == "installing":
            spinner.fail("💥 Server is installing, start blocked.")
            sys.exit(1)

        servers.set_status(server, "running")
        servers.sync()

        spinner.ok("✅ ")

        if console:
            ctx.invoke(server_console, name=name)


@cli.command()
@click.argument("name")
def kill(name):
    """
    Forcefully kill running server.
    """

    if click.confirm(
        "Are you sure you want to do this? This will kill the running container without saving data."
    ):
        with yaspin(text="Killing server", color="yellow") as spinner:
            if not config.configuration:
                spinner.fail("💥 Wilfred has not been configured")
                sys.exit(1)

            server = servers.get_by_name(name.lower())

            if not server:
                spinner.fail("💥 Server does not exit")
                sys.exit(1)

            servers.kill(server)
            servers.set_status(server, "stopped")
            servers.sync()

            spinner.ok("✅ ")


@cli.command()
@click.argument("name")
def stop(name):
    """
    Stop server.
    """

    servers.sync()

    with yaspin(text="Stopping server", color="yellow") as spinner:
        if not config.configuration:
            spinner.fail("💥 Wilfred has not been configured")
            sys.exit(1)

        server = servers.get_by_name(name.lower())

        if not server:
            spinner.fail("💥 Server does not exit")
            sys.exit(1)

        if server["status"] == "installing":
            spinner.fail(
                " ".join(
                    (
                        "💥 Server is installing, you cannot gracefully stop it.",
                        "Use `wilfred kill` if the installation process has hanged.",
                    )
                )
            )
            sys.exit(1)

        servers.set_status(server, "stopped")
        servers.sync()

        spinner.ok("✅ ")


@cli.command()
@click.argument("name")
def delete(name):
    """
    Delete existing server.
    """

    if click.confirm(
        "Are you sure you want to do this? All data will be permanently deleted."
    ):
        with yaspin(text="Deleting server", color="yellow") as spinner:
            if not config.configuration:
                spinner.fail("💥 Wilfred has not been configured")
                sys.exit(1)

            server = servers.get_by_name(name.lower())

            if not server:
                spinner.fail("💥 Server does not exit")
                sys.exit(1)

            servers.remove(server)
            spinner.ok("✅ ")


@cli.command("console")
@click.argument("name")
def server_console(name):
    """
    Attach to server console, view log and run commands.
    """

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    server = servers.get_by_name(name.lower())

    if not server:
        error("Server does not exit", exit_code=1)

    click.secho(
        " ".join(
            (
                f"Viewing server console of {name} (id {server['id']})",
                f"{'- input disabled, installing' if server['status'] == 'installing' else ''}",
            )
        ),
        bold=True,
    )

    servers.console(
        server, disable_user_input=True if server["status"] == "installing" else False
    )


@cli.command()
@click.argument("name")
def edit(name):
    """
    Edit server (name, memory, port, environment variables)
    """

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    server = servers.get_by_name(name.lower())

    if not server:
        error("Server does not exist", exit_code=1)

    click.echo(servers.pretty(server=server))
    click.echo("Leave values empty to use existing value")

    name = click.prompt("Name", default=server["name"]).lower()

    if " " in name:
        error("space not allowed in name", exit_code=1)

    port = click.prompt("Port", default=server["port"])
    memory = click.prompt("Memory", default=server["memory"])

    if not is_integer(port) or not is_integer(memory):
        error("port/memory must be integer", exit_code=1)

    click.secho("Environment Variables", bold=True)

    for v in images.get_image(server["image_uid"])["variables"]:
        if v["install_only"]:
            continue

        curr = database.query(
            f"SELECT * FROM variables WHERE server_id = '{server['id']}' AND variable = '{v['variable']}'",
            fetchone=True,
        )

        if not curr:
            continue

        database.query(
            " ".join(
                (
                    f"UPDATE variables SET value = '{click.prompt(v['prompt'], default=curr['value'])}'",
                    f"WHERE server_id = '{server['id']}' AND variable = '{v['variable']}'",
                )
            )
        )

    database.query(f"UPDATE servers SET name = '{name}' WHERE id='{server['id']}'")
    database.query(f"UPDATE servers SET port = {port} WHERE id='{server['id']}'")
    database.query(f"UPDATE servers SET memory = {memory} WHERE id='{server['id']}'")

    click.echo(
        "✅ Server information updated, restart server for changes to take effect"
    )


if __name__ == "__main__":
    main()
