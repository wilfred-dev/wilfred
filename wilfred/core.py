#################################################################
#                                                               #
# Wilfred                                                       #
# Copyright (C) 2020-2021, Vilhelm Prytz, <vilhelm@prytznet.se> #
#                                                               #
# Licensed under the terms of the MIT license, see LICENSE.     #
# https://github.com/wilfred-dev/wilfred                        #
#                                                               #
#################################################################

import requests
import click

from random import choice
from string import ascii_lowercase, digits

from wilfred.version import version, commit_hash
from wilfred.message_handler import warning


def random_string(length=8):
    """
    Generate a random string of fixed length

    :param int length: length of string to generate
    """

    return "".join(choice(ascii_lowercase + digits) for i in range(length))


def check_for_new_releases(enable_emojis=True):
    """
    Checks if a new version is available on GitHub
    """

    url = "https://api.github.com/repos/wilfred-dev/wilfred/tags"
    key = "name"
    version_type = "version"

    if version == "0.0.0.dev0":
        url = "https://api.github.com/repos/wilfred-dev/wilfred/commits"
        key = "sha"
        version_type = "commit"

    r = requests.get(url)

    if r.status_code != requests.codes.ok:
        warning("unable to retrieve latest version")

        return

    try:
        latest = r.json()[0][key]
    except Exception:
        warning("unable to parse release data")

        return

    compare = commit_hash if version == "0.0.0.dev0" else f"v{version}"

    if latest != compare:
        click.echo(
            "".join(
                (
                    f"{'🎉 ' if enable_emojis else click.style('! ', fg='green')}",
                    f"A new {version_type} of Wilfred is available! {latest}",
                )
            )
        )

    return


def is_integer(variable):
    try:
        int(variable)
    except Exception:
        return False

    return True


def set_in_dict(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

    return dic
