#!/usr/bin/env python
"""
# Descendant Mappings for Tissues and Cell Types

## Overview

The ontology-aware tissue and cell type filters in the Single Cell Data Portal each require artifacts generated
by this script.

#### Descendant Mappings
To facilitate in-filter, cross-panel restriction of filter values, a descendant hierarchy dictionary is required by
the Single Cell Data Portal frontend. For example, if a user selects `hematopoietic system` in the tissue filter's
`System` panel, the values in the tissue filter's `Organ` and `Tissue` panels must be restricted by `hematopoietic
system`.

This script generates a dictionary of descendants keyed by tissue or cell type ontology term ID. The dictionary
is stored as a JSON file and copied to cellxgene-ontology-guide/ontology_assets directory. A versioned github release is
 created to simplify referencing in the Single Cell Data Portal.

The descendant mappings should be updated when:

1. The ontology version is updated,
2. A new tissue or cell type is added to the production corpus, or,
3. The hand-curated systems, organs, cell classes or cell subclasses are updated.
"""
import contextlib
import itertools
import json
import os
from typing import Any, Dict, Iterator, List
from urllib.request import urlopen

import env
from cellxgene_ontology_guide.ontology_parser import OntologyParser
from cellxgene_ontology_guide.supported_versions import CXGSchema


def load_prod_datasets() -> Any:
    """
    Request datasets the production corpus.
    """
    response = urlopen("https://api.cellxgene.cziscience.com/dp/v1/datasets/index").read().decode("utf-8")
    return json.loads(response)


def save_json(data: Any, file_name: str) -> None:
    """
    Save the given data to a JSON file.
    :param data: Any data compatiblewith JSON
    :param file_name: The name of the file to save the data to.
    """
    with open(file_name, "w") as f:
        json.dump(data, f, indent=2)


def extract_cell_types(datasets: List[Dict[str, Any]]) -> List[str]:
    """
    List the set of cell type values for the given datasets.

    :param datasets: a list of datasets from the production corpus.
    :return: a list formated of cell type values
    """
    cell_types = set()
    for dataset in datasets:
        for cell_type in dataset["cell_type"]:
            cell_types.add(cell_type["ontology_term_id"].replace("_", ":"))
    return list(cell_types)


def extract_tissues(datasets: List[Dict[str, Any]]) -> List[str]:
    """
    List the set of tissue values for the given datasets.

    :param datasets: a list of datasets from the production corpus.
    :return: a list of formated tissue values with tags for tissue type.
    """
    tissues = set()
    for dataset in datasets:
        for tissue in dataset["tissue"]:
            formatted_term_id = tissue["ontology_term_id"].replace("_", ":")
            tissue_type = tissue["tissue_type"]
            tissues.add(tag_tissue_type(formatted_term_id, tissue_type))

    return list(tissues)


def tag_tissue_type(term_id: str, tissue_type: str) -> str:
    """
    Append the tissue type to the given term_id name if the tissue type is cell
    culture or organoid, otherwise return the term_id name as is.

    :param term_id: str term_id name
    :param tissue_type: str tissue type
    :return: str term_id name with tissue type appended
    """
    # Tissue types
    tissue_type_cell_culture = "cell culture"
    tissue_type_organoid = "organoid"

    if tissue_type == tissue_type_cell_culture:
        # true if the given tissue type is "cell culture".
        return f"{term_id} ({tissue_type_cell_culture})"

    if tissue_type == tissue_type_organoid:
        # true if the given tissue type is "organoid".
        return f"{term_id} ({tissue_type_organoid})"

    return term_id


def key_organoids_by_ontology_term_id(term_ids: Iterator[str]) -> Dict[str, str]:
    """
    Returns a dictionary of organoid ontology term IDs by stem ontology term ID.

    :param term_ids: List of term_id names
    :return: Dict of organoid ontology term IDs by ontology term ID
    """

    organoids_by_ontology_term_id = {}
    for term_id in term_ids:
        if "(organoid)" in term_id:
            """
            Historically (i.e. before schema 4.0.0 and the introduction of
            `tissue_type`), tissues of type "organoid" were tagged with "(organoid)"
            in their labels and ontology IDs. The post-4.0.0 `tissue_type` value is
            mapped to this tagged version in order to minimize downstream updates to
            the filter functionality.
            """
            ontology_term_id = term_id.replace(" (organoid)", "")
            organoids_by_ontology_term_id[ontology_term_id] = term_id

    return organoids_by_ontology_term_id


