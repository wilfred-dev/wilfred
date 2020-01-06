# Wilfred

[![Build Status](https://travis-ci.com/wilfred-dev/wilfred.svg?branch=master)](https://travis-ci.com/wilfred-dev/wilfred)
[![Python Versions](https://img.shields.io/pypi/pyversions/wilfred)](https://pypi.org/project/wilfred)
[![pypi](https://img.shields.io/pypi/v/wilfred)](https://pypi.org/project/wilfred)
[![wilfred](https://snapcraft.io//wilfred/badge.svg)](https://snapcraft.io/wilfred)
[![Snap Status](https://build.snapcraft.io/badge/wilfred-dev/wilfred.svg)](https://build.snapcraft.io/user/wilfred-dev/wilfred)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/wilfred-dev/wilfred.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/wilfred-dev/wilfred/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/wilfred-dev/wilfred.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/wilfred-dev/wilfred/alerts/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Wilfred is a command-line interface for running game servers locally. It uses Docker to run game servers in containers, which means they are completely separated. Wilfred can run any game that can run in Docker.

⚠️ Wilfred is currently under development and should not be considered stable. Features may brake or may not be implemented yet. Use with caution.

## Supported games

As long as your server can run in Docker, it can probably run using Wilfred (after some tinkering). These are the games supported by default. You can submit new games to [wilfred-dev/images](https://github.com/wilfred-dev/images).

- Minecraft
  - Vanilla Minecraft
  - BungeeCord
  - Paper
  - Waterfall

## Installation

Please refer to the [official documentation](https://wilfred.readthedocs.io/en/latest/installation/) for further installation instructions and documentation.

### Quickstart

Wilfred can be installed using `pip`. You need to use **Python 3.6** or newer in order for Wilfred to work.

```bash
pip install wilfred --upgrade
```

You can also install Wilfred using snap.

```bash
snap install wilfred --classic
```

Once you got it installed, run `wilfred setup` in order to set a path for Wilfred to use to store server files.

## Contributing

Feel free to send a pull request or open an issue.
