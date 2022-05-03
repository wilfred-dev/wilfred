Development & Ops
=================

.. note::
    This is mostly used as a reference for the core project team.


Working with Wilfred locally
----------------------------

Make sure you have `pipenv <https://github.com/pypa/pipenv>`__ installed and that you have cloned the repository to your computer (perhaps created a fork).

At the root of the project, enter the `shell` for the development environment.

.. code-block:: bash

    pipenv shell

This will create the environment. Then you need to install the dependencies.

.. code-block:: bash

    pipenv install
    pipenv install --dev

Instead of using `wilfred <command>` to run Wilfred, you can use the built-in run script.

.. code-block:: bash

    ./run.py <command>

In this way, you can develop and see your changes instantly.

Publishing a release
--------------------

Update the version in `wilfred/version.py` and `docs/source/conf.py` accordingly.

Set the version name and release status of this release in `CHANGELOG.md` to `released on YYYY-MM-DD`.

Commit the changes.

Tag the release on GitHub. Include all the changes from `CHANGELOG.md` in the release notes (you can use a previous release as reference).

GitHub Actions should automatically build and release the `PyPI package <https://pypi.org/project/wilfred/>`__.

Revert the changes in `wilfred/version.py` and commit the changes (should therefore not be included in the release).

Windows
-------

You have to install `pypiwin32` to develop on Windows.

.. code-block:: bash

    pipenv shell
    pip install pypiwin32

This is not ideal, but due to a bug in Pipenv we cannot put the `pypiwin32` package as a platform specific dependency in the `Pipfile`.

Versioning convention
---------------------

Wilfred releases should use the `semantic versioning convention <https://semver.org/>`__ (i.e. `MAJOR.MINOR.PATCH`).
