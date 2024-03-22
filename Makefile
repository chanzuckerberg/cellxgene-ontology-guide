include tools/coverage.mk

lint:
	pre-commit run --all-files
