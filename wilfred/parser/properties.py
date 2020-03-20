####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

from configparser import RawConfigParser


def _config_parser(path):
    """appends a dummy section to the top of the raw file so that the built-in
    python function, ConfigParser, can read and parse the file"""

    with open(path) as f:
        file_content = "[dummy_section]\n" + f.read()

    config_parser = RawConfigParser()
    config_parser.read_string(file_content)

    return config_parser


def properties_read(path):
    config_parser = _config_parser(path)

    settings = {}

    for item in config_parser.items("dummy_section"):
        settings[item[0]] = item[1]

    return settings


def properties_write(path, key, value):
    with open(path) as f:
        raw = f.read().split("\n")

    _write = []

    for line in raw:
        if key in line:
            if line.split("=")[0] == key:
                _write.append(f"{key}={value}")
                continue

        _write.append(line)

    with open(path, "w") as f:
        f.write("\n".join(_write))
