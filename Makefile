lint:
	pre-commit run --all-files

unit-test-ontology-builder:
	cd ./tools/ontology-builder && python -m pytest tests
