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
import click

from appdirs import user_config_dir
from os.path import isfile, isdir
from pathlib import Path

from wilfred.message_handler import warning, error

API_VERSION = 1


class Config(object):
    def __init__(self):
        self.data_dir = f"{user_config_dir()}/wilfred"
        self.config_path = f"{self.data_dir}/config.json"

        if not isdir(self.data_dir):
            Path(self.data_dir).mkdir(parents=True, exist_ok=True)

        self._read()

    def _read(self):
        if not isfile(self.config_path):
            warning(
                "configuration file does not exist. Run `wilfred setup` to initiate the program.",
            )
            self.configuration = None

            return

        with open(self.config_path) as f:
            self.configuration = json.loads(f.read())

        if self.configuration["meta"]["version"] != API_VERSION:
            error(
                f"configuration has API level {self.configuration['meta']['version']}, Wilfreds API level is {API_VERSION}",
                exit_code=1,
            )

    def write(self, data_path):
        try:
            Path(data_path).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            error(
                f"unable to access specified path {click.style(str(e), bold=True)}",
                exit_code=1,
            )

        with open(self.config_path, "w") as f:
            f.write(
                json.dumps(
                    {"meta": {"version": API_VERSION}, "data_path": data_path}, indent=4
                )
            )
