install: package-data
	pip install .

install-dev: package-data
	pip install -e .[test]

package-data:
	cp ../../LICENSE ./LICENSE

clean:
	rm -rf ./build ./src/cellxgene_ontology_guide.egg-info
	rm ./LICENSE


unit-tests:
	python -m pytest tests
