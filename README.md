![PyPI](https://img.shields.io/pypi/v/cellxgene-ontology-guide?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/cellxgene-ontology-guide)
[![codecov](https://codecov.io/gh/chanzuckerberg/cellxgene-ontology-guide/graph/badge.svg?token=ceXxNPx22I)](https://codecov.io/gh/chanzuckerberg/cellxgene-ontology-guide)
![example workflow](https://github.com/chanzuckerberg/cellxgene-ontology-guide/actions/workflows/push-tests.yml/badge.svg?branch=main)
![GitHub](https://img.shields.io/github/license/chanzuckerberg/cellxgene-ontology-guide)

# CellxGene Ontology Guide

CellxGene Ontology Guide is a filtered and curated collection of ontological metadata from different public sources.
The primary goal is to serve the ontology needs of the [CellxGene](https://cellxgene.cziscience.com/) project and its
associated tools. An [API](./api/python) for querying the data is also provided.

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](https://github.com/chanzuckerberg/.github/blob/master/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [opensource@chanzuckerberg.com](mailto:opensource@chanzuckerberg.com).

## Release Please

[Release-please]() is used to manage the release process for this repository. To make changes to how releases are
managed, update [.release-please.yml](./release-please-config.json). [This GHA workflow](.github/workflows/release.
yml) performs the release.

For instruction on how to release the different components of this repository, see the following:

- [API](./api/python/README.md#release-process)
- [Ontology Assets](./README.md#release-process)
- [Descendant Mappings](./README.md#descendant-mappings-tag)

# Components

## Ontology Assets

The [ontology-assets](./ontology-assets) directory contains static ontology assets that are used by CellxGene
project. The jsonschema for these assets are stored in [asset-schemas](./asset-schemas).

This is a description of the files within the [ontology-assets](./ontology-assets) directory:

- [ontology_info.json](./ontology-assets/ontology_info.json) contains the ontology versions used by the current and deprecated [cellxgene-schema](https://github.com/chanzuckerberg/single-cell-curation/tree/main/schema)
- The `*.json.gz` files are filtered version of ontology sources found in [ontology_info.json](./ontology-assets/ontology_info.json). They are generated using the GHA workflow [generate_all_ontology.yml](.github/workflows/generate_all_ontology.yml) and the [all_ontology_generator.py](./tools/ontology-builder/src/all_ontology_generator.py) script.
- The `*_list.json` files are manually curated and are used to filter the ontologies.
- The `*_descendants.json` are descendant mapping files. They are generated on a weekly bases using the GHA workflow [generate_descendant_mappings.yml](./.github/workflows/generate_descendant_mappings.yml) and the [generate_descendant_mappings.py](./scripts/generate_descendant_mappings.py) script.

### Deprecating Ontologies

Older version of cellxgene-schema will be fully deprecated after 6 months of the release of a new version.

[TODO: document the process for deprecating ontologies](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/170)

### Descendant Mappings

The `latest` tag is use to idenitfy the latest version of the descendant mappings for downsteam consumers to use. To retrieve the latest version of the descendant mappings, use the following urls:

- tissue - `https://github.com/chanzuckerberg/cellxgene-ontology-guide/blob/latest/ontology-assets/tissue_descendants.json`
- cell type - `https://github.com/chanzuckerberg/cellxgene-ontology-guide/blob/latest/ontology-assets/cell_type_descendants.json`

### Release Process

Each release will be tagged and versioned within a GitHub Release using the SemVer Versioning schema. The format of the version will be MAJOR.MINOR.PATCH, where MAJOR and MINOR indicate the compatibility of the change. A new version will be released for the following reasons(not an exhaustive list):

- A Patch version will be created whenever the source ontology files are updated.
- A Minor version will be created whenever new fields or files are added to the precomputed ontology files.
- A Major version will be created when fields or files are removed from the precomputed ontology files.
- A version update will be created if a fix is required related to how the files are computed. This would likely be a Major or Minor update.

To release a new version of the ontology assets, merge a pull request to main. Release-please will automatically create a PR with the a version bump if needed. Merging the release-please PR will create a new release in github with a tagged version. Releasing the ontology assets will also result in a release of the python API. Closing the PR will skip the release of these changes and they will be included in the next release.

#### Descendant Mappings Tag

The GHA workflow [tag-latest-ontology-assets.yml](.github/workflows/tag-latest-ontology-assets.yml) will automatically update the `latest` tag when the appropriate.
