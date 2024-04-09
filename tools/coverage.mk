# shared coverage targets
REPO_ROOT := $(shell git rev-parse --show-toplevel)
COVERAGE_DATA_FILE=.coverage.$(shell git rev-parse --short HEAD)
export COVERAGE_RUN_ARGS:=--data-file=$(REPO_ROOT)/$(COVERAGE_DATA_FILE) --branch --parallel-mode


coverage/run:
	coverage run $(COVERAGE_RUN_ARGS) -m pytest;

coverage/combine:
	coverage combine --data-file=$(COVERAGE_DATA_FILE)

coverage/report-xml: coverage/combine
	coverage xml --data-file=$(COVERAGE_DATA_FILE) -i --skip-empty

coverage/report-html: coverage/combine
	coverage html --data-file=$(COVERAGE_DATA_FILE) -i --skip-empty