def untag(term_id: str) -> str:
    """
    Remove the tag from the given term_id name.

    :param term_id: str term_id name
    :return: str term_id name without the tag
    """
    return term_id.split(" ")[0]


def build_descendants_by_term_id(
    term_id_hierarchy: List[List[str]], ontology_parser: OntologyParser
) -> Dict[str, List[str]]:
    """
    Create descendant relationships between the given term_id hierarchy.

    :param term_id_hierarchy: List of lists of term_id names in a hierarchy. The first list is the top
    level of the hierarchy.
    :param ontology_parser: OntologyParser instance
    :return: Dict of descendants by term_id sorted in ascending order.
    """
    all_descendants = {}
    organoids_by_ontology_term_id = key_organoids_by_ontology_term_id(itertools.chain(*term_id_hierarchy))
    for idx, term_ids in enumerate(term_id_hierarchy):
        # Create the set of descendants that can be included for this term_id set.
        # For example, systems can include organs or tissues,
        # organs can only include tissues, tissues can't have descendants.
        accept_lists = term_id_hierarchy[idx + 1 :]

        # Tissue or cell type for example will not have any descendants.
        if not accept_lists:
            continue

        accept_list = list(itertools.chain.from_iterable(accept_lists))

        # Remove tags and List descendants of term_ids.
        for term_id, descendants in ontology_parser.map_term_descendants(map(untag, term_ids)).items():
            # remove the tag from the entity name
            term_id = term_id.split(" ")[0]
            descendants = set(descendants)

            # Determine the set of descendants that be included.
            descendant_accept_list = []
            for descendant in descendants:
                # Include all entities in the accept list.
                if descendant in accept_list:
                    descendant_accept_list.append(descendant)

                # Add organoid descendants, if any.
                if descendant in organoids_by_ontology_term_id:
                    descendant_accept_list.append(organoids_by_ontology_term_id[descendant])

            # Add organoid term_id, if any.
            if term_id in organoids_by_ontology_term_id:
                descendant_accept_list.append(organoids_by_ontology_term_id[term_id])

            if not descendant_accept_list:
                continue

            # Add descendants to dictionary.
            all_descendants[term_id] = sorted(descendant_accept_list)
    return all_descendants


def generate_cell_descendant_mapping(ontology_parser: OntologyParser, datasets: List[Dict[str, Any]]) -> None:
    """
    Extracts a descendant mapping of CL starting with a set of hand-curated cell classes and subclasses. Cell types
    from the production corpus are also included in the mapping. The resulting mapping is saved to a JSON file.

    :param ontology_parser: OntologyParser instance
    :param datasets: a list of datasets from the production corpus.

    """
    # Load curated list of cell classes and cell subclasses.
    with open(os.path.join(env.ONTOLOGY_ASSETS_DIR, "cell_class_list.json"), "r") as f:
        cell_classes = json.load(f)

    with open(os.path.join(env.ONTOLOGY_ASSETS_DIR, "cell_subclass_list.json"), "r") as f:
        cell_subclasses = json.load(f)

    # extract the cell types from the datasets in the production corpus
    prod_cell_types = extract_cell_types(datasets)
    # establish the hierarchy of terms
    heirarchy = [cell_classes, cell_subclasses, prod_cell_types]
    # build the descendants mapping
    descendent_mapping = build_descendants_by_term_id(heirarchy, ontology_parser)
    # save the mapping to a file
    file_name = os.path.join(env.ONTOLOGY_ASSETS_DIR, "cell_type_descendants.json")
    save_json(descendent_mapping, file_name)


