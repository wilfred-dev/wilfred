# CHANGELOG

Please refer to the [official documentation](https://docs.wilfredproject.org/en/latest/development.html) for more information about the CHANGELOG and releases.

## v0.8.0 (released on 2020-12-19)

* **Added** [#92](https://github.com/wilfred-dev/wilfred/issues/92) Added new commit check on `--version`. If running the HEAD version of the brew package or the edge channel of the snap package, `wilfred --version` will now check for new commits-
* **Added** [#74](https://github.com/wilfred-dev/wilfred/issues/74) Added the ability for Wilfred to automatically refresh the default images periodically. Wilfred will currently initiate refresh if images on file are older than 1 week or if the running version of Wilfred changes.
* **Added** [#86](https://github.com/wilfred-dev/wilfred/issues/86) Added the ability to specify repo and branch as image source when running `wilfred images --refresh`. The new options are `--repo` (which by default has the value `wilfred-dev/images` and `--branch` (which by default has the value `master`).
* **Fixed** [#87](https://github.com/wilfred-dev/wilfred/issues/87) Fixed so that `wilfred delete` no longer gracefully stops the container before deletion and instead kills the container (`container.kill()`). The use of `container.stop()` was not intended. This change will lead to faster server deletion.
* **Fixed** [#84](https://github.com/wilfred-dev/wilfred/issues/84) Fixed a bug that would cause Wilfred to display a long traceback when `docker_client()` function raised exception (such as `DockerException` which is raised when Docker is not installed/broken)

## v0.7.1 (released on 2020-06-19)

* **Fixed** [#57](https://github.com/wilfred-dev/wilfred/issues/57) Fixed a bug that caused `wilfred top` to crash when the installation finishes and the server starts (refactored underlying API).
* **Fixed** [#58](https://github.com/wilfred-dev/wilfred/issues/58) Fixed a bug that caused all server statuses to show up as `stoppped`. `running`, `installing` and `stopped` are now properly displayed and detected (refactored underlying API, related to [#57]((https://github.com/wilfred-dev/wilfred/issues/57))).

## v0.7.0 (released on 2020-06-17)

* **Changed** [#56](https://github.com/wilfred-dev/wilfred/issues/56)/[#43](https://github.com/wilfred-dev/wilfred/issues/43) Name of server folders now include both the unique ID and the name of the server (easier to find the server folder).

## v0.6.1 (released on 2020-05-03)

* **Fixed** [#54](https://github.com/wilfred-dev/wilfred/issues/54) Hopefully fixed broken PyPI deployment with Travis CI.
* **Fixed** [#55](https://github.com/wilfred-dev/wilfred/issues/55) Fixed so that Docker exceptions reveal more info when installing by raising the Docker exceptions directly to the CLI.
* **Changed** Replaced mkdocs documentation with Sphinx (and initial API autodoc).

## v0.6.0 (released on 2020-04-10)

* **Added** [#47](https://github.com/wilfred-dev/wilfred/issues/47) Added `--force`/`-f` flags to `wilfred kill` and `wilfred delete` (forces actions without confirmation).
* **Added** [#50](https://github.com/wilfred-dev/wilfred/issues/50) Added ability to reset back to default startup command (remove custom startup command).
* **Changed** Enforce 20 character length limit on server names.
* **Changed** [#42](https://github.com/wilfred-dev/wilfred/issues/42) Major refactor, separate the CLI from the core API and rewrite some of the core methods to be more consistent. With this, the Wilfred API now has it's own set of exceptions that it raise. The exceptions are no longer caught within the methods themselves and instead within the UI (a lot more predictable and makes a lot more sense).
* **Fixed** [#49](https://github.com/wilfred-dev/wilfred/issues/49) Fixed a bug that caused Wilfred to crash if a container stopped running between the statement that checks if the server is running and the statement that actually retrieves the log in `wilfred console`.

## v0.5.1 (released on 2020-03-21)

* **Added** Added project URLs to `setup.py`.
* **Changed** Disabled terminal emojis on Windows (PowerShell and cmd have poor support for emojis).
* **Fixed** [#46](https://github.com/wilfred-dev/wilfred/issues/46) Fixed a bug that caused Wilfred to crash if attaching to the server console during installation.

## v0.5.0 (released on 2020-03-20)

* **Added** [#12](https://github.com/wilfred-dev/wilfred/issues/12) Added support for Windows.
* **Added** Added new unit tests.
* **Added** Print snap revision if Wilfred is installed via snap.
* **Changed** Replaced [yaspin](https://pypi.org/project/yaspin/) with [halo](https://pypi.org/project/halo/) for terminal spinners (mostly because yaspin does not support Windows).
* **Changed** Updated copyright headers.

## v0.4.2 (released on 2020-02-16)

* **Fixed** [#41](https://github.com/wilfred-dev/wilfred/issues/41) Fixed a critical bug that caused servers with config settings linked to environment variables not to start.

## v0.4.1 (released on 2020-02-10)

* **Fixed** [#37](https://github.com/wilfred-dev/wilfred/issues/37) Fixed so that the commit hash and build date are correctly displayed on `wilfred --version` for pip installations (error in Travis CI config).

## v0.4.0 (released on 2020-02-10)

* **Added** [#21](https://github.com/wilfred-dev/wilfred/issues/21) Added `wilfred config`, ability to edit server configuration files. Exposes the server configuration to Wilfred. Currently supporting `.properties` and read-only `.yml` and `.json`.
* **Added** Added image API version 2, introduces configuration files.
* **Added** [#23](https://github.com/wilfred-dev/wilfred/issues/23) Added `wilfred top`, server statistics that fill the screen and updates in real-time (like `top`).
* **Changed** [#30](https://github.com/wilfred-dev/wilfred/issues/30) Releases are now built with the git commit hash saved as a variable (including versions pushed to the Snap edge channel). `wilfred --version` displays the commit hash accordingly.
* **Changed** Removed unnecessary `python3-distutils` and `build-essential` from `stage-packages` within the Snapcraft configuration (see [this comment](https://github.com/wilfred-dev/wilfred/issues/30#issuecomment-581396779)). 53 MB decrease in package size.
* **Fixed** [#17](https://github.com/wilfred-dev/wilfred/issues/17) Changing port using `wilfred edit` should be able to trigger configuration update on supported filetypes (this is closely related to image API v2 and [#21](https://github.com/wilfred-dev/wilfred/issues/21)).
* **Fixed** [#28](https://github.com/wilfred-dev/wilfred/issues/28) SQLAlchemy exceptions no longer occur when trying to delete a server that has no environment variables.
* **Fixed** [#31](https://github.com/wilfred-dev/wilfred/issues/31) Config settings that are linked to an environment variable are no longer editable using `wilfred config`.

## v0.3.0 (released on 2020-01-25)

* **Added** Added check for new releases against GitHub when running `wilfred --version`.
* **Added** Added check so that it is now required for all images UID's to be lowercase.
* **Changed** Refactor: more clean way of searching for images internally (improved the `image.get_image` function using `next`).

## v0.2.0 (released on 2020-01-18)

* **Added** [#14](https://github.com/wilfred-dev/wilfred/issues/14) Added ability to restart servers using `wilfred restart <name>`.
* **Added** [#15](https://github.com/wilfred-dev/wilfred/issues/15) Added ability to send a single command to STDIN of the server without attaching to the server console.
* **Changed** [#16](https://github.com/wilfred-dev/wilfred/issues/16) Changed database management (major rewrite), use SQLAlchemy instead of raw SQL queries everywhere
* **Fixed** Empty environment variables in startup commands are now correctly replaced (bug).

## v0.1.1 (released on 2020-01-11)

* **Changed** [#11](https://github.com/wilfred-dev/wilfred/issues/11) Build `wheel` package along with standard `sdist` on Travis CI PyPI deployment.
* **Changed** Update help texts.
* **Fixed** Only perform Travis CI PyPI deployment once, an error in the config caused the CI to deploy twice during the `v0.1.0` release.
* **Fixed** [#10](https://github.com/wilfred-dev/wilfred/issues/10) Truncate custom startup commands, too long commands no longer break table styling.

## v0.1.0 (released on 2020-01-11)

* Initial release
