import os

PACKAGE_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_ROOT = os.path.join(PACKAGE_ROOT, "data")
ONTOLOGY_FILENAME_SUFFIX = ".json.gz"
ONTOLOGY_INFO_FILENAME = "ontology_info.json"
VALID_NON_ONTOLOGY_TERMS = ["unknown", "na"]
