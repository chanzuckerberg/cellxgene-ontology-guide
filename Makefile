lint:
	pre-commit run --all-files

docs:
	pdoc --output-dir docs/ cellxgene_ontology_guide

docs-local:
	pdoc cellxgene_ontology_guide