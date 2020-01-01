# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import click
import sys


def _message(prefix, msg):
    click.echo(f"{prefix} {msg}")


def error(message, exit_code=None):
    _message(prefix=click.style("🔴 Error", fg="red"), msg=message)

    if exit_code:
        sys.exit(exit_code)


def warning(message, exit_code=None):
    _message(prefix=click.style("⚠️  Warning ", fg="yellow"), msg=message)

    if exit_code:
        sys.exit(exit_code)


def info(message, exit_code=None):
    _message(prefix=click.style("🔵 Info", fg="blue"), msg=message)

    if exit_code:
        sys.exit(exit_code)
