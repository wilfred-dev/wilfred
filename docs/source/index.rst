.. Wilfred documentation master file, created by
   sphinx-quickstart on Sat May  2 21:42:47 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Wilfred
===================================

Wilfred is a command-line interface for running and managing game servers locally. It uses Docker to run game servers in containers, which means they are completely separated. Wilfred can run any game that can run in Docker.


.. warning::

   The documentation has just been migrated to Sphinx. It's currently being updated and things may change at any time. We're also preparing for the Wilfred API to be documented here.

Installation
------------

Prerequisites
^^^^^^^^^^^^^

Wilfred currently supports Linux (should be everywhere where Python and Docker is supported), MacOS and now Windows.

Before installing, make sure you have Docker already installed and configured. You can install it from the links below.

* `Docker on Linux <https://docs.docker.com/install/>`__
* `Docker Desktop on MacOS <https://docs.docker.com/docker-for-mac/install/>`__
* `Docker Desktop on Windows <https://docs.docker.com/docker-for-windows/install/>`__

You can verify that Docker is installed using ``docker --version`` or ``docker info`` (``info`` shows more information).

.. code-block:: bash

   user@host:~$ docker --version
   Docker version XX.XX.X, build XXXXXXXXXX

If you're having trouble accessing the Docker CLI as a non-root user, you can `add yourself to the Docker group <https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user>`__.

Homebrew
^^^^^^^^

The recommended way of installing Wilfred is via `Homebrew <https://brew.sh>`__ (works on macOS and Linux). Make sure you have it installed on your system. Once Homebrew is installed, use the two commands below to install Wilfred via the offical tap.

.. code-block:: bash

   brew tap wilfred-dev/wilfred
   brew install wilfred

Want the bleeding edge? You can install the latest commit using ``--HEAD`` (bugs are to be expected, don't use in production environments!).

.. code-block:: bash

   brew tap wilfred-dev/wilfred
   brew install --HEAD wilfred

Pip
^^^

Wilfred can be installed using ``pip``. You need to use **Python 3.6** or newer to run Wilfred (if you also have ``pip2`` on your system, run with ``pip3``).

.. code-block:: bash

   pip install wilfred --upgrade

You can install using a specific python version, e.g. `3.8`.

.. code-block:: bash

   python3.8 -m pip install wilfred --upgrade

Snap (experimental)
^^^^^^^^^^^^^^^^^^^

.. warning::
   The snap package is not considered stable. You can only install it using the `--devmode` which is not recommended in a production environment. For now, please use the pip package. See issue `#6 <https://github.com/wilfred-dev/wilfred/issues/6>`__ for updates regarding the snap package.

|snapbadge|_

.. |snapbadge| image:: https://snapcraft.io/static/images/badges/en/snap-store-black.svg
.. _snapbadge: https://snapcraft.io/wilfred

Snapcraft is configured to automatically build the latest commit and push it to the `edge` release branch. These releases can be installed using snap. Currently, the same releases pushed to Pip are also pushed to the `beta` branch.

.. code-block:: bash

   snap install wilfred --beta --devmode

Again, the ``--beta`` channel and ``--devmode`` should **not** be used in a production environment.

Basic Configuration
-------------------

Once you got Wilfred installed, you can run the setup command to create the basic configuration.

.. code-block:: bash

   wilfred setup

Currently, the only config option required is the path for soring data.

.. code-block:: text

   Path for storing server data [/home/{{ username }}/wilfred-data/servers]:

By default, this is ``/home/{{ username }}/wilfred-data/servers``. You can use any path as long as you have permissions to access it as the current user.

To create a new server, you can run ``wilfred create`` and follow the instructions.

Upgrading
---------

To check if you're running the latest version, run ``wilfred --version``. If a new version is available, Wilfred will print a message.

If you installed Wilfred using ``pip``, then you can upgrade by running the same command as for installing (note the ``--upgrade`` flag).

.. code-block:: bash

   pip install wilfred --upgrade

If you installed Wilfred using ``snap``, you can use ``refresh`` to download the latest version (snap should automatically update).

.. code-block:: bash

   snap refresh wilfred

If you installed Wilfred using ``brew``, you can use Homebrew to upgrade Wilfred as you would do with any formula.

.. code-block:: bash

   brew update
   brew upgrade

.. toctree::
   :maxdepth: 3
   :hidden:

   commands
   images
   api
   development

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
