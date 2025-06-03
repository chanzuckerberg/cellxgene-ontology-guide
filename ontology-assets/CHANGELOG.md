# Changelog

## [1.0.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.6.0...ontology-assets-v1.0.0) (2025-06-03)


### Features

* add experimental release + cl terms in efo ([#263](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/263)) ([#267](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/267)) ([508dc12](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/508dc12e26c0a2a4ce17578624dd7164b3546f34))
* add function to fetch curated ontology term lists ([#141](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/141)) ([5c7db62](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5c7db62672512f1b00b1380db77b8f06dbbfb000))
* additional species-specific ontologies for cxg 5.3 multispecies schema ([#255](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/255)) ([64c32fe](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/64c32fe91256323e3d5a2eff4153aa4ec63f528e))
* bump CL, EFO, HsapDv, MmusDv, MONDO, UBERON ontology versions for CxG schema 5.2.0 ([#217](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/217)) ([5bb43b9](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5bb43b988652ff003e89deccff8aecb9852205e5))
* bump ontology assets for 6.0 ([#281](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/281)) ([96d17de](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/96d17de8c0a3ef776e9b1195181b2b025d28b15e))
* fetch ontology term descriptions, if available ([#181](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/181)) ([0120377](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0120377f798192be6dde64322c10a0ecff935f05))
* fetch ontology term synonyms ([#200](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/200)) ([89c1725](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/89c1725bcb1a267229e43f136ea2d8941cb4a3bb))
* load GH Release Assets for schema version in memory ([#72](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/72)) ([58bad0a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/58bad0a698f262f167ba821ff00a4a7ca254d13a))
* pinned ontologies for schema 5.3.0 ([#275](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/275)) ([cd6a15e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/cd6a15e0b5ef8a9b95a956f6373b85de665225e7))
* prototype to support multiple prefixes ([#225](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/225)) ([dbcdd29](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/dbcdd297e2f06ca0f833cb293a7bc584d06ae738))
* refactor ancestry mapping to include distance from descendant node + implement functions to support curated list term mapping ([#96](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/96)) ([7fc3562](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7fc3562b040f7c2962c0a6e751996933727d9206))
* refer to ontology source filenames in ontology_info and return that in get_ontology_download_url ([#106](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/106)) ([ff9d826](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ff9d82646413b3153daf8e6e60a9c8a1f32a0f61))
* **release:** generate descendant mapping for tissues and cells ([#100](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/100)) ([841fddf](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/841fddf59abbaf1cb3bc823bdfb52b9e71371d92))
* remove all-ontology.json.gz ([83fefd6](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/83fefd68c7845d2a4d0299d958082820fd0f4fb3))
* remove v from ontology_info.json ([#196](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/196)) ([a1292a3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a1292a3c3a7d6c58e30b81c77418ce047d93df69))
* set up new github workflow for only ontologies that have changed ([#264](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/264)) ([45d0fce](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/45d0fce7fc168fd59961bd624af1c6097beda0ab))
* split all_ontology into individual files. ([#93](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/93)) ([ead59e5](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ead59e5c0fe56c8f1feab9959d75965372c1316e))
* update EFO to 3.71.0 ([#242](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/242)) ([7a92c0f](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7a92c0fdb72b983c308da257594dc6be89f5c992))
* update ontology_info.json for 5.1 ([#207](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/207)) ([d5c8ae3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/d5c8ae3f0502f0ca7165f821f384d553e2ed3e0b))
* upload assets on release ([#56](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/56)) ([84a1c5d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/84a1c5de42716d5c866d5eef7ce7113f6edbdbda))


### Misc

* deploy api when ontology_info.json changes ([#194](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/194)) ([40d58f6](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/40d58f6ca4cdb5236e1a3288e887d1d2516a7dbb))
* deprecate older version of cellxgene schema ([#172](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/172)) ([186e762](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/186e76235df3eec6767e3014e48530377d14d21f))
* move curated lists to ontology-assets ([#48](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/48)) ([77916df](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/77916df50d391c48ed0100441b1366f5013888bf))
* moving the generated artifacts ([c03c8e3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c03c8e353c61c69a807e80ec9d986bb652c41155))
* release 1.0.0 ([60eef67](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/60eef67d69fa3f4f776e67eeefef27391a307785))
* release main ([#130](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/130)) ([0b37dc8](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0b37dc85fea679874d51cfc7a22aeaee3e1d94b9))
* release main ([#146](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/146)) ([4ca76f0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/4ca76f0c6971946c54e8fd0a28f59eb6aabb8802))
* release main ([#185](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/185)) ([9b2fe53](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/9b2fe538b606172634f85ac1ab54d20a00dd1aa7))
* release main ([#195](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/195)) ([2f36845](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2f3684595a1ef2172d273ca79587e1c201e010e4))
* release main ([#201](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/201)) ([a8f5991](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a8f5991198f5825b35652f171aa4b456444a3ef4))
* release main ([#204](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/204)) ([dfc8d8e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/dfc8d8e95a2ad764e4c5dacefd19027b045bd8a2))
* release main ([#211](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/211)) ([77d6d7d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/77d6d7d536e01cd5f830d45a4f661a9a7121999f))
* release main ([#218](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/218)) ([b56bb90](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b56bb906fee5f87e711333f7fd27e61fd541fa33))
* release main ([#224](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/224)) ([133167c](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/133167c61004db1b3cd2f3b8e715dde67a71f3f9))
* release main ([#243](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/243)) ([7c2ff4d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7c2ff4d07ff6794d06cab6227b0bf5c87d66ec80))
* release main ([#256](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/256)) ([bd48472](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/bd48472af831b2fe76ca87180f1a798c9703be38))
* release main ([#258](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/258)) ([d56f1f4](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/d56f1f429cfbe6ec05ef84897be711252e461dce))
* release main ([#260](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/260)) ([9edebfd](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/9edebfd5b0a434fff5fd8c23245db85a63401156))
* release main ([#268](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/268)) ([0ac2219](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0ac2219f0f92f61aee2ec560f73750086eb6aabc))
* release main ([#274](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/274)) ([06fbda3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/06fbda32540ed62d5788b5aa189eb4476372257d))
* release main ([#282](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/282)) ([919a083](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/919a083f3312256a1e9eba7a3bc47a677650030d))
* release main ([#74](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/74)) ([e748fe9](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/e748fe972ef25b5fa15b271e73c3d7ad3d0b9f7f))
* release tsmith/release-assets ([63b782d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/63b782d2ee8a8bdbdf83e61e0d37674954c802ee))
* release tsmith/release-assets ([#57](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/57)) ([6a6b02a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/6a6b02a96ab55f204480926ade478b197ff16e4e))
* remove 5.3.1-alpha ([#273](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/273)) ([a930332](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a9303329e95e800ac8186ed833d7b45d146f6448))
* update ontology decendant mappings ([#117](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/117)) ([48451af](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/48451af5f3dcdb10cf1d97e50869f6c27f1dc756))
* update ontology decendant mappings ([#142](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/142)) ([fb23618](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fb2361810c227427a5ba50156328aeee74796aac))
* update ontology decendant mappings ([#162](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/162)) ([12def74](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/12def746eebb3d0273bb826be569ebfa1739d5ed))
* update ontology descendant mappings ([#167](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/167)) ([5d3d097](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5d3d0979798c78a8874bcca945986f809b76a825))
* update ontology descendant mappings ([#180](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/180)) ([65ca10f](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/65ca10feb7677f4066f87f73b49ea9f3b9ba78ca))
* update ontology descendant mappings ([#202](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/202)) ([b41948b](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b41948b5ca97888e4107c487f99cb120a68c9932))
* update ontology descendant mappings ([#205](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/205)) ([94157d0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/94157d072afd094393365a8610e85fb26b55f3ef))
* update ontology descendant mappings ([#209](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/209)) ([c493ca9](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c493ca953ebea208442ce6ba883b4f3b29450046))
* update ontology descendant mappings ([#213](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/213)) ([2a38574](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2a38574cebc6b83ee45bc19da35f383e574320e8))
* update ontology descendant mappings ([#219](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/219)) ([fa3094a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fa3094a263fa5785f6b939c3d8a8989244799e09))


### BugFixes

* lint errors ([f5e4583](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f5e45838e3c99dc3785ffc12f5e72aecc1ceeb29))
* parse through NCBITaxon ancestors ([#259](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/259)) ([c461251](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c461251d7b5becc5f2c268a52d3848a3f96474da))
* Schema format and validation fixes.  ([#113](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/113)) ([0465ee7](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0465ee75468fb5e0169e6ec4b5a40f1b875ecdd1))
* upgrade EFO from 3.69 to 3.74 ([#257](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/257)) ([c38e905](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c38e905c22113c8c83bc632e1e9cdd140510f5b3))

## [1.6.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.5.0...ontology-assets-v1.6.0) (2025-06-02)


### Features

* add experimental release + cl terms in efo ([#263](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/263)) ([#267](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/267)) ([508dc12](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/508dc12e26c0a2a4ce17578624dd7164b3546f34))
* add function to fetch curated ontology term lists ([#141](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/141)) ([5c7db62](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5c7db62672512f1b00b1380db77b8f06dbbfb000))
* additional species-specific ontologies for cxg 5.3 multispecies schema ([#255](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/255)) ([64c32fe](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/64c32fe91256323e3d5a2eff4153aa4ec63f528e))
* bump CL, EFO, HsapDv, MmusDv, MONDO, UBERON ontology versions for CxG schema 5.2.0 ([#217](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/217)) ([5bb43b9](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5bb43b988652ff003e89deccff8aecb9852205e5))
* bump ontology assets for 6.0 ([#281](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/281)) ([96d17de](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/96d17de8c0a3ef776e9b1195181b2b025d28b15e))
* fetch ontology term descriptions, if available ([#181](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/181)) ([0120377](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0120377f798192be6dde64322c10a0ecff935f05))
* fetch ontology term synonyms ([#200](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/200)) ([89c1725](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/89c1725bcb1a267229e43f136ea2d8941cb4a3bb))
* load GH Release Assets for schema version in memory ([#72](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/72)) ([58bad0a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/58bad0a698f262f167ba821ff00a4a7ca254d13a))
* pinned ontologies for schema 5.3.0 ([#275](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/275)) ([cd6a15e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/cd6a15e0b5ef8a9b95a956f6373b85de665225e7))
* prototype to support multiple prefixes ([#225](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/225)) ([dbcdd29](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/dbcdd297e2f06ca0f833cb293a7bc584d06ae738))
* refactor ancestry mapping to include distance from descendant node + implement functions to support curated list term mapping ([#96](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/96)) ([7fc3562](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7fc3562b040f7c2962c0a6e751996933727d9206))
* refer to ontology source filenames in ontology_info and return that in get_ontology_download_url ([#106](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/106)) ([ff9d826](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ff9d82646413b3153daf8e6e60a9c8a1f32a0f61))
* **release:** generate descendant mapping for tissues and cells ([#100](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/100)) ([841fddf](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/841fddf59abbaf1cb3bc823bdfb52b9e71371d92))
* remove all-ontology.json.gz ([83fefd6](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/83fefd68c7845d2a4d0299d958082820fd0f4fb3))
* remove v from ontology_info.json ([#196](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/196)) ([a1292a3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a1292a3c3a7d6c58e30b81c77418ce047d93df69))
* set up new github workflow for only ontologies that have changed ([#264](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/264)) ([45d0fce](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/45d0fce7fc168fd59961bd624af1c6097beda0ab))
* split all_ontology into individual files. ([#93](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/93)) ([ead59e5](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ead59e5c0fe56c8f1feab9959d75965372c1316e))
* update EFO to 3.71.0 ([#242](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/242)) ([7a92c0f](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7a92c0fdb72b983c308da257594dc6be89f5c992))
* update ontology_info.json for 5.1 ([#207](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/207)) ([d5c8ae3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/d5c8ae3f0502f0ca7165f821f384d553e2ed3e0b))
* upload assets on release ([#56](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/56)) ([84a1c5d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/84a1c5de42716d5c866d5eef7ce7113f6edbdbda))


### Misc

* deploy api when ontology_info.json changes ([#194](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/194)) ([40d58f6](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/40d58f6ca4cdb5236e1a3288e887d1d2516a7dbb))
* deprecate older version of cellxgene schema ([#172](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/172)) ([186e762](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/186e76235df3eec6767e3014e48530377d14d21f))
* move curated lists to ontology-assets ([#48](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/48)) ([77916df](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/77916df50d391c48ed0100441b1366f5013888bf))
* moving the generated artifacts ([c03c8e3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c03c8e353c61c69a807e80ec9d986bb652c41155))
* release 1.0.0 ([60eef67](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/60eef67d69fa3f4f776e67eeefef27391a307785))
* release main ([#130](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/130)) ([0b37dc8](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0b37dc85fea679874d51cfc7a22aeaee3e1d94b9))
* release main ([#146](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/146)) ([4ca76f0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/4ca76f0c6971946c54e8fd0a28f59eb6aabb8802))
* release main ([#185](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/185)) ([9b2fe53](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/9b2fe538b606172634f85ac1ab54d20a00dd1aa7))
* release main ([#195](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/195)) ([2f36845](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2f3684595a1ef2172d273ca79587e1c201e010e4))
* release main ([#201](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/201)) ([a8f5991](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a8f5991198f5825b35652f171aa4b456444a3ef4))
* release main ([#204](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/204)) ([dfc8d8e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/dfc8d8e95a2ad764e4c5dacefd19027b045bd8a2))
* release main ([#211](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/211)) ([77d6d7d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/77d6d7d536e01cd5f830d45a4f661a9a7121999f))
* release main ([#218](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/218)) ([b56bb90](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b56bb906fee5f87e711333f7fd27e61fd541fa33))
* release main ([#224](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/224)) ([133167c](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/133167c61004db1b3cd2f3b8e715dde67a71f3f9))
* release main ([#243](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/243)) ([7c2ff4d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7c2ff4d07ff6794d06cab6227b0bf5c87d66ec80))
* release main ([#256](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/256)) ([bd48472](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/bd48472af831b2fe76ca87180f1a798c9703be38))
* release main ([#258](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/258)) ([d56f1f4](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/d56f1f429cfbe6ec05ef84897be711252e461dce))
* release main ([#260](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/260)) ([9edebfd](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/9edebfd5b0a434fff5fd8c23245db85a63401156))
* release main ([#268](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/268)) ([0ac2219](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0ac2219f0f92f61aee2ec560f73750086eb6aabc))
* release main ([#274](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/274)) ([06fbda3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/06fbda32540ed62d5788b5aa189eb4476372257d))
* release main ([#74](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/74)) ([e748fe9](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/e748fe972ef25b5fa15b271e73c3d7ad3d0b9f7f))
* release tsmith/release-assets ([63b782d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/63b782d2ee8a8bdbdf83e61e0d37674954c802ee))
* release tsmith/release-assets ([#57](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/57)) ([6a6b02a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/6a6b02a96ab55f204480926ade478b197ff16e4e))
* remove 5.3.1-alpha ([#273](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/273)) ([a930332](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a9303329e95e800ac8186ed833d7b45d146f6448))
* update ontology decendant mappings ([#117](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/117)) ([48451af](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/48451af5f3dcdb10cf1d97e50869f6c27f1dc756))
* update ontology decendant mappings ([#142](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/142)) ([fb23618](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fb2361810c227427a5ba50156328aeee74796aac))
* update ontology decendant mappings ([#162](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/162)) ([12def74](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/12def746eebb3d0273bb826be569ebfa1739d5ed))
* update ontology descendant mappings ([#167](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/167)) ([5d3d097](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5d3d0979798c78a8874bcca945986f809b76a825))
* update ontology descendant mappings ([#180](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/180)) ([65ca10f](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/65ca10feb7677f4066f87f73b49ea9f3b9ba78ca))
* update ontology descendant mappings ([#202](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/202)) ([b41948b](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b41948b5ca97888e4107c487f99cb120a68c9932))
* update ontology descendant mappings ([#205](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/205)) ([94157d0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/94157d072afd094393365a8610e85fb26b55f3ef))
* update ontology descendant mappings ([#209](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/209)) ([c493ca9](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c493ca953ebea208442ce6ba883b4f3b29450046))
* update ontology descendant mappings ([#213](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/213)) ([2a38574](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2a38574cebc6b83ee45bc19da35f383e574320e8))
* update ontology descendant mappings ([#219](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/219)) ([fa3094a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fa3094a263fa5785f6b939c3d8a8989244799e09))


### BugFixes

* lint errors ([f5e4583](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f5e45838e3c99dc3785ffc12f5e72aecc1ceeb29))
* parse through NCBITaxon ancestors ([#259](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/259)) ([c461251](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c461251d7b5becc5f2c268a52d3848a3f96474da))
* Schema format and validation fixes.  ([#113](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/113)) ([0465ee7](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0465ee75468fb5e0169e6ec4b5a40f1b875ecdd1))
* upgrade EFO from 3.69 to 3.74 ([#257](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/257)) ([c38e905](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c38e905c22113c8c83bc632e1e9cdd140510f5b3))

## [1.5.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.4.0-alpha...ontology-assets-v1.5.0-alpha) (2025-03-05)


### Features

* pinned ontologies for schema 5.3.0 ([#275](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/275)) ([cd6a15e](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/cd6a15e0b5ef8a9b95a956f6373b85de665225e7))
* set up new github workflow for only ontologies that have changed ([#264](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/264)) ([45d0fce](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/45d0fce7fc168fd59961bd624af1c6097beda0ab))


### Misc

* remove 5.3.1-alpha ([#273](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/273)) ([a930332](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a9303329e95e800ac8186ed833d7b45d146f6448))

## [1.4.0-alpha](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.3.2...ontology-assets-v1.4.0) (2025-02-13)


### Features

* add experimental release + cl terms in efo ([#263](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/263)) ([#267](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/267)) ([508dc12](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/508dc12e26c0a2a4ce17578624dd7164b3546f34))

## [1.3.2](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.3.1...ontology-assets-v1.3.2) (2025-02-06)


### BugFixes

* parse through NCBITaxon ancestors ([#259](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/259)) ([c461251](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c461251d7b5becc5f2c268a52d3848a3f96474da))

## [1.3.1](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.3.0...ontology-assets-v1.3.1) (2025-01-28)


### BugFixes

* upgrade EFO from 3.69 to 3.74 ([#257](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/257)) ([c38e905](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c38e905c22113c8c83bc632e1e9cdd140510f5b3))

## [1.3.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.2.0...ontology-assets-v1.3.0) (2025-01-28)


### Features

* additional species-specific ontologies for cxg 5.3 multispecies schema ([#255](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/255)) ([64c32fe](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/64c32fe91256323e3d5a2eff4153aa4ec63f528e))

## [1.2.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.1.0...ontology-assets-v1.2.0) (2024-11-14)


### Features

* prototype to support multiple prefixes ([#225](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/225)) ([dbcdd29](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/dbcdd297e2f06ca0f833cb293a7bc584d06ae738))
* update EFO to 3.71.0 ([#242](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/242)) ([7a92c0f](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7a92c0fdb72b983c308da257594dc6be89f5c992))

## [1.1.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.0.2...ontology-assets-v1.1.0) (2024-09-04)


### Features

* bump CL, EFO, HsapDv, MmusDv, MONDO, UBERON ontology versions for CxG schema 5.2.0 ([#217](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/217)) ([5bb43b9](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5bb43b988652ff003e89deccff8aecb9852205e5))

## [1.0.2](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.0.1...ontology-assets-v1.0.2) (2024-08-23)


### Misc

* update ontology descendant mappings ([#213](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/213)) ([2a38574](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/2a38574cebc6b83ee45bc19da35f383e574320e8))
* update ontology descendant mappings ([#219](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/219)) ([fa3094a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fa3094a263fa5785f6b939c3d8a8989244799e09))

## [1.0.1](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v1.0.0...ontology-assets-v1.0.1) (2024-07-08)


### Misc

* update ontology descendant mappings ([#209](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/209)) ([c493ca9](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c493ca953ebea208442ce6ba883b4f3b29450046))

## [1.0.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v0.5.0...ontology-assets-v1.0.0) (2024-05-15)


### Features

* update ontology_info.json for 5.1 ([#207](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/207)) ([d5c8ae3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/d5c8ae3f0502f0ca7165f821f384d553e2ed3e0b))


### Misc

* release 1.0.0 ([60eef67](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/60eef67d69fa3f4f776e67eeefef27391a307785))
* update ontology descendant mappings ([#202](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/202)) ([b41948b](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/b41948b5ca97888e4107c487f99cb120a68c9932))
* update ontology descendant mappings ([#205](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/205)) ([94157d0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/94157d072afd094393365a8610e85fb26b55f3ef))

## [0.5.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v0.4.0...ontology-assets-v0.5.0) (2024-04-15)


### Features

* fetch ontology term synonyms ([#200](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/200)) ([89c1725](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/89c1725bcb1a267229e43f136ea2d8941cb4a3bb))

## [0.4.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v0.3.0...ontology-assets-v0.4.0) (2024-04-11)


### Features

* remove v from ontology_info.json ([#196](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/196)) ([a1292a3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/a1292a3c3a7d6c58e30b81c77418ce047d93df69))


### Misc

* deploy api when ontology_info.json changes ([#194](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/194)) ([40d58f6](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/40d58f6ca4cdb5236e1a3288e887d1d2516a7dbb))

## [0.3.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v0.2.0...ontology-assets-v0.3.0) (2024-04-09)


### Features

* fetch ontology term descriptions, if available ([#181](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/181)) ([0120377](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0120377f798192be6dde64322c10a0ecff935f05))


### Misc

* deprecate older version of cellxgene schema ([#172](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/172)) ([186e762](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/186e76235df3eec6767e3014e48530377d14d21f))
* update ontology decendant mappings ([#162](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/162)) ([12def74](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/12def746eebb3d0273bb826be569ebfa1739d5ed))
* update ontology descendant mappings ([#167](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/167)) ([5d3d097](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5d3d0979798c78a8874bcca945986f809b76a825))
* update ontology descendant mappings ([#180](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/180)) ([65ca10f](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/65ca10feb7677f4066f87f73b49ea9f3b9ba78ca))

## [0.2.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v0.1.0...ontology-assets-v0.2.0) (2024-03-25)


### Features

* add function to fetch curated ontology term lists ([#141](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/141)) ([5c7db62](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/5c7db62672512f1b00b1380db77b8f06dbbfb000))


### Misc

* update ontology decendant mappings ([#142](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/142)) ([fb23618](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/fb2361810c227427a5ba50156328aeee74796aac))

## [0.1.0](https://github.com/chanzuckerberg/cellxgene-ontology-guide/compare/ontology-assets-v0.0.1...ontology-assets-v0.1.0) (2024-03-15)


### Features

* load GH Release Assets for schema version in memory ([#72](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/72)) ([58bad0a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/58bad0a698f262f167ba821ff00a4a7ca254d13a))
* refactor ancestry mapping to include distance from descendant node + implement functions to support curated list term mapping ([#96](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/96)) ([7fc3562](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/7fc3562b040f7c2962c0a6e751996933727d9206))
* refer to ontology source filenames in ontology_info and return that in get_ontology_download_url ([#106](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/106)) ([ff9d826](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ff9d82646413b3153daf8e6e60a9c8a1f32a0f61))
* **release:** generate descendant mapping for tissues and cells ([#100](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/100)) ([841fddf](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/841fddf59abbaf1cb3bc823bdfb52b9e71371d92))
* remove all-ontology.json.gz ([83fefd6](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/83fefd68c7845d2a4d0299d958082820fd0f4fb3))
* split all_ontology into individual files. ([#93](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/93)) ([ead59e5](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/ead59e5c0fe56c8f1feab9959d75965372c1316e))


### Misc

* update ontology decendant mappings ([#117](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/117)) ([48451af](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/48451af5f3dcdb10cf1d97e50869f6c27f1dc756))


### BugFixes

* lint errors ([f5e4583](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/f5e45838e3c99dc3785ffc12f5e72aecc1ceeb29))
* Schema format and validation fixes.  ([#113](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/113)) ([0465ee7](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/0465ee75468fb5e0169e6ec4b5a40f1b875ecdd1))

## 0.0.1 (2024-02-26)

### Features

- upload assets on release ([#56](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/56)) ([84a1c5d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/84a1c5de42716d5c866d5eef7ce7113f6edbdbda))

### Misc

- move curated lists to ontology-assets ([#48](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/48)) ([77916df](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/77916df50d391c48ed0100441b1366f5013888bf))
- moving the generated artifacts ([c03c8e3](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/c03c8e353c61c69a807e80ec9d986bb652c41155))
- release tsmith/release-assets ([63b782d](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/63b782d2ee8a8bdbdf83e61e0d37674954c802ee))
- release tsmith/release-assets ([#57](https://github.com/chanzuckerberg/cellxgene-ontology-guide/issues/57)) ([6a6b02a](https://github.com/chanzuckerberg/cellxgene-ontology-guide/commit/6a6b02a96ab55f204480926ade478b197ff16e4e))
