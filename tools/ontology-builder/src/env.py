import os

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT_DIR = os.path.realpath(__file__).rsplit("/", maxsplit=4)[0]
ONTOLOGY_REF_DIR = os.path.join(PACKAGE_ROOT, "ontology-references")
RAW_ONTOLOGY_DIR = os.path.join(ONTOLOGY_REF_DIR, "raw-files")
ONTOLOGY_ASSETS_DIR = os.path.join(PROJECT_ROOT_DIR, "ontology-assets")
ONTO_INFO_YAML = os.path.join(ONTOLOGY_ASSETS_DIR, "ontology_info.yml")
PARSED_ONTOLOGIES_FILE = os.path.join(ONTOLOGY_ASSETS_DIR, "all_ontology.json.gz")
SCHEMA_DIR = os.path.join(PROJECT_ROOT_DIR, "artifact-schemas")
