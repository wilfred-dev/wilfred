# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import json
from appdirs import user_config_dir
from os.path import isfile, isdir
from pathlib import Path
from wilfred.message_handler import warning


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
                "configuration file does not exist. Run `wilfred setup` to initiate the program."
            )
            self.configuration = None

            return

        with open(self.config_path) as f:
            self.configuration = json.loads(f.read())
