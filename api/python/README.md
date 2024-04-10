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

## Release

The [release.yml](../../.github/workflows/release.yml) GHA should handle the release process for the pypi package.
However if you need to manually release the package, you can use the following commands:

```bash
make release/pypi
```

The file [ontology-assets-version.json](./ontology-assets-version.json) will be automatically updated with a new version number whenever new ontology-assets are released. This will trigger a new release of the pypi package with the new ontology-assets.
