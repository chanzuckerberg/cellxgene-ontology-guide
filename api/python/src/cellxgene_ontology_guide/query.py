from typing import List

import env
import gzip
import json

with gzip.open(env.ALL_ONTOLOGY_JSON, "rt") as f:
    ONTOLOGY_DICT = json.load(f)


def get_ancestors(term_id: str) -> List[str]:
    # TODO: Support List input, Dict return?
    # TODO: Regex input validation?
    # TODO: docstring
    ontology_name = term_id.split(":")[0]
    return ONTOLOGY_DICT[ontology_name][term_id]["ancestors"]
