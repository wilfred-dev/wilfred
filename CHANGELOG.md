# CHANGELOG

Please refer to the [official documentation](https://docs.wilfredproject.org/en/latest/development/) for more information about the CHANGELOG and releases.

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
