# Development & Ops

!!! note
    This is mostly used as a reference for the core project team.

## Publishing a release

Update the version in `wilfred/version.py` and `snap/snapcraft.yml` accordingly.

Set the version name and release status of this release in `CHANGELOG.md` to `released on YYYY-MM-DD`.

Commit the changes.

Tag the release on GitHub. Include all the changes from `CHANGELOG.md` in the release notes (you can use a previous release as reference).

Travis should automatically build and release the [PyPI package](https://pypi.org/project/wilfred/), and snapcraft should also build and release the snap package automatically.

After the [snap build](https://build.snapcraft.io/user/wilfred-dev/wilfred) has finished, go to the [Snap](https://snapcraft.io/wilfred) listing and push the `edge` channel to `stable` or `beta` depending on the type of release.

Revert the changes in `wilfred/version.py` and commit the changes (should therefore not be included in the release).

## Versioning convention

Wilfred releases should use the [semantic versioning convention](https://semver.org/) (i.e. `MAJOR.MINOR.PATCH`).
