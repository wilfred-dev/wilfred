# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020


class ContainerVariables(object):
    def __init__(self, server, image, database, install=False):
        self._server = server
        self._image = image
        self._database = database
        self._install = install

    def parse_startup_command(self, cmd):
        for k, v in self.get_env_vars().items():
            cmd = cmd.replace("{{image.env." + k + "}}", v)

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

        return environment
