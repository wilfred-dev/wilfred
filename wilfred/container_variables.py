# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred


class ContainerVariables(object):
    def __init__(self, server, image, database, install=False):
        self._server = server
        self._image = image
        self._database = database
        self._install = install

    def parse_startup_command(self, cmd):
        for k, v in self.get_env_vars().items():
            cmd = cmd.replace("{{image.env." + str(k) + "}}", str(v if v else ""))

        return cmd

    def get_env_vars(self):
        environment = {}

        for var in self._image["variables"]:
            value = self._database.query(
                f"SELECT value FROM variables WHERE server_id = '{self._server['id']}' AND variable = '{var['variable']}'",
                fetchone=True,
            )["value"]

            if not value:
                continue

            if var["install_only"] and not self._install:
                continue

            environment[var["variable"]] = value

        environment["SERVER_MEMORY"] = self._server["memory"]
        environment["SERVER_PORT"] = self._server["port"]

        return environment
