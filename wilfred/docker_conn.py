# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import docker


def docker_client(base_url=None):
    """returns client object used for Docker socket communication

    :param str base_url: Base URL for Docker socket. Uses env if None."""

    client = docker.DockerClient(base_url=base_url) if base_url else docker.from_env()

    return client
