####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

import requests
import click

from random import choice
from string import ascii_lowercase, digits

from wilfred.version import version
from wilfred.message_handler import warning


def random_string(length=8):
    """
    Generate a random string of fixed length

    :param int length: length of string to generate
    """

    return "".join(choice(ascii_lowercase + digits) for i in range(length))


def check_for_new_releases():
    """
    Checks if a new version is available on GitHub
    """

    r = requests.get("https://api.github.com/repos/wilfred-dev/wilfred/tags")

    if r.status_code != requests.codes.ok:
        warning("unable to retrieve latest version")

        return

    try:
        latest_release = r.json()[0]["name"]
    except Exception:
        warning("unable to parse release data")

        return

    if latest_release != f"v{version}":
        click.echo(f"🎉 A new version of Wilfred is available! {latest_release}")

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
