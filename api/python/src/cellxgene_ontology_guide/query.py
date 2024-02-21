from typing import Dict, List

import env
import gzip
import json

with gzip.open(env.ALL_ONTOLOGY_JSON, "rt") as f:
    ONTOLOGY_DICT = json.load(f)


def _parse_ontology_name(term_id: str) -> str:
    # TODO: Regex input validation? Enum validation for ontology names / nice error handling?
    return term_id.split(":")[0]


def get_term_ancestors(term_id: str, include_self: bool = False) -> List[str]:
    # TODO: docstrings
    ontology_name = _parse_ontology_name(term_id)
    ancestors = ONTOLOGY_DICT[ontology_name][term_id]["ancestors"]
    return ancestors + term_id if include_self else ancestors


def get_terms_ancestors(term_ids: str, include_self: bool = False) -> Dict[str, List[str]]:
    return {term_id: get_term_ancestors(term_id, include_self) for term_id in term_ids}


def get_term_descendants(term_id: str, include_self: bool = False) -> List[str]:
    ontology_name = _parse_ontology_name(term_id)
    ontology_terms = ONTOLOGY_DICT[ontology_name]
    descendants = [term_id] if include_self else []
    for term, metadata in ontology_terms.items():
        if term_id in metadata["ancestors"]:
            descendants.append(term)
    return descendants


def get_terms_descendants(term_ids: List[str], include_self: bool = False) -> Dict[str, List[str]]:
    descendants_dict = dict()
    ontology_names = set()
    for term_id in term_ids:
        ontology_name = _parse_ontology_name(term_id)
        descendants_dict[term_id] = [term_id] if include_self else []
        ontology_names.add(ontology_name)

    for ontology in ontology_names:
        for candidate_descendant, candidate_metadata in ONTOLOGY_DICT[ontology].items():
            for ancestor_id in descendants_dict.keys():
                if ancestor_id in candidate_metadata["ancestors"]:
                    descendants_dict[ancestor_id].append(candidate_descendant)

    return descendants_dict


def is_term_deprecated(term_id: str) -> bool:
    ontology_name = _parse_ontology_name(term_id)
    return ONTOLOGY_DICT[ontology_name][term_id]["deprecated"]


def get_term_replacement(term_id: str) -> str:
    ontology_name = _parse_ontology_name(term_id)
    return ONTOLOGY_DICT[ontology_name][term_id].get("replaced_by", None)


def get_term_metadata(term_id: str) -> Dict[str, str]:
    ontology_name = _parse_ontology_name(term_id)
    return {
        key: ONTOLOGY_DICT[ontology_name][term_id].get(key, None) for key in {"comments", "term_tracker", "consider"}
    }


def get_term_label(term_id: str) -> str:
    ontology_name = _parse_ontology_name(term_id)
    return ONTOLOGY_DICT[ontology_name][term_id]["label"]
