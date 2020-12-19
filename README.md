# Wilfred

[![Build Status](https://travis-ci.com/wilfred-dev/wilfred.svg?branch=master)](https://travis-ci.com/wilfred-dev/wilfred)
[![Python Versions](https://img.shields.io/pypi/pyversions/wilfred)](https://pypi.org/project/wilfred)
[![pypi](https://img.shields.io/pypi/v/wilfred)](https://pypi.org/project/wilfred)
[![wilfred](https://snapcraft.io//wilfred/badge.svg)](https://snapcraft.io/wilfred)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/wilfred-dev/wilfred.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/wilfred-dev/wilfred/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/wilfred-dev/wilfred.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/wilfred-dev/wilfred/alerts/)
[![Downloads](https://pepy.tech/badge/wilfred)](https://pepy.tech/project/wilfred)
[![Discord](https://img.shields.io/discord/666366973072113698?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://wilfredproject.org/discord)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Wilfred is a command-line interface for running and managing game servers locally. It uses Docker to run game servers in containers, which means they are completely separated. Wilfred can run any game that can run in Docker.

⚠️ Wilfred is currently under development and should not be considered stable. Features may break or may not be implemented yet. Use with caution.

## Documentation

The official documentation is available [here](https://docs.wilfredproject.org/en/latest/). For support, use our [Discord Chat](https://wilfredproject.org/discord). For bugs, you can open an issue [here](https://github.com/wilfred-dev/wilfred/issues).

## Supported games

As long as your server can run in Docker, it can probably run using Wilfred (after some tinkering). These are the games supported by default. You can submit new games to [wilfred-dev/images](https://github.com/wilfred-dev/images).

- Minecraft
  - Vanilla Minecraft
  - BungeeCord
  - Paper
  - Spigot
  - Waterfall
  - Bedrock
- Multi Theft Auto
- Voice Servers
  - Mumble

## Installation

Please refer to the [official documentation](https://docs.wilfredproject.org/en/latest/#installation) for further installation instructions and documentation.

### Quickstart

Make sure you have Docker installed (see the official documentation for more info). The recommended way of installing Wilfred is via [Homebrew](https://brew.sh). Once brew is installed, Wilfred can easily be installed from the official tap.

```bash
brew tap wilfred-dev/wilfred
brew install wilfred
```

Want the bleeding edge? You can install the latest commit using ``--HEAD`` (bugs are to be expected, don't use in production environments!).

```bash
brew tap wilfred-dev/wilfred
brew install --HEAD wilfred
```

Wilfred can also be installed using `pip`. You need to use **Python 3.6** or newer to run Wilfred.

```bash
pip install wilfred --upgrade
```

A [snap](https://snapcraft.io/wilfred) package is also in the works but is currently not considered stable.

Once you got Wilfred installed, run `wilfred setup` to set a path for Wilfred to use to store server files.

![Creating a server in Wilfred](https://raw.githubusercontent.com/wilfred-dev/wilfred/master/docs/quickstart.gif)

To create your first server, use `wilfred create`. Most values have a default value, where you can just press return to use them.

Wilfred will ask you which "image" to use. An image is a set of configuration files that defines a specific game within Wilfred. These images are not to be confused with Docker images, Wilfred images sort of wrap around the Docker images. A couple of games are already built into Wilfred, but you can also create your own.

Then, Wilfred will ask you to set any environment variables (if available for that image). The environment variables differ from game to game and most of them have a default value.

Once the server is created, you can use `wilfred servers` to list available servers. To start it, use `wilfred start <name>`. To attach to the server console, you can use `wilfred console <name>`. If you want to start the server and attach to the server console in a single command, you can use `wilfred start <name> --console` (it will start the server and then immediately attach to the server console).

## Helping

The best places to contribute are through the issue tracker and the official Discord server. For code contributions, pull requests and patches are always welcome!

## Contributors ✨

Created, written, and maintained by [Vilhelm Prytz](https://github.com/vilhelmprytz).
