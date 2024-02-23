import os

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(PACKAGE_ROOT)))
FIXTURES_ROOT = os.path.join(ROOT_DIR, "api/python/src/cellxgene_ontology_guide/artifacts")
ONTOLOGY_REF_DIR = os.path.join(PACKAGE_ROOT, "ontology-references")
RAW_ONTOLOGY_DIR = os.path.join(ONTOLOGY_REF_DIR, "raw-files")
ONTO_INFO_YAML = os.path.join(FIXTURES_ROOT, "ontology_info.yml")
PARSED_ONTOLOGIES_FILE = os.path.join(FIXTURES_ROOT, "all_ontology.json.gz")
SCHEMA_DIR = os.path.join(os.path.realpath(__file__).rsplit("/", maxsplit=4)[0], "artifact-schemas")
ONTOLOGY_ASSETS = os.path.join(os.path.realpath(__file__).rsplit("/", maxsplit=4)[0], "ontology-assets")
