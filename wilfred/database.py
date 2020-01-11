# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

import sqlite3
import click

from appdirs import user_data_dir
from os.path import isfile, isdir
from pathlib import Path

from wilfred.message_handler import info, error

API_VERSION = 1


def _query(path, query, fetchone=False):
    """
    executes specified query on sqlite3 database located at specified path

    :param str path: the path of the sqlite3 database
    :param str query: sql query to execute
    """

    result = []

    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute(query)

        if fetchone:
            result = cur.fetchone()
        else:
            for r in cur.fetchone() if fetchone else cur.fetchall():
                result.append(dict(r))

        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        error(
            "could not communicate with database " + click.style(str(e), bold=True),
            exit_code=1,
        )
    except sqlite3.IntegrityError as e:
        error("invalid input " + click.style(str(e), bold=True), exit_code=1)

    return result


class Database(object):
    def __init__(self):
        self.data_dir = f"{user_data_dir()}/wilfred"
        self.database_path = f"{self.data_dir}/wilfred.db"

        if not isdir(self.data_dir):
            Path(self.data_dir).mkdir(parents=True, exist_ok=True)

        # main sqlite3 database
        if not isfile(self.database_path):
            info("local database not found, creating")
            self._create_tables()
            self._insert_api_version()

            return
        if (
            int(
                self.query(
                    f"SELECT value FROM constants WHERE name = 'api_version'",
                    fetchone=True,
                )["value"]
            )
            != API_VERSION
        ):
            error(f"database API level differs from Wilfreds", exit_code=1)

    def _create_tables(self):
        _tables = [
            """CREATE TABLE constants (
                name VARCHAR NOT NULL UNIQUE,
                value VARCHAR,
                PRIMARY KEY (name)
            );""",
            """CREATE TABLE servers (
                id VARCHAR NOT NULL UNIQUE,
                name VARCHAR NOT NULL UNIQUE,
                image_uid VARCHAR NOT NULL,
                memory INT NOT NULL,
                port INT NOT NULL UNIQUE,
                custom_startup VARCHAR,
                status VARCHAR NOT NULL,
                PRIMARY KEY (id)
            );""",
            """CREATE TABLE variables (
                server_id VARCHAR NOT NULL,
                variable VARCHAR NOT NULL,
                value VARCHAR NOT NULL
            )""",
        ]

        with click.progressbar(
            _tables, label="Creating tables", length=len(_tables)
        ) as tables:
            for table in tables:
                _query(self.database_path, table)

    def _insert_api_version(self):
        _query(
            self.database_path,
            f"INSERT INTO constants (name, value) VALUES ('api_version', '{API_VERSION}')",
        )

    def query(self, query, *args, **kwargs):
        return _query(self.database_path, query, *args, **kwargs)
