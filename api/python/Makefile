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

build: package-data
	python -m pip install --upgrade pip
	pip install build twine
	python -m build

release/testpypi: build
	python -m twine upload --repository testpypi dist/*

release/pypi: build
	# Manually release in case CI/CD pipeline is not working in ./.github/workflows/release.yml
	python -m twine upload dist/*

unit-tests:
	python -m pytest tests

