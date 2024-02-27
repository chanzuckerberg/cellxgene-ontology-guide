import os

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))
ALL_ONTOLOGY_FILENAME = "all_ontology.json.gz"
ONTOLOGY_INFO_FILENAME = "ontology_info.json"
ONTOLOGY_ASSET_RELEASE_URL = "https://github.com/chanzuckerberg/cellxgene-ontology-guide/releases/download"
SCHEMA_VERSION_TO_ONTOLOGY_ASSET_TAG = {
    "5.0.0": "ontology-assets-v0.0.1"
}
