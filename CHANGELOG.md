# CHANGELOG

Please refer to the [official documentation](https://wilfred.readthedocs.io/en/latest/development/) for more information about the CHANGELOG and releases.

## v0.1.1 (released on 2020-01-11)

### Enhancements

* [#11](https://github.com/wilfred-dev/wilfred/issues/11) Build `wheel` package along with standard `sdist` on Travis CI pypi deployment.
* Update help texts.

### Bugs

* Only perform Travis CI `pypi` deployment once, an error in the config caused the CI to deploy twice during the `v0.1.0` release.
* [#10](https://github.com/wilfred-dev/wilfred/issues/10) Truncate custom startup commands, too long commands do no longer break table styling.

## v0.1.0 (released on 2020-01-11)

* Initial release
