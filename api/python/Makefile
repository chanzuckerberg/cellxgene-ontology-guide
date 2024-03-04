install: package-data
	pip install .

install-dev: package-data
	pip install -e .[test]

uninstall:
	pip uninstall -y cellxgene-ontology-guide

clean: uninstall
	rm -rf ./build ./src/cellxgene_ontology_guide.egg-info ./src/cellxgene_ontology_guide/data ./LICENSE

package-data:
	cp ../../LICENSE ./LICENSE
	cp -r ../../ontology-assets/ ./src/cellxgene_ontology_guide/data
	touch ./src/cellxgene_ontology_guide/data/__init__.py

unit-tests:
	python -m pytest tests