def generate_tissue_descendant_mapping(ontology_parser: OntologyParser, datasets: List[Dict[str, Any]]) -> None:
    """
    Extracts a descendant mapping of UBERON starting with a set of hand-curated system and organ tissue. Tissues types
    from the production corpus are also included in the mapping. The resulting mapping is saved to a JSON file.

    :param ontology_parser: OntologyParser instance
    :param datasets: a list of datasets from the production corpus.
    :return:
    """
    # Load curated list of systems and organ tissues.
    with open(os.path.join(env.ONTOLOGY_ASSETS_DIR, "system_list.json"), "r") as f:
        system_tissues = json.load(f)

    with open(os.path.join(env.ONTOLOGY_ASSETS_DIR, "organ_list.json"), "r") as f:
        organ_tissues = json.load(f)

    # extract the tissue types from the datasets in the production corpus
    prod_tissues = extract_tissues(datasets)
    # establish the hierarchy of terms
    heirarchy = [system_tissues, organ_tissues, prod_tissues]
    # build the descendants mapping
    descendent_mapping = build_descendants_by_term_id(heirarchy, ontology_parser)
    # save the mapping to a file
    file_name = os.path.join(env.ONTOLOGY_ASSETS_DIR, "tissue_descendants.json")
    save_json(descendent_mapping, file_name)


def compare_descendant_mappings(file_1: str, file_2: str) -> None:
    print(f"\n------Comparing {file_1} and {file_2}")
    # Testing
    with open(os.path.join(env.ONTOLOGY_ASSETS_DIR, file_1), "r") as f:
        mapping_1 = json.load(f)

    with open(os.path.join(env.ONTOLOGY_ASSETS_DIR, file_2), "r") as f:
        mapping_2 = json.load(f)

    matching_keys = mapping_1.keys() & mapping_2.keys()
    diff1_2 = dict()
    diff2_1 = dict()
    for key in matching_keys:
        decendents_1 = set(mapping_1[key])
        decendents_2 = set(mapping_2[key])
        diff1_2[key] = decendents_1 - decendents_2
        diff2_1[key] = decendents_2 - decendents_1
    print(f"KEYS: In {file_1} not in {file_2}")
    print("\t", mapping_1.keys() - mapping_2.keys() or None)
    print(f"DESCENDANT: In {file_1} not in {file_2}")
    for key in matching_keys:
        diff = set(mapping_1[key]) - set(mapping_2[key])
        if diff:
            print("\t", key, diff)

    print(f"\nKEYS: In {file_2} not in {file_1}")
    print("\t", mapping_2.keys() - mapping_1.keys() or None)
    print(f"DESCENDANT: In {file_2} not in {file_1}")
    for key in matching_keys:
        diff = set(mapping_2[key]) - set(mapping_1[key])
        if diff:
            print("\t", key, diff)


if __name__ == "__main__":
    with contextlib.suppress(FileNotFoundError):
        os.rename(
            os.path.join(env.ONTOLOGY_ASSETS_DIR, "cell_type_descendants.json"),
            os.path.join(env.ONTOLOGY_ASSETS_DIR, "cell_type_descendants_last.json"),
        )
    with contextlib.suppress(FileNotFoundError):
        os.rename(
            os.path.join(env.ONTOLOGY_ASSETS_DIR, "tissue_descendants.json"),
            os.path.join(env.ONTOLOGY_ASSETS_DIR, "tissue_descendants_last.json"),
        )

    ONTOLOGY_PARSER = OntologyParser(CXGSchema().version)
    # version
    PROD_DATASETS = load_prod_datasets()
    generate_cell_descendant_mapping(ONTOLOGY_PARSER, PROD_DATASETS)
    generate_tissue_descendant_mapping(ONTOLOGY_PARSER, PROD_DATASETS)

    with contextlib.suppress(FileNotFoundError):
        compare_descendant_mappings("cell_type_descendants.json", "cell_type_descendants_last.json")
    with contextlib.suppress(FileNotFoundError):
        compare_descendant_mappings("tissue_descendants.json", "tissue_descendants_last.json")

    os.remove(os.path.join(env.ONTOLOGY_ASSETS_DIR, "cell_type_descendants_last.json"))
    os.remove(os.path.join(env.ONTOLOGY_ASSETS_DIR, "tissue_descendants_last.json"))
