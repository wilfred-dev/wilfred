# CHANGELOG

Please refer to the [official documentation](https://wilfred.readthedocs.io/en/latest/development/) for more information about the CHANGELOG and releases.

## next-release

### Added

* [#14](https://github.com/wilfred-dev/wilfred/issues/14) Added ability to restart servers using `wilfred restart <name>`.
* [#15](https://github.com/wilfred-dev/wilfred/issues/15) Added ability to send a single command to STDIN of server without attaching to server console.

## v0.1.1 (released on 2020-01-11)

### Changed

* [#11](https://github.com/wilfred-dev/wilfred/issues/11) Build `wheel` package along with standard `sdist` on Travis CI PyPI deployment.
* Update help texts.

### Fixed

* Only perform Travis CI PyPI deployment once, an error in the config caused the CI to deploy twice during the `v0.1.0` release.
* [#10](https://github.com/wilfred-dev/wilfred/issues/10) Truncate custom startup commands, too long commands no longer break table styling.

## v0.1.0 (released on 2020-01-11)

* Initial release
