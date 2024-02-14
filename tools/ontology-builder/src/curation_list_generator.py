"""
Using the dictionarys from curated_list.py, generate a json file that matches the JSON schema in artifact-schemas
"""

import json
from typing import List

from curated_lists import cell_classes, cell_subclasses, organ_tissues, system_tissues


def reformat_ontology_term_id(d: List[str]) -> List[str]:
    # TODO: move to API
    return [i.replace("_", ":") for i in d]


def main() -> None:
    # Create a dictionary that matches the JSON schema in artifact-schemas
    with open("ontology-references/system_list.json", "w") as f:
        json.dump(reformat_ontology_term_id(system_tissues), f)

    with open("ontology-references/organ_list.json", "w") as f:
        json.dump(reformat_ontology_term_id(organ_tissues), f)

    with open("ontology-references/tissue_general_list.json", "w") as f:
        json.dump(reformat_ontology_term_id(system_tissues + organ_tissues), f)

    with open("ontology-references/cell_class_list.json", "w") as f:
        json.dump(reformat_ontology_term_id(cell_classes), f)

    with open("ontology-references/cell_subclass_list.json", "w") as f:
        json.dump(reformat_ontology_term_id(cell_subclasses), f)


if __name__ == "__main__":
    main()
