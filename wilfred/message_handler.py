#################################################################
#                                                               #
# Wilfred                                                       #
# Copyright (C) 2020-2021, Vilhelm Prytz, <vilhelm@prytznet.se> #
#                                                               #
# Licensed under the terms of the MIT license, see LICENSE.     #
# https://github.com/wilfred-dev/wilfred                        #
#                                                               #
#################################################################

import click
import sys


def _message(prefix, msg):
    click.echo(f"{prefix} {msg}")


def ui_exception(e):
    _exception_name = click.style(f"{type(e).__name__}", bold=True)
    error(f"{_exception_name} {str(e)}", exit_code=1)


def error(message, exit_code=None):
    _message(prefix=click.style("💥 Error", fg="red"), msg=message)

    if exit_code is not None:
        sys.exit(exit_code)


def warning(message, exit_code=None):
    _message(prefix=click.style("⚠️  Warning ", fg="yellow"), msg=message)

    if exit_code is not None:
        sys.exit(exit_code)


def info(message, exit_code=None):
    _message(prefix=click.style("🔵 Info", fg="blue"), msg=message)

    if exit_code is not None:
        sys.exit(exit_code)
