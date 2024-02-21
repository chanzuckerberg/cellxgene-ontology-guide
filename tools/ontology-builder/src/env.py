import os

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))
ONTOLOGY_REF_DIR = os.path.join(PACKAGE_ROOT, "ontology-references")
RAW_ONTOLOGY_DIR = os.path.join(ONTOLOGY_REF_DIR, "raw-files")
ONTO_INFO_YAML = os.path.join(ONTOLOGY_REF_DIR, "ontology_info.yml")
PARSED_ONTOLOGIES_FILE = os.path.join(ONTOLOGY_REF_DIR, "all_ontology.json.gz")
SCHEMA_DIR = os.path.join(os.path.realpath(__file__).rsplit("/", maxsplit=4)[0], "artifact-schemas")
