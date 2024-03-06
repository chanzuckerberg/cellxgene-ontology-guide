import os

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_ROOT = os.path.join(PACKAGE_ROOT, "data")
ONTOLOGY_FILENAME_SUFFIX = ".json.gz"
ONTOLOGY_INFO_FILENAME = "ontology_info.json"
ONTOLOGY_ASSET_RELEASE_URL = "https://github.com/chanzuckerberg/cellxgene-ontology-guide/releases/download"
SCHEMA_VERSION_TO_ONTOLOGY_ASSET_TAG = {"5.0.0": "ontology-assets-v0.0.1"}
