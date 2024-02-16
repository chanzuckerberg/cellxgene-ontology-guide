import json
import os.path
from typing import List

from curated_lists import CELL_CLASSES, CELL_SUBCLASSES, ORGAN_TISSUES, SYSTEM_TISSUES, TISSUE_GENERAL


def reformat_ontology_term_ids(d: List[str]) -> List[str]:
    # TODO: move to API
    return [i.replace("_", ":") for i in d]


def main(path: str = "ontology-references") -> None:
    """
    Using the dictionarys from curated_list.py, generate a json file that matches the JSON schema in artifact-schemas
    :param path: The destination path for the json files
    :return:
    """
    # Create a dictionary that matches the JSON schema in artifact-schemas
    with open(os.path.join(path, "system_list.json"), "w") as f:
        json.dump(reformat_ontology_term_ids(SYSTEM_TISSUES), f)

    with open(os.path.join(path, "organ_list.json"), "w") as f:
        json.dump(reformat_ontology_term_ids(ORGAN_TISSUES), f)

    with open(os.path.join(path, "tissue_general_list.json"), "w") as f:
        json.dump(reformat_ontology_term_ids(TISSUE_GENERAL), f)

    with open(os.path.join(path, "cell_class_list.json"), "w") as f:
        json.dump(reformat_ontology_term_ids(CELL_CLASSES), f)

    with open(os.path.join(path, "cell_subclass_list.json"), "w") as f:
        json.dump(reformat_ontology_term_ids(CELL_SUBCLASSES), f)


if __name__ == "__main__":
    main()
