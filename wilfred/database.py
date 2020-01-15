# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

# import sqlite3
# import click

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from appdirs import user_data_dir

# from os.path import isfile, isdir
# from pathlib import Path

# from wilfred.message_handler import info, error

engine = create_engine(
    f"sqlite:///{user_data_dir()}/wilfred/test_wilfred.db", echo=True
)
Base = declarative_base()


class Server(Base):
    __tablename__ = "servers"

    id = Column(String, primary_key=True, unique=True)
    name = Column(String)
    image_uid = Column(String)
    memory = Column(Integer)
    port = Column(Integer)
    custom_startup = Column(String)
    status = Column(String)

    environment_variables = relationship("EnvironmentVariable")

    def __repr__(self):
        return f"<Server(id='{self.id}', name='{self.name}', image_uid='{self.image_uid}', port='{self.port}')>"


class EnvironmentVariable(Base):
    __tablename__ = "environment_variables"

    server_id = Column(String, ForeignKey("servers.id"))
    variable = Column(String)
    value = Column(String)
