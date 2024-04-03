import os

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))
RAW_ONTOLOGY_DIR = os.path.join(PACKAGE_ROOT, "raw-files")
PROJECT_ROOT_DIR = os.path.realpath(__file__).rsplit("/", maxsplit=4)[0]
SCHEMA_DIR = os.path.join(PROJECT_ROOT_DIR, "asset-schemas")
ONTOLOGY_ASSETS_DIR = os.path.join(PROJECT_ROOT_DIR, "ontology-assets")
ONTOLOGY_INFO_FILE = os.path.join(ONTOLOGY_ASSETS_DIR, "ontology_info.json")
