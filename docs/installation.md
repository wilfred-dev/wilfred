# Prerequisites

Wilfred currently supports Linux (should be everywhere where Python and Docker is supported), MacOS and now Windows.

Before installing, make sure you have Docker already installed and configured. You can install it from the links below.

* [Docker on Linux](https://docs.docker.com/install/)
* [Docker Desktop on MacOS](https://docs.docker.com/docker-for-mac/install/)
* [Docker Desktop on Windows](https://docs.docker.com/docker-for-windows/install/)

You can verify that Docker is installed using `docker --version` or `docker info` (`info` shows more information).

```bash
user@host:~$ docker --version
Docker version XX.XX.X, build XXXXXXXXXX
```

If you're having trouble accessing the Docker CLI as a non-root user, you can [add yourself to the Docker group](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user).

# Pip

Wilfred can be installed using `pip`. You need to use **Python 3.6** or newer to run Wilfred (if you also have `pip2` on your system, run with `pip3`).

```bash
pip install wilfred --upgrade
```

You can install using a specific python version, e.g. `3.8`.

```bash
python3.8 -m pip install wilfred --upgrade
```

# Homebrew

If you're using macOS with [Homebrew](https://brew.sh) or Linux with [Linuxbrew](https://docs.brew.sh/Homebrew-on-Linux), you can install Wilfred using the official tap.

```bash
brew tap wilfred-dev/wilfred
brew install wilfred
```

# Snap (experimental)

!!! warning
    The snap package is not considered stable. You can only install it using the `--devmode` which is not recommended in a production environment. For now, please use the pip package. See issue [#6](https://github.com/wilfred-dev/wilfred/issues/6) for updates regarding the snap package.

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/wilfred)

Snapcraft is configured to automatically build the latest commit and push it to the `edge` release branch. These releases can be installed using snap. Currently, the same releases pushed to Pip are also pushed to the `beta` branch.

```bash
snap install wilfred --beta --devmode
```

Again, the `--beta` channel and `--devmode` should **not** be used in a production environment.

# Basic configuration

Once you got Wilfred installed, you can run the setup command to create the basic configuration.

```bash
wilfred setup
```

Currently, the only config option required is the path for soring data.

```text
Path for storing server data [/home/{{ username }}/wilfred-data/servers]:
```

By default, this is `/home/{{ username }}/wilfred-data/servers`. You can use any path as long as you have permissions to access it as the current user.

To create a new server, you can run `wilfred create` and follow the instructions.

# Upgrading

To check if you're running the latest version, run `wilfred --version`. If a new version is available, Wilfred will print a message.

If you installed Wilfred using `pip`, then you can upgrade by running the same command as for installing (note the `--upgrade` flag).

```bash
pip install wilfred --upgrade
```

If you installed Wilfred using `snap`, you can use `refresh` to download the latest version (snap should automatically update).

```bash
sudo snap refresh wilfred
```

If you installed Wilfred using `brew`, you can use Homebrew to upgrade Wilfred as you would do with any formula.

```bash
brew update
brew upgrade
```
