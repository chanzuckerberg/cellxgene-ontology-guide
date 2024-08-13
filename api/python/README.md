# Python API

API Documentation: https://chanzuckerberg.github.io/cellxgene-ontology-guide/cellxgene_ontology_guide.html

pypi: https://pypi.org/project/cellxgene-ontology-guide/

# Developer Setup

## Install

```bash
make install
```

## Uninstall

```bash
make uninstall
```

## Run Unit Tests

```bash
make install-dev
make unit-tests
```

## Release Process

A new version of the PyPi package will be released for the following reasons (not an exhaustive list):

- A new version will be created when functionality is added, changed, or removed.
- A new version of the API will likely be needed if the shape of the ontology asset release changes.
- A new version will be created when cellxgene schema change to reflect its compatibility with the new version of the CellxGene schema.
- A new version will be created when any of the ontology versions associated with a [cellxgene-schema](https://github.com/chanzuckerberg/single-cell-curation/tree/main/schema) definition changes.

To release a new version of API, merge a pull request to main. Release-please will automatically create a PR with the a version bump if needed. Merging the release-please PR will create a new release in github and a new version will be uploaded to pypi. If no changes were made that affect the API, the API will not be release. Closing the PR will skip the release of these changes and they will be included in the next release.

If the version number needs to be change see [release-please documentation](https://github.com/googleapis/release-please?tab=readme-ov-file#how-do-i-change-the-version-number) for how to change the version number. This same process can be used to manually release the package.

## Local Manual Release

The [release.yml](../../.github/workflows/release.yml) GHA should handle the release process for the pypi package. In the event release-please has stopped working and a release is required a manual release of the pypi package can be performed by running the following:

```bash
make build
make release/pypi
```

The file [ontology-assets-version.json](./ontology-assets-version.json) will be automatically updated with a new version number whenever new ontology-assets are released. This will trigger a new release of the pypi package with the new ontology-assets.
