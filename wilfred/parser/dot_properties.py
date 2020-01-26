# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

# from configparser import RawConfigParser


def properties_parser(path):
    # with open(path) as f:
    #     file_content = '[dummy_section]\n' + f.read()

    # config_parser = RawConfigParser()
    # config_parser.read_string(file_content)

    # return config_parser

    with open(path) as f:
        raw = f.read().split("\n")

    return raw
