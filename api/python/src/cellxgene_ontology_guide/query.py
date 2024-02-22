import gzip
import json
import re
from typing import Any, Dict, List

import env
import yaml

with gzip.open(env.ALL_ONTOLOGY_JSON, "rt") as f:
    ONTOLOGY_DICT = json.load(f)

with open(env.ONTOLOGY_INFO_YML, "rt") as f:
    SUPPORTED_ONTOLOGIES = yaml.safe_load(f)


def _parse_ontology_name(term_id: str) -> str:
    """
    Parse the ontology name from a given term ID. If the term ID does not conform to the expected term format or is not
    from an ontology supported by cellxgene-ontology-guide, raise a ValueError.

    :param term_id: str ontology term to parse
    :return: str name of ontology that term belongs to
    """
    pattern = r"[A-Za-z]+:\d+"
    if not re.match(pattern, term_id):
        raise ValueError(f"{term_id} does not conform to expected regex pattern {pattern} and cannot be queried.")

    ontology_name = term_id.split(":")[0]
    if ontology_name not in SUPPORTED_ONTOLOGIES:
        raise ValueError(f"{term_id} is not part of a supported ontology, its metadata cannot be fetched.")

    return ontology_name


def get_term_ancestors(term_id: str, include_self: bool = False) -> List[str]:
    """
    Get the ancestor ontology terms for a given term. If include_self is True, the term itself will be included as an
     ancestor.

     Example: get_term_ancestors("CL:0000005") -> ["CL:0000000", ...]

    :param term_id: str ontology term to find ancestors for
    :param include_self: boolean flag to include the term itself as an ancestor
    :return: flattened List[str] of ancestor terms
    """
    ontology_name = _parse_ontology_name(term_id)
    ancestors = ONTOLOGY_DICT[ontology_name][term_id]["ancestors"]
    return ancestors + [term_id] if include_self else ancestors


def get_term_list_ancestors(term_ids: str, include_self: bool = False) -> Dict[str, List[str]]:
    """
    Get the ancestor ontology terms for each term in a list. If include_self is True, the term itself will be included
     as an ancestor.

     Example: get_term_list_ancestors(["CL:0000003", "CL:0000005"], include_self=True) -> {
        "CL:0000003": ["CL:0000003"],
        "CL:0000005": ["CL:0000005", "CL:0000000", ...]
    }

    :param term_ids: list of str ontology terms to find ancestors for
    :param include_self: boolean flag to include the term itself as an ancestor
    :return: Dictionary mapping str term IDs to their respective flattened List[str] of ancestor terms. Maps to empty
    list if there are no ancestors.
    """
    return {term_id: get_term_ancestors(term_id, include_self) for term_id in term_ids}


def get_terms_descendants(term_ids: List[str], include_self: bool = False) -> Dict[str, List[str]]:
    """
    Get the descendant ontology terms for each term in a list. If include_self is True, the term itself will be included
     as a descendant.

    Example: get_terms_descendants(["CL:0000003", "CL:0000005"], include_self=True) -> {
        "CL:0000003": ["CL:0000003", "CL:0000004", ...],
        "CL:0000005": ["CL:0000005", "CL:0002363", ...]
    }

    :param term_ids: list of str ontology terms to find descendants for
    :param include_self: boolean flag to include the term itself as an descendant
    :return: Dictionary mapping str term IDs to their respective flattened List[str] of descendant terms. Maps to empty
    list if there are no descendants.
    """
    descendants_dict = dict()
    ontology_names = set()
    for term_id in term_ids:
        ontology_name = _parse_ontology_name(term_id)
        descendants_dict[term_id] = [term_id] if include_self else []
        ontology_names.add(ontology_name)

    for ontology in ontology_names:
        for candidate_descendant, candidate_metadata in ONTOLOGY_DICT[ontology].items():
            for ancestor_id in descendants_dict:
                if ancestor_id in candidate_metadata["ancestors"]:
                    descendants_dict[ancestor_id].append(candidate_descendant)

    return descendants_dict


def is_term_deprecated(term_id: str) -> bool:
    """
    Check if an ontology term is deprecated.

    Example: is_term_deprecated("CL:0000003") -> True

    :param term_id: str ontology term to check for deprecation
    :return: boolean flag indicating whether the term is deprecated
    """
    ontology_name = _parse_ontology_name(term_id)
    return ONTOLOGY_DICT[ontology_name][term_id]["deprecated"]


def get_term_replacement(term_id: str) -> str:
    """
    Fetch the replacement term for a deprecated ontology term, if a replacement exists. Return None otherwise.

    Example: get_term_replacement("CL:0000003") -> "CL:0000000"

    :param term_id: str ontology term to check a replacement term for
    :return: replacement str term ID if it exists, None otherwise
    """
    ontology_name = _parse_ontology_name(term_id)
    return ONTOLOGY_DICT[ontology_name][term_id].get("replaced_by", None)


def get_term_metadata(term_id: str) -> Dict[str, Any]:
    """
    Fetch metadata for a given ontology term. Returns a dict with format

    {"comments": ["...", ...], "term_tracker": "...", "consider": ["...", ...]}

    Comments maps to List[str] of ontology curator comments
    Term Tracker maps to a str url where there is discussion around this term's curation (or deprecation).
    Consider maps to List[str] of alternate ontology terms to consider using instead of this term

    All keys map to None if no metadata of that type is present.

    :param term_id: str ontology term to fetch metadata for
    :return: Dict with keys 'Comments', 'Term Tracker', and 'Consider' containing associated metadata.
    """
    ontology_name = _parse_ontology_name(term_id)
    return {
        key: ONTOLOGY_DICT[ontology_name][term_id].get(key, None) for key in {"comments", "term_tracker", "consider"}
    }


def get_term_label(term_id: str) -> str:
    """
    Fetch the human-readable label for a given ontology term.

    Example: get_term_label("CL:0000005") -> "fibroblast neural crest derived"

    :param term_id: str ontology term to fetch label for
    :return: str human-readable label for the term
    """
    ontology_name = _parse_ontology_name(term_id)
    return ONTOLOGY_DICT[ontology_name][term_id]["label"]
