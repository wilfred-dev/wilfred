####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

import docker


def docker_client(base_url=None):
    """returns client object used for Docker socket communication

    :param str base_url: Base URL for Docker socket. Uses env if None."""

    client = docker.DockerClient(base_url=base_url) if base_url else docker.from_env()

    return client
