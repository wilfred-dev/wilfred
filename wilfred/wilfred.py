# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import click

from wilfred.docker_conn import docker_client
from wilfred.version import version
from wilfred.config_parser import Config
from wilfred.database import Database
from wilfred.message_handler import error

client = docker_client()
config = Config().configuration
database = Database()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"✨ wilfred version {version}")
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

    pass


@cli.command()
def servers():
    """list of all servers"""

    try:
        containers = client.containers.list()
    except Exception as e:
        error(
            click.style("unable to communicate with docker - ", bold=True) + str(e),
            exit_code=1,
        )

    pass


@cli.command()
def create():
    """create a new server"""

    pass


@cli.command()
def delete():
    """delete existing server"""

    pass


if __name__ == "__main__":
    main()
