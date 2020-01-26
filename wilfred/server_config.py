# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

from wilfred.parser.dot_properties import properties_parser


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

        self._raw = []
        self._variables = []  # list of dicts

        self._parse()

    def _parse(self):
        for file in self._image["config"]["files"]:
            path = f"{self._configuration['data_path']}/{self._server.id}"

            if file["parser"] == "properties":
                self._raw.append(properties_parser(f"{path}/{file['filename']}"))

                break

            raise Exception("no available parser for this type of file")
        return True

    def pretty(self):
        """Returns parsed configuration variables in a print-friendly format"""

        return self._raw

    def edit(self, variable, value):
        """Modifies value of specified variable"""

        pass
