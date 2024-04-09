![PyPI](https://img.shields.io/pypi/v/cellxgene-ontology-guide?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/cellxgene-ontology-guide)
[![codecov](https://codecov.io/gh/chanzuckerberg/cellxgene-ontology-guide/graph/badge.svg?token=ceXxNPx22I)](https://codecov.io/gh/chanzuckerberg/cellxgene-ontology-guide)
![example workflow](https://github.com/chanzuckerberg/cellxgene-ontology-guide/actions/workflows/push-tests.yml/badge.svg?branch=main)

# CellxGene Ontology Guide

CellxGene Ontology Guide is a filtered and curated collection of ontological metadata from different public sources.
The primary goal is to serve the ontology needs of the [CellxGene](https://cellxgene.cziscience.com/) project and its
associated tools. An [API](./api) for querying the data is also provided.

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](https://github.com/chanzuckerberg/.github/blob/master/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [opensource@chanzuckerberg.com](mailto:opensource@chanzuckerberg.com).

## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@chanzuckerberg.com](mailto:security@chanzuckerberg.com).

## Updating to a new Cellxgene Schema Version

1. Update the [ontology_info.json](./ontology-assets/ontology_info.json) file with the new schema version
2. Leave the older versions in the file for backward compatibility. They will be deprecated and removed automatically after 6 months. That process is handled in [deprecate_previous_cellxgene_schema_versions](https://github.com/chanzuckerberg/cellxgene-ontology/blob/main/tools/ontology-builder/src/all_ontology_generator.py#L311-L311).
