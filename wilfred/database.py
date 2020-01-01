# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import sqlite3
import click
from appdirs import user_data_dir
from os.path import isfile, isdir
from os import mkdir
from wilfred.message_handler import info, error


def _query(path, query):
    """
    executes specified query on sqlite3 database located at specified path

    :param str path: the path of the sqlite3 database
    :param str query: sql query to execute
    """

    try:
        conn = sqlite3.connect(path)

        cur = conn.cursor()
        cur.execute(query)

        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(path)
        error(
            "could not communicate with database " + click.style(str(e), bold=True),
            exit_code=1,
        )


class Database(object):
    def __init__(self):
        self.data_dir = f"{user_data_dir()}/wilfred"
        self.database_path = f"{self.data_dir}/wilfred.db"

        if not isdir(self.data_dir):
            mkdir(self.data_dir)

        # main sqlite3 database
        if not isfile(self.database_path):
            info("local database not found, creating")
            self._create_tables()

    def _create_tables(self):
        _tables = ["CREATE TABLE contants (name VARCHAR NOT NULL, value VARCHAR)"]

        with click.progressbar(
            _tables, label="Creating tables", length=len(_tables)
        ) as tables:
            for table in tables:
                _query(self.database_path, table)
