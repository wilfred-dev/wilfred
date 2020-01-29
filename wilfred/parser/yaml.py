# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

import yaml
import click

from wilfred.core import set_in_dict


def _remove_unnecessary_lists(raw):
    d = {}
    for k, v in raw.items():
        if type(v) in [list, tuple] and type(v[0]) in [dict]:
            d[k] = v[0]
            continue
        d[k] = v

    return d


def yaml_read(path):
    with open(path) as f:
        _raw = yaml.load(f, Loader=yaml.FullLoader)

    def _walk(d):
        """
        Walk a tree (nested dicts).

        For each 'path', or dict, in the tree, returns a 3-tuple containing:
        (path, sub-dicts, values)

        where:
        * path is the path to the dict
        * sub-dicts is a tuple of (key,dict) pairs for each sub-dict in this dict
        * values is a tuple of (key,value) pairs for each (non-dict) item in this dict
        """
        # nested dict keys
        nested_keys = tuple(k for k in d.keys() if isinstance(d[k], dict))
        # key/value pairs for non-dicts
        items = tuple((k, d[k]) for k in d.keys() if k not in nested_keys)

        # return path, key/sub-dict pairs, and key/value pairs
        yield ("/", [(k, d[k]) for k in nested_keys], items)

        # recurse each subdict
        for k in nested_keys:
            for res in _walk(d[k]):
                # for each result, stick key in path and pass on
                res = ("/%s" % k + res[0], res[1], res[2])
                yield res

    _reformatted = {}

    # walk _raw dictionary
    for (path, dicts, items) in _walk(_remove_unnecessary_lists(_raw)):
        for key, val in items:
            key = f"{path}{key}"

            # yaml lists are not editable by Wilfred for now, too much work
            if type(val) in [list, tuple]:
                key = f"{key} ({click.style('yaml lists are not editable with Wilfred', bold=True)})"

            _reformatted[key] = str(val)

    return _reformatted


def yaml_write(path, key, value):  # editing does not do anything yet!!!
    with open(path) as f:
        _raw = yaml.load(f, Loader=yaml.FullLoader)

    _raw[key.split("/")[1]][0] = set_in_dict(
        _remove_unnecessary_lists(_raw), key.split("/")[1:], value
    )

    with open(path, "w") as f:
        yaml.dump(_raw, f)

    return True
