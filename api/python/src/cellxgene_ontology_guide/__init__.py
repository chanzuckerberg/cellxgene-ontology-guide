"""
[![PyPI](https://img.shields.io/pypi/v/cellxgene-ontology-guide?label=pypi%20package)](https://pypi.org/project/cellxgene-ontology-guide/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cellxgene-ontology-guide)](<(https://pypi.org/project/cellxgene-ontology-guide/)>)
[![codecov](https://codecov.io/gh/chanzuckerberg/cellxgene-ontology-guide/graph/badge.svg?token=ceXxNPx22I)](https://codecov.io/gh/chanzuckerberg/cellxgene-ontology-guide)
![example workflow](https://github.com/chanzuckerberg/cellxgene-ontology-guide/actions/workflows/push-tests.yml/badge.svg?branch=main)
[![GitHub](https://img.shields.io/github/license/chanzuckerberg/cellxgene-ontology-guide)](./LICENSE)

# cellxgene-ontology-guide
A Python package to help with ontology term mapping in for projects in the [cellxgene](https://cellxgene.cziscience.com/) ecosystem.

## Installation
```bash
pip install cellxgene-ontology-guide
```
## Notebooks
Notebooks on how to use the ontology guide can be found in the
[notebooks directory](https://github.com/chanzuckerberg/cellxgene-ontology-guide/tree/main/api/python/notebooks) of the
repository.
.. include:: ../../CHANGELOG.md
"""

__version__ = "1.2.0"
__all__ = ["curated_ontology_term_lists", "entities", "ontology_parser", "supported_versions"]
