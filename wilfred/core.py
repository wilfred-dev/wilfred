# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

from random import choice
from string import ascii_lowercase, digits


def random_string(length=8):
    """
    Generate a random string of fixed length

    :param int length: length of string to generate
    """

    return "".join(choice(ascii_lowercase + digits) for i in range(length))


def is_integer(variable):
    try:
        int(variable)
    except Exception:
        return False

    return True
