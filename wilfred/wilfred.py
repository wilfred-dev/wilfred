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
from sqlalchemy.exc import IntegrityError

from wilfred.docker_conn import docker_client
from wilfred.version import version
from wilfred.config_parser import Config
from wilfred.database import session, database_path, Server, EnvironmentVariable
from wilfred.servers import Servers
from wilfred.images import Images
from wilfred.message_handler import warning, error
from wilfred.core import is_integer, random_string, check_for_new_releases
from wilfred.migrate import Migrate

if sys.platform.startswith("win"):
    click.echo("Wilfred does not support Windows")
    sys.exit(1)


config = Config()
images = Images()
servers = Servers(docker_client(), config.configuration, images)

# check
Migrate()


def print_version(ctx, param, value):
    """
    print version and exit
    """

    if not value or ctx.resilient_parsing:
        return

    check_for_new_releases()

    click.echo(
        "✨ wilfred version {}".format(
            "development (0.0.0.dev0)" if version == "0.0.0.dev0" else f"v{version}"
        )
    )
    ctx.exit()


def print_path(ctx, param, value):
    """
    print config/data paths
    """

    if not value or ctx.resilient_parsing:
        return

    click.echo(f"Configuration file: {click.format_filename(config.config_path)}")
    click.echo(f"Image config file: {click.format_filename(images.image_dir)}")
    click.echo(f"Database file: {click.format_filename(database_path)}")
    if config.configuration:
        click.echo(
            f"Server data: {click.format_filename(config.configuration['data_path'])}"
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
@click.option(
    "--path", is_flag=True, callback=print_path, expose_value=False, is_eager=True
)
def cli():
    """
    Wilfred

    🐿️  A CLI for managing game servers using Docker.

    ⚠️  Wilfred is currently under development and should not be considered stable.
    Features may break or may not be implemented yet. Use with caution.
    """

    pass


@cli.command()
def setup():
    """Setup wilfred, create configuration."""

    if config.configuration:
        warning("A configuration file for Wilfred already exists.")
        click.confirm("Are you sure you wan't to continue?", abort=True)

    data_path = click.prompt(
        "Path for storing server data",
        default=f"{str(Path.home())}/wilfred-data/servers",
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
            images.download_default(read=True)

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

    name = click.prompt("Server Name").lower()

    if " " in name:
        error("space not allowed in name", exit_code=1)

    click.secho("Available Images", bold=True)
    click.echo(images.pretty())

    image_uid = click.prompt("Image UID", default="minecraft-vanilla")

    if " " in image_uid:
        error("space not allowed in image_uid", exit_code=1)

    if not images.get_image(image_uid):
        error("image does not exist", exit_code=1)

    port = click.prompt("Port", default=25565)
    memory = click.prompt("Memory", default=1024)

    click.secho("Environment Variables", bold=True)

    # create
    server = Server(
        id=random_string(),
        name=name,
        image_uid=image_uid,
        memory=memory,
        port=port,
        custom_startup=None,
        status="installing",
    )
    session.add(server)

    try:
        session.commit()
    except IntegrityError as e:
        error(f"unable to create server {click.style(str(e), bold=True)}", exit_code=1)

    # environment variables available for the container
    for v in images.get_image(image_uid)["variables"]:
        if not v["hidden"]:
            value = click.prompt(
                v["prompt"], default=v["default"] if v["default"] is not True else None
            )

        if v["hidden"]:
            value = v["default"]

        variable = EnvironmentVariable(
            server_id=server.id, variable=v["variable"], value=value
        )
        session.add(variable)

    try:
        session.commit()
    except IntegrityError as e:
        error(
            f"unable to create variables {click.style(str(e), bold=True)}", exit_code=1
        )

    # custom startup command
    if click.confirm("Would you like to set a custom startup command (optional)?"):
        custom_startup = click.prompt(
            "Custom startup command", default=images.get_image(image_uid)["command"]
        )

        server.custom_startup = custom_startup
        try:
            session.commit()
        except IntegrityError as e:
            error(
                f"unable to set startup command {click.style(str(e), bold=True)}",
                exit_code=1,
            )

    with yaspin(text="Creating server", color="yellow") as spinner:
        servers.install(server, skip_wait=True if detach else False, spinner=spinner)
        spinner.ok("✅ ")

    if console:
        ctx.invoke(start, name=name)
        ctx.invoke(server_console, name=name)


@cli.command("sync")
def sync_cmd():
    """
    Sync all servers on file with Docker (start/stop/kill).
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

    servers.sync()

    with yaspin(text="Server start", color="yellow") as spinner:
        if not config.configuration:
            spinner.fail("💥 Wilfred has not been configured")
            sys.exit(1)

        server = session.query(Server).filter_by(name=name.lower()).first()

        if not server:
            spinner.fail("💥 Server does not exit")
            sys.exit(1)

        if server.status == "installing":
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

            server = session.query(Server).filter_by(name=name.lower()).first()

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
    Stop server gracefully.
    """

    servers.sync()

    with yaspin(text="Stopping server", color="yellow") as spinner:
        if not config.configuration:
            spinner.fail("💥 Wilfred has not been configured")
            sys.exit(1)

        server = session.query(Server).filter_by(name=name.lower()).first()

        if not server:
            spinner.fail("💥 Server does not exit")
            sys.exit(1)

        if server.status == "installing":
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
@click.option(
    "--console", help="Attach to server console immediately after start.", is_flag=True
)
@click.pass_context
def restart(ctx, name, console):
    """
    Restart server by specifiying the
    name of the server as argument.
    """

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    ctx.invoke(stop, name=name)
    ctx.invoke(start, name=name)

    if console:
        ctx.invoke(server_console, name=name)


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

            server = session.query(Server).filter_by(name=name.lower()).first()

            if not server:
                spinner.fail("💥 Server does not exit")
                sys.exit(1)

            servers.remove(server)
            spinner.ok("✅ ")


@cli.command("command")
@click.argument("name")
@click.argument("command")
def run_command(name, command):
    """
    Send command to STDIN of server
    """

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    server = session.query(Server).filter_by(name=name.lower()).first()

    if not server:
        error("Server does not exit", exit_code=1)

    servers.command(server, command)


@cli.command(
    "console",
    short_help="\n\n".join(
        (
            " ".join(
                (
                    "Attach current terminal to the console of a specific server (STDIN of running process).",
                    "This allows you to view the current log and send commands.",
                )
            ),
            "Use CTRL+C to exit the console, the server will continue to run in the background.",
        )
    ),
)
@click.argument("name")
def server_console(name):
    """
    Attach to server console, view log and run commands.
    """

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    server = session.query(Server).filter_by(name=name.lower()).first()

    if not server:
        error("Server does not exit", exit_code=1)

    click.secho(
        " ".join(
            (
                f"Viewing server console of {name} (id {server.id})",
                f"{'- input disabled, installing' if server.status == 'installing' else ''}",
            )
        ),
        bold=True,
    )

    servers.console(
        server, disable_user_input=True if server.status == "installing" else False
    )


@cli.command(
    short_help=" ".join(
        (
            "Edit existing server (name, memory, port, environment variables and the custom startup command).",
            "Restart server after update for changes to take effect.",
        )
    )
)
@click.argument("name")
def edit(name):
    """
    Edit server (name, memory, port, environment variables)
    """

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    server = session.query(Server).filter_by(name=name.lower()).first()

    if not server:
        error("Server does not exist", exit_code=1)

    click.echo(servers.pretty(server=server))
    click.echo("Leave values empty to use existing value")

    name = click.prompt("Name", default=server.name).lower()

    if " " in name:
        error("space not allowed in name", exit_code=1)

    port = click.prompt("Port", default=server.port)
    memory = click.prompt("Memory", default=server.memory)

    if not is_integer(port) or not is_integer(memory):
        error("port/memory must be integer", exit_code=1)

    click.secho("Environment Variables", bold=True)

    for v in images.get_image(server.image_uid)["variables"]:
        if v["install_only"]:
            continue

        current_variable = (
            session.query(EnvironmentVariable)
            .filter_by(server_id=server.id)
            .filter_by(variable=v["variable"])
            .first()
        )

        if not current_variable:
            continue

        if not v["hidden"]:
            value = click.prompt(v["prompt"], default=current_variable.value)

        if v["hidden"]:
            value = v["default"]

        current_variable.value = value

        try:
            session.commit()
        except IntegrityError as e:
            error(
                f"unable to edit variables {click.style(str(e), bold=True)}",
                exit_code=1,
            )

    server.custom_startup = (
        None if server.custom_startup == "None" else server.custom_startup
    )
    custom_startup = None

    if server.custom_startup is not None:
        custom_startup = click.prompt(
            "Custom startup command", default=server.custom_startup
        )

    if server.custom_startup is None:
        if click.confirm("Would you like to set a custom startup command?"):
            custom_startup = click.prompt(
                "Custom startup command",
                default=images.get_image(server.image_uid)["command"],
            )

    server.name = name
    server.port = port
    server.memory = memory

    if custom_startup:
        server.custom_startup = custom_startup

    try:
        session.commit()
    except IntegrityError as e:
        error(f"unable to edit server {click.style(str(e), bold=True)}", exit_code=1)

    click.echo(
        "✅ Server information updated, restart server for changes to take effect"
    )


if __name__ == "__main__":
    main()
