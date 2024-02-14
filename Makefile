lint:
	pre-commit run --all-files

unit-test-ontology-builder:
	Make unit-tests -C tools/ontology-builder
