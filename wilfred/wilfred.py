# -*- coding: utf-8 -*-

# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import click

from wilfred.docker_conn import docker_client
from wilfred.version import version
from wilfred.config_parser import Config
from wilfred.database import Database
from wilfred.servers import Servers
from wilfred.images import Images
from wilfred.message_handler import warning, error

config = Config()
database = Database()
images = Images()
servers = Servers(database, docker_client(), config.configuration, images)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("✨ wilfred version {}".format(version))
    ctx.exit()


def main():
    cli()


@click.group()
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
def cli():
    """
    A CLI for managing game servers using Docker.

    ⚠️  This is still experimental, features may not be implemented yet or broken.
    """

    pass


@cli.command()
def setup():
    """setup wilfred, create config"""

    if config.configuration:
        warning("A configuration file for Wilfred already exists.")
        click.confirm("Are you sure you wan't to continue?", abort=True)

    data_path = click.prompt(
        "Path for storing server data", default="/srv/wilfred/servers"
    )

    config.write(data_path)


@cli.command("servers")
def servers_list():
    """list of all servers"""

    click.echo(servers.pretty())

    pass


@cli.command("images")
def list_images():
    """list available images"""

    click.echo(images.pretty())

    pass


@cli.command()
def create():
    """create a new server"""

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    click.secho("Available Images", bold=True)
    click.echo(images.pretty())

    name = click.prompt("Name")
    image_uuid = click.prompt("Image UUID", default="default-vanilla-minecraft")
    port = click.prompt("Port", default=25565)
    memory = click.prompt("Memory", default=1024)

    servers.create(name, image_uuid, memory, port)

    pass


@cli.command("sync")
def sync_cmd():
    """
    sync all servers on file with Docker (start/stop/create)
    """

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    servers.sync()


@cli.command()
@click.argument("name")
def start(name):
    """
    start existing server
    """

    servers.set_status(servers.get_by_name(name)[0], "running")
    servers.sync()


@cli.command()
def delete():
    """delete existing server"""

    if not config.configuration:
        error("Wilfred has not been configured", exit_code=1)

    pass


if __name__ == "__main__":
    main()
