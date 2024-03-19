lint:
	pre-commit run --all-files

docs:
	pdoc --output-dir docs/ ./api/python/src/cellxgene_ontology_guide

docs-local:
	pdoc ./api/python/src/cellxgene_ontology_guide
