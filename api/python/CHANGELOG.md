# Changelog

## [0.1.2](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/python-api-v0.1.1...python-api-v0.1.2) (2024-03-18)


### BugFixes

* update README.md for API ([f606073](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f606073fd5b3783d51010289734b2915939a2e46))

## [0.1.1](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/python-api-v0.1.0...python-api-v0.1.1) (2024-03-18)


### BugFixes

* python-api release version ([#131](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/131)) ([3237651](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/32376519536cfa38e1889e2d185d713d5a46d013))

## [0.1.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/python-api-v0.0.2...python-api-v0.1.0) (2024-03-15)


### Features

* add data to the python package  ([#87](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/87)) ([0eb6831](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0eb68314345e641218b8bae243cff417271dca1b))
* add is_valid_term_id method to OntologyParser ([#115](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/115)) ([72c2073](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/72c2073f0a466d86e4cd40307dc53e3f9e31489f))
* include license file with python package ([#85](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/85)) ([2be3d81](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2be3d817041a4fbb6d5ab8b169a69b2fd8086e38))
* refactor ancestry mapping to include distance from descendant node + implement functions to support curated list term mapping ([#96](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/96)) ([7fc3562](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7fc3562b040f7c2962c0a6e751996933727d9206))
* refer to ontology source filenames in ontology_info and return that in get_ontology_download_url ([#106](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/106)) ([ff9d826](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ff9d82646413b3153daf8e6e60a9c8a1f32a0f61))
* split all_ontology into individual files. ([#93](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/93)) ([ead59e5](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ead59e5c0fe56c8f1feab9959d75965372c1316e))
* Support getting download link for ontology from source repo ([#86](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/86)) ([fd55b76](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fd55b760e655d419adcea94ade948347fa95ca6e))


### Misc

* automate testpypi releases ([#118](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/118)) ([b5a1a66](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b5a1a6608e44c6347281f6b59404af952a7e999c))
* clean-up ontology_parser single fetch and bulk fetch methods + account for acceptable non-ontology terms ([#112](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/112)) ([2ef7435](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2ef7435df62a75261fd75c819a76e7dd8f42cb99))
* **deps-dev:** bump semantic-version from 2.8.5 to 2.10.0 in /api/python ([#98](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/98)) ([dfe0b39](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/dfe0b397667cc8c4c6076cd293df576cbff3815f))


### BugFixes

* imports for api ([4cd3386](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/4cd33864fa59b3bd5e565a05b5b74414989566a8))
* update requirements ([#114](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/114)) ([9888f3d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/9888f3dad04e26ffd2bc5434a45645390a8eec01))

## 0.0.1 (2024-02-26)

### Features

- Add API ontology querying module ([68f3168](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/68f3168d164a192d538c987239bc2783decd5b1e))
- Add API ontology querying module ([#39](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/39)) ([239ef2b](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/239ef2b231d2b02051c374491bfee11a7e5d9d8e))
- **API:** setup python library ([211a099](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/211a099365b4de1ab9ff2dcf0f481a34f62f13c4))
- **API:** setup python library ([f60f897](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f60f8975584ed5e8fa9cd6dbe91bb0ba3f4e11bb))
- **API:** Setup the library for development ([1f7ce03](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/1f7ce0307db25ee553f0f924c872a73d4f0ae90f))
- implement stubbed query functions ([334deb5](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/334deb57463609d2736e369d188380686880fa9c))
- set version regex for pyton api ([3720dab](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/3720dabd593b3c6138470bd0b871f32c03f94dcf))

### Misc

- release tsmith/release-assets ([63b782d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/63b782d2ee8a8bdbdf83e61e0d37674954c802ee))
- release tsmith/release-assets ([#57](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/57)) ([6a6b02a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/6a6b02a96ab55f204480926ade478b197ff16e4e))

### BugFixes

- README.md ([1eae21d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/1eae21d1143d21fe248d8067671a270e46e54b19))
