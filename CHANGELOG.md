# Changelog

## [0.1.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/v0.0.1...v0.1.0) (2024-03-15)


### Features

* add data to the python package  ([#87](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/87)) ([0eb6831](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0eb68314345e641218b8bae243cff417271dca1b))
* add is_valid_term_id method to OntologyParser ([#115](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/115)) ([72c2073](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/72c2073f0a466d86e4cd40307dc53e3f9e31489f))
* include license file with python package ([#85](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/85)) ([2be3d81](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2be3d817041a4fbb6d5ab8b169a69b2fd8086e38))
* load GH Release Assets for schema version in memory ([#72](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/72)) ([58bad0a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/58bad0a698f262f167ba821ff00a4a7ca254d13a))
* refactor ancestry mapping to include distance from descendant node + implement functions to support curated list term mapping ([#96](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/96)) ([7fc3562](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7fc3562b040f7c2962c0a6e751996933727d9206))
* refer to ontology source filenames in ontology_info and return that in get_ontology_download_url ([#106](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/106)) ([ff9d826](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ff9d82646413b3153daf8e6e60a9c8a1f32a0f61))
* **release:** generate descendant mapping for tissues and cells ([#100](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/100)) ([841fddf](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/841fddf59abbaf1cb3bc823bdfb52b9e71371d92))
* remove all-ontology.json.gz ([83fefd6](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/83fefd68c7845d2a4d0299d958082820fd0f4fb3))
* split all_ontology into individual files. ([#93](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/93)) ([ead59e5](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ead59e5c0fe56c8f1feab9959d75965372c1316e))
* Support getting download link for ontology from source repo ([#86](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/86)) ([fd55b76](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fd55b760e655d419adcea94ade948347fa95ca6e))
* validate all json against their defined schemas. ([#91](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/91)) ([2512163](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/25121636ac65cb2f77996f44feb42f8e95847145))


### Misc

* clean-up ontology_parser single fetch and bulk fetch methods + account for acceptable non-ontology terms ([#112](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/112)) ([2ef7435](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2ef7435df62a75261fd75c819a76e7dd8f42cb99))
* **deps-dev:** bump semantic-version from 2.8.5 to 2.10.0 in /api/python ([#98](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/98)) ([dfe0b39](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/dfe0b397667cc8c4c6076cd293df576cbff3815f))
* **deps:** bump actions/cache from 1 to 4 in /.github/workflows ([#109](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/109)) ([b168bf2](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b168bf2dd64b891a8b4fa217e471f56df5222b8d))
* **deps:** bump actions/checkout from 2 to 4 in /.github/workflows ([#108](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/108)) ([caa835f](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/caa835fcd7b5a66846d7f189884c11fea6c6df48))
* **deps:** bump actions/setup-python from 1 to 5 in /.github/workflows ([#107](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/107)) ([b390ae4](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b390ae487b809273ec7aa3546af0d97edec0c620))
* **deps:** bump google-github-actions/release-please-action from 4.0.2 to 4.1.0 in /.github/workflows ([#110](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/110)) ([a45f34e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a45f34ea9fb4fdda54282d344ef6dc078ca19e1d))
* **deps:** bump pre-commit/action from 3.0.0 to 3.0.1 in /.github/workflows ([#111](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/111)) ([a2c9bd1](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a2c9bd1c170c09fac7d2a38deacc3a6211872618))
* **deps:** bump semantic-version from 2.8.5 to 2.10.0 in /tools/ontology-builder ([#97](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/97)) ([1ee8b7e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/1ee8b7ec440906c7a3b2a5c9bea3107bda0455ee))


### BugFixes

* dependabot for github actions ([341d418](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/341d4186c0a8da00c6c6eee11f598b682345d3e0))
* exclude CHANGELOG.md from prettier ([968a17e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/968a17eb52edee20f7d816c9449c25542b645dae))
* imports for api ([4cd3386](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/4cd33864fa59b3bd5e565a05b5b74414989566a8))
* lint errors ([f5e4583](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f5e45838e3c99dc3785ffc12f5e72aecc1ceeb29))
* python api releases ([bf0477e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/bf0477edcc36a96ff72ce05c7a0081d4f4dd9d37))
* run schema validator when *.json.gz updates ([886c855](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/886c85594b7b406a64048b3a6758b328dd5508b7))
* Schema format and validation fixes.  ([#113](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/113)) ([0465ee7](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0465ee75468fb5e0169e6ec4b5a40f1b875ecdd1))
* update gitignore ([15b9937](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/15b99376435d8c961ddc84e92aa821d5fe0bd5a2))
* update requirements ([#114](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/114)) ([9888f3d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/9888f3dad04e26ffd2bc5434a45645390a8eec01))

## 0.0.1 (2024-02-26)

### Features

- Add API ontology querying module ([68f3168](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/68f3168d164a192d538c987239bc2783decd5b1e))
- Add API ontology querying module ([#39](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/39)) ([239ef2b](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/239ef2b231d2b02051c374491bfee11a7e5d9d8e))
- **API:** setup python library ([211a099](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/211a099365b4de1ab9ff2dcf0f481a34f62f13c4))
- **API:** setup python library ([f60f897](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f60f8975584ed5e8fa9cd6dbe91bb0ba3f4e11bb))
- **API:** Setup the library for development ([1f7ce03](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/1f7ce0307db25ee553f0f924c872a73d4f0ae90f))
- **data release:** add hand curated_lists.py and orphans with comments and a generator s… ([#33](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/33)) ([413dc23](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/413dc233b61cfe62faa90328fd7ceca40ff5968d))
- Define JSON Schemas for ontology data release artifacts ([#32](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/32)) ([b23894a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b23894ad677ffdfa912ad0dc5897c099ff72efc3))
- fix changelog ([0285ef7](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0285ef79dde453a6ff540b88ce6c391a5d992e2b))
- implement stubbed query functions ([334deb5](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/334deb57463609d2736e369d188380686880fa9c))
- regenerate all_ontology if the schema changes ([5f74bfb](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5f74bfb222a5d30dc5e4821c19ad2cc782e15c94))
- set version regex for pyton api ([3720dab](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/3720dabd593b3c6138470bd0b871f32c03f94dcf))
- setup Lintes for repo ([4a70384](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/4a70384556bbdeedcfbb1520de051c7a7aa06ace))
- Store branch ancestors ("part_of" relationships) in all_ontology.json ([80e1f0d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/80e1f0ddc7be8e669521e09afc66eff919e2bbe6))
- Store branch ancestors ("part_of" relationships) in all_ontology.json ([#38](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/38)) ([64c2653](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/64c2653574f614e939696b2f5e0c0f3c4833d740))
- **testing:** add testing for ontology-builder ([e087eca](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/e087ecaf259cf102ef417296928545b74e4ef65b))
- **testing:** add testing for ontology-builder ([e087eca](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/e087ecaf259cf102ef417296928545b74e4ef65b))
- upload assets on release ([81725db](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/81725dbdcfe145662945bce3e1624f58c515e12a))
- upload assets on release ([#56](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/56)) ([84a1c5d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/84a1c5de42716d5c866d5eef7ce7113f6edbdbda))

### Misc

- add ontology-assets to release ([b09c814](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b09c8144b90ce0bfe7a3890d7d8bc508c7fb64c3))
- add ontology-assets to release ([04835c0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/04835c08bbbc5dce4a49864c884b7e84b8efdb92))
- bootstrap release-please ([f32db86](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f32db86fa71fb9274fd6d3fa10c91b095ba3575f))
- bootstrap release-please ([7d0554f](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7d0554ffc4742d4aa363bfe8e25abab1fc51be7b))
- change bootstrap-sha ([f2571e8](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f2571e84900f204556b0ce83cbef533469ac16b6))
- check that pr titles follow conventional commit format ([#41](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/41)) ([bd6d842](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/bd6d842c296d1b45fe3c8391a2a5dfa4770b857e))
- clean-up extract ontology term metadata parsing ([b9d2959](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b9d2959e81e3ea09e7238bf22828c8943f8faa31))
- configure release-please ([#40](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/40)) ([879ead2](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/879ead24c2d680612302a6a8e759773bcf3a4c97))
- **deps:** bump owlready2 from 0.38 to 0.45 in /tools/ontology-builder ([5466a08](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5466a0808bb9cae29c99cb145ba0642a35ab2303))
- **deps:** bump owlready2 from 0.38 to 0.45 in /tools/ontology-builder ([#37](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/37)) ([db3e5c8](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/db3e5c8af6ef9618947d95a76f1ee67ff0ddafaa))
- **deps:** bump pyyaml from 6.0 to 6.0.1 in /tools/ontology-builder ([98dfba2](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/98dfba2161fbf6fb2fe98dd22e31de910a4f379f))
- **deps:** bump pyyaml from 6.0 to 6.0.1 in /tools/ontology-builder ([#36](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/36)) ([72e7e40](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/72e7e40a9ee9a3eba344ae060dcb8531fc9b664b))
- enable release-please for API and Assets ([#55](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/55)) ([9ecda79](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/9ecda79210c5563dce8d8c743cca8367f35395ff))
- move curated lists to ontology-assets ([#48](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/48)) ([77916df](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/77916df50d391c48ed0100441b1366f5013888bf))
- move over all_ontology.json generator script + gha to repo from single-cell-curation ([f90fb05](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f90fb05d770ac17bfced15ca85e3f61d016dc4fa))
- move over all_ontology.json generator script + gha to repo from single-cell-curation ([#27](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/27)) ([49237a7](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/49237a729a95092eccf725c351fdca726a21625e))
- moving the generated artifacts ([c03c8e3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c03c8e353c61c69a807e80ec9d986bb652c41155))
- refactor all_ontology_generator for cleanliness and modularity ([b96c552](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b96c552f5d21386fed083af039fccd918aad8844))
- refactor all_ontology_generator for cleanliness and modularity ([b96c552](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b96c552f5d21386fed083af039fccd918aad8844))
- refactor all_ontology_generator for cleanliness and modularity ([4384459](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/43844597e23aaabf7b3d7e0cd3593012b312ea05))
- release 0.0.2 ([4972aa2](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/4972aa291eca32a9c00c429be762143e66bb15e1))
- release 0.0.2 ([#42](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/42)) ([19079d4](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/19079d47bb2161535b030c95628c2994dfc9827e))
- release tsmith/release-assets ([63b782d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/63b782d2ee8a8bdbdf83e61e0d37674954c802ee))
- release tsmith/release-assets ([#57](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/57)) ([6a6b02a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/6a6b02a96ab55f204480926ade478b197ff16e4e))
- remove unused release.yml configs ([ce00bef](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ce00bef8ec65fd03d973c63e14277165e098647c))
- test-release ([5f20d18](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5f20d1862c5898e501d7dd990305e277212d7d2b))

### BugFixes

- .release-please-manifest.json is valid json ([c09f2cc](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c09f2cc479d55aed7aedb62a0cef779274d645ed))
- add dependabot.yml ([575f371](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/575f371f8fcb74eff3db1a1060de9bbf8d479057))
- add ontology-assets ([8d51dea](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/8d51deaa62c4620f915f806a36717ac6ab8b520e))
- add ontology-assets ([01f504d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/01f504d0cdd5cb1031470479649a1e39dab3282f))
- README.md ([d19efeb](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/d19efeb4b3510d7eebeb0c67af9a2755839e224c))
- README.md ([1eae21d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/1eae21d1143d21fe248d8067671a270e46e54b19))
- release pr format ([20d9d1d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/20d9d1d555ad6306c4c21b75ed05d37c6c13d4d0))
- remove root from release-please-config.json ([8265b3e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/8265b3e104239f2c774b04fa13d0cf1c9d435534))
- test branch ([f68622a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f68622aa261c6aee93d4ae568e049e1505e7b3a5))
- test branch ([fac02bb](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fac02bb900777a90bcd7891446d61d985cb8a87c))
- test release ([aab95e8](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/aab95e819c579b09e83b86b34f2248f03162fa01))
- trigger all-ontology generation if schema changes ([#46](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/46)) ([3121833](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/3121833e24e39c449457e4fbd44cfb6cec5d21d5))
- use matrix ([b4d5298](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b4d5298158ce31775d4469cee25ef0db532680fb))
