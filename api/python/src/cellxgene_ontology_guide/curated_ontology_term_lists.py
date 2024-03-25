import functools
import json
import os
from typing import List

from cellxgene_ontology_guide._constants import DATA_ROOT
from cellxgene_ontology_guide.entities import CuratedOntologyTermList


@functools.cache
def get_curated_ontology_term_list(curated_ontology_term_list: CuratedOntologyTermList) -> List[str]:
    """
    Get the list of curated ontology terms for the given curated_ontology_term_list.

    :param curated_ontology_term_list: Enum attribute representing the curated ontology term list
    :return: List[str] of ontology term IDs
    """
    filename = f"{curated_ontology_term_list.value}_list.json"
    with open(os.path.join(DATA_ROOT, filename)) as f:
        return json.load(f)  # type: ignore
