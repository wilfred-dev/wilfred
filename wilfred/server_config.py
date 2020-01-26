# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

import click

from tabulate import tabulate

from wilfred.parser.properties import properties_read, properties_write


class ServerConfig:
    def __init__(self, configuration, server, image):
        """
        Read, edit and update configurations for servers. Exposes server specific configs to Wilfred.

        :param dictionary configuration: JSON dict for Wilfred config
        :param str server: SQLAlchemy server object
        :param dictionary image: Image dict object
        """

        self._configuration = configuration
        self._server = server
        self._image = image

        self.raw = []
        self._variables = []  # list of dicts

        self._parse()

    def _parse(self):
        for file in self._image["config"]["files"]:
            path = f"{self._configuration['data_path']}/{self._server.id}"

            if file["parser"] == "properties":
                _raw = properties_read(f"{path}/{file['filename']}")
                _raw["_wilfred_config_filename"] = file["filename"]

                self.raw.append(_raw)

                continue

            raise Exception("no available parser for this type of file")
        return True

    def pretty(self):
        """Returns parsed configuration variables in a print-friendly format"""

        headers = {
            "file": click.style("Config File", bold=True),
            "setting": click.style("Setting", bold=True),
            "value": click.style("Value", bold=True),
        }

        data = []

        for file in self.raw:
            for k, v in file.items():
                data.append(
                    {"file": file["_wilfred_config_filename"], "setting": k, "value": v}
                )

        return tabulate(data, headers=headers, tablefmt="fancy_grid",)

    def edit(self, variable, value):
        """Modifies value of specified variable"""

        _times = 0
        for file in self.raw:
            if variable in file:
                _times += 1

        if _times > 2:
            # unhandled yet, will redo
            raise Exception("same variable key exists in multiple files")

        for file in self._image["config"]["files"]:
            if variable in next(
                filter(
                    lambda x: x["_wilfred_config_filename"] == file["filename"],
                    self.raw,
                ),
                {},
            ):
                path = f"{self._configuration['data_path']}/{self._server.id}"

                if file["parser"] == "properties":
                    properties_write(f"{path}/{file['filename']}", variable, value)