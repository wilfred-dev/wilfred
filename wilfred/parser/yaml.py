# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

import yaml


def yaml_read(path):
    with open(path) as f:
        _raw = yaml.load(f, Loader=yaml.FullLoader)

    return _raw


def yaml_write(path, key, value):
    with open(path) as f:
        _raw = yaml.load(f, Loader=yaml.FullLoader)

    _key = key.split(":")
    curr = _raw

    for level in _key:
        print(curr)
        print(level)
        if level in curr:
            curr = _raw[level]

    curr = value

    with open(path, "w") as f:
        yaml.dump(_raw, f)

    pass
