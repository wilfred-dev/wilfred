####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

import json


def json_read(path):
    with open(path) as f:
        _raw = json.loads(f.read())

    _reformatted = {}

    def _iterate_dict(data, _name):
        """
        iterates a dictionary and continues to iterate the value of the dict if the
        type is dictionary, list or tuple (recursion). Adds the dictionary key and value
        to the _reformatted dict if it's a string, integer or boolean
        """

        _def = _name
        for k, v in data.items():
            _name = f"{_def}/{k}"
            if type(v) in [dict]:
                _iterate_dict(v, _name)
            if type(v) in [list, tuple]:
                _iterate_list(v, _name)

            if type(v) in [str, int, bool]:
                _reformatted[f"{_def}/{k}"] = v

    def _iterate_list(data, _name):
        """
        iterates a list and continues to iterate the values of the list if the
        type is dictionary, list or tuple (recursion). Adds the list value
        to the _reformatted dict if it's a string, integer or boolean
        """

        _def = _name

        i = 0
        for x in data:
            _name = f"{_def}/{i}"
            if type(x) in [dict]:
                _iterate_dict(x, _name)
            if type(x) in [list, tuple]:
                _iterate_list(x, _name)

            if type(x) in [str, int, bool]:
                _reformatted[f"{_def}/{i}"] = x

            i = i + 1

    for k, v in _raw.items():
        _name = k

        if type(v) in [dict]:
            _iterate_dict(v, _name)
        if type(v) in [list, tuple]:
            _iterate_list(v, _name)

        if type(v) in [str, int, bool]:
            _reformatted[k] = v

    return _reformatted


def json_write(path, key, value):
    raise Exception("Modifying JSON variables is currently not supported")

    # return True
