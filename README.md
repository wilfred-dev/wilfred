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
  - Waterfall
  - Bedrock
- Multi Theft Auto
- Voice Servers
  - Mumble

## Installation

Please refer to the [official documentation](https://docs.wilfredproject.org/en/latest/installation/) for further installation instructions and documentation.

### Quickstart

Wilfred can be installed using `pip`. You need to use **Python 3.6** or newer to run Wilfred.

```bash
pip install wilfred --upgrade --user
```

A [snap](https://snapcraft.io/wilfred) package is also in the works but currently not considered stable.

Once you got Wilfred installed, run `wilfred setup` to set a path for Wilfred to use to store server files.

## Contributing

The best places to contribute are through the issue tracker and the official Discord server. For code contributions, pull requests and patches are always welcome!

## Credits

Created, written and maintained by [Vilhelm Prytz](https://github.com/VilhelmPrytz).
