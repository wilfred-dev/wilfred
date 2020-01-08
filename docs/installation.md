# Prerequisites

Before installing Wilfred, make sure you already have [Docker](https://docs.docker.com/install/) installed on your system.

You can verify that Docker is installed using `docker --version` or `docker info` (`info` shows more information).

```bash
user@host:~$ docker --version
Docker version XX.XX.X, build XXXXXXXXXX
```

If you're having trouble accessing the Docker CLI as an non-root user, you can [add yourself to the Docker group](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user).

# Pip

Wilfred can be installed using `pip`. You need to use **Python 3.6** or newer in order for Wilfred to work.

```bash
pip install wilfred --upgrade --user
```

You can install using a specific python versions, e.g. `3.8`.

```bash
python3.8 -m pip install wilfred --upgrade
```

# Snap

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/wilfred)

The snap package is not yet considered stable.

Snapcraft is configured to automatically build the latest commit and push it to the `edge` release branch. These releases can be installed using snap.

```bash
snap install wilfred --edge --classic
```

The `--edge` release should **not** be used in a production environment.

!!! note
    The `--classic` flag is required in order for Wilfred to work. This is because Wilfred speaks to the Docker unix socket directly (`classic` confinement means no snap isolation).

# Basic configuration

Once you got Wilfred installed, you can run the setup command in order to create the basic configuration.

```bash
wilfred setup
```

Currently, the only config option required is the path for soring data.

```text
Path for storing server data [/home/{{ username }}/wilfred/servers]:
```

By default, this is `/home/{{ username }}/wilfred/servers`. You can use any path as long as you have permissions to access it as the current user.

To create a new server, you can run `wilfred create` and follow the instructions.

# Upgrading

If you installed Wilfred using `pip`, then you can upgrade by running the same command as for installing (note the `--upgrade` flag).

If you installed Wilfred using `snap`, you can use `refresh` to download the latest version.

```bash
sudo snap refresh wilfred
```

(snap should automatically update)
