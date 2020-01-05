# -*- coding: utf-8 -*-

# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import click
import codecs
import locale
import os
import sys

from yaspin import yaspin

from wilfred.docker_conn import docker_client
from wilfred.version import version
from wilfred.config_parser import Config
from wilfred.database import Database
from wilfred.servers import Servers
from wilfred.images import Images
from wilfred.message_handler import warning, error
from wilfred.core import is_integer, random_string

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
        "Path for storing server data", default="/srv/wilfred/servers"
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
@click.pass_context
def create(ctx, console):
    """Create a new server."""

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    click.secho("Available Images", bold=True)
    click.echo(images.pretty())

    name = click.prompt("Name").lower()

    if " " in name:
        error("space not allowed in name", exit_code=1)

    image_uuid = click.prompt("Image UUID", default="minecraft-vanilla")

    if " " in image_uuid:
        error("space not allowed in image_uuid", exit_code=1)

    if not images.get_image(image_uuid):
        error("image does not exist", exit_code=1)

    port = click.prompt("Port", default=25565)
    memory = click.prompt("Memory", default=1024)

    click.secho("Environment Variables", bold=True)

    # create
    database.query(
        " ".join(
            (
                "INSERT INTO servers",
                "(id, name, image_uuid, memory, port, status)"
                f"VALUES ('{random_string()}', '{name}', '{image_uuid}', '{memory}', '{port}', 'created')",
            )
        )
    )

    server_id = database.query(
        f"SELECT id FROM servers WHERE name = '{name}'", fetchone=True
    )["id"]

    # environment variables available for the container
    for v in images.get_image(image_uuid)["variables"]:
        value = click.prompt(v["prompt"], default=v["default"])

        database.query(
            f"INSERT INTO variables (server_id, variable, value) VALUES ('{server_id}', '{v['variable']}', '{value}')"
        )

    with yaspin(text="Creating server", color="yellow") as spinner:
        servers.sync(db_update=True)

        spinner.ok("✅ ")

    if console:
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

    with yaspin(text="Server start", color="yellow") as spinner:
        if not config.configuration:
            spinner.fail("💥 Wilfred has not been configured")
            sys.exit(1)

        server = servers.get_by_name(name.lower())

        if not server:
            spinner.fail("💥 Server does not exit")
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

    with yaspin(text="Stopping server", color="yellow") as spinner:
        if not config.configuration:
            spinner.fail("💥 Wilfred has not been configured")
            sys.exit(1)

        server = servers.get_by_name(name.lower())

        if not server:
            spinner.fail("💥 Server does not exit")
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

    click.secho(f"Viewing server console of {name} (id {server['id']})", bold=True)

    servers.console(server)


@cli.command()
@click.argument("name")
def edit(name):
    """
    Edit server information (name, memory, port)
    """

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    server = servers.get_by_name(name.lower())

    if not server:
        error("Server does not exist", exit_code=1)

    click.echo(servers.pretty(server=server))
    click.echo("Leave values empty to use existing value")

    name = click.prompt("Name", default="").lower()

    if " " in name:
        error("space not allowed in name", exit_code=1)

    port = click.prompt("Port", default="")
    memory = click.prompt("Memory", default="")

    if name:
        database.query(f"UPDATE servers SET name = '{name}' WHERE id='{server['id']}'")

    if port:
        if not is_integer(port):
            error("port must be integer", exit_code=1)

        database.query(f"UPDATE servers SET port = {port} WHERE id='{server['id']}'")

    if memory:
        if not is_integer(memory):
            error("memory must be integer", exit_code=1)

        database.query(
            f"UPDATE servers SET memory = {memory} WHERE id='{server['id']}'"
        )

    if name or port or memory:
        click.echo(
            "✅ Server information updated, restart server for changes to take effect"
        )


if __name__ == "__main__":
    main()
