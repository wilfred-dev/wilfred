# CHANGELOG

Please refer to the [official documentation](https://wilfred.readthedocs.io/en/latest/development/) for more information about the CHANGELOG and releases.

## v0.3.0 (released on 2020-01-25)

### Added

* Added check for new releases against GitHub when running `wilfred --version`.
* Added check so that it is now required for all images UID's to be lowercase.

### Changed

* Refactor: more clean way of searching for images internally (improved the `image.get_image` function using `next`).

## v0.2.0 (released on 2020-01-18)

### Added

* [#14](https://github.com/wilfred-dev/wilfred/issues/14) Added ability to restart servers using `wilfred restart <name>`.
* [#15](https://github.com/wilfred-dev/wilfred/issues/15) Added ability to send a single command to STDIN of the server without attaching to the server console.

### Changed

* [#16](https://github.com/wilfred-dev/wilfred/issues/16) Changed database management (major rewrite), use SQLAlchemy instead of raw SQL queries everywhere

### Fixed

* Empty environment variables in startup commands are now correctly replaced (bug).

## v0.1.1 (released on 2020-01-11)

### Changed

* [#11](https://github.com/wilfred-dev/wilfred/issues/11) Build `wheel` package along with standard `sdist` on Travis CI PyPI deployment.
* Update help texts.

### Fixed

* Only perform Travis CI PyPI deployment once, an error in the config caused the CI to deploy twice during the `v0.1.0` release.
* [#10](https://github.com/wilfred-dev/wilfred/issues/10) Truncate custom startup commands, too long commands no longer break table styling.

## v0.1.0 (released on 2020-01-11)

* Initial release
