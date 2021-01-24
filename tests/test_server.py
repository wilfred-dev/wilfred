#################################################################
#                                                               #
# Wilfred                                                       #
# Copyright (C) 2020-2021, Vilhelm Prytz, <vilhelm@prytznet.se> #
#                                                               #
# Licensed under the terms of the MIT license, see LICENSE.     #
# https://github.com/wilfred-dev/wilfred                        #
#                                                               #
#################################################################

from pathlib import Path

from wilfred.api.images import Images
from wilfred.api.servers import Servers
from wilfred.docker_conn import docker_client
from wilfred.api.server_config import ServerConfig
from wilfred.database import Server, EnvironmentVariable, session
from wilfred.api.config_parser import Config

config = Config()
config.write(f"{str(Path.home())}/wilfred-data/servers")
config.read()

images = Images()

if not images.check_if_present():
    images.download()

images.read_images()

servers = Servers(docker_client(), config.configuration, images)


def test_create_server():
    # create
    server = Server(
        id="test",
        name="test",
        image_uid="minecraft-paper",
        memory="1024",
        port="25565",
        custom_startup=None,
        status="installing",
    )
    session.add(server)
    session.commit()

    minecraft_version = EnvironmentVariable(
        server_id=server.id, variable="MINECRAFT_VERSION", value="latest"
    )

    eula_acceptance = EnvironmentVariable(
        server_id=server.id, variable="EULA_ACCEPTANCE", value="true"
    )

    session.add(minecraft_version)
    session.add(eula_acceptance)
    session.commit()

    servers.install(server, skip_wait=False)
    servers.sync()


def test_start_server():
    server = session.query(Server).filter_by(id="test").first()

    if server.status == "installing":
        raise Exception("server is installing")

    servers.set_status(server, "running")
    servers.sync()


def test_pseudo_config_write():
    server = session.query(Server).filter_by(id="test").first()

    image = images.get_image(server.image_uid)

    Path(f"{str(Path.home())}/temp/test_test").mkdir(parents=True, exist_ok=True)

    with open(f"{str(Path.home())}/temp/test_test/server.properties", "w") as f:
        f.write("\n".join(("query.port=25564", "server-port=25564")))

    ServerConfig(
        {"data_path": f"{str(Path.home())}/temp"}, servers, server, image
    ).write_environment_variables()


def test_delete_server():
    server = session.query(Server).filter_by(id="test").first()
    servers.remove(server)
