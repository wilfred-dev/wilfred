# Development & Ops

!!! note
    This is mostly used as reference for the core project team.

## Publishing a release

Update the version in `wilfred/version.py`  accordingly (`snap/snapcraft.yml` should automatically use the Git tag).

Set the version name and release status of this release in `CHANGELOG.md` to `released on YYYY-MM-DD`.

Commit the changes.

Tag the release on GitHub. Include all the changes from `CHANGELOG.md` in the release notes.

Travis should automatically build and release the pypi package, and snapcraft should also build and release the snap package automatically.

Revert the changes in `wilfred/version.py` and commit the changes (should therefore not be included in the release).

## Versioning convention

Wilfred releases should use the [semantic versioning convention](https://semver.org/) (i.e. `MAJOR.MINOR.PATCH`).
