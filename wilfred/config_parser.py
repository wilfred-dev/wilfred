# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import json
import click
from appdirs import user_config_dir
from os.path import isfile
from wilfred.message_handler import warning


class Config(object):
    def __init__(self):
        self.config_path = f"{user_config_dir()}/wilfred/config.json"
        self._read()

    def _read(self):
        if not isfile(self.config_path):
            warning(
                "configuration file does not exist. Run `wilfred setup` to initiate the program."
            )
            self.configuration = None

            return

        with open(self.config_path) as f:
            self.configuration = json.loads(f.read())
