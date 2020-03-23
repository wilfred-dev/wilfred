####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

from wilfred.images import Images
from wilfred.servers import Servers
from wilfred.docker_conn import docker_client
from wilfred.server_config import ServerConfig
from wilfred.database import Server, EnvironmentVariable, session


configuration = {"data_path": "/tmp/wilred/servers"}
images = Images()
servers = Servers(docker_client(), configuration, images)


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

    image = images.get_image(server.image_uid)

    ServerConfig(configuration, servers, server, image).write_environment_variables()

    servers.set_status(server, "running")
    servers.sync()


def test_delete_server():
    server = session.query(Server).filter_by(id="test").first()
    servers.remove(server)
