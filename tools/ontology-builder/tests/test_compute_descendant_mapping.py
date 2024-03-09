import os.path
from unittest.mock import Mock

import pytest
from compute_descendent_mappings import (
    build_descendants_by_entity,
    extract_cell_types,
    extract_tissues,
    key_organoids_by_ontology_term_id,
    save_json,
    tag_tissue_type,
)


def test_save_json(tmpdir):
    test_file = tmpdir.join("test_file.json")
    save_json({}, test_file)
    assert os.path.isfile(test_file)


@pytest.mark.parametrize(
    "datasets, expected",
    [
        ([{"cell_type": {"ontology_term_id": "CL_0000000"}}], ["CL:0000000"]),
        ([{"cell_type": {}}], []),
        ([], []),
    ],
)
def test_extract_cell_types(datasets, expected):
    assert extract_cell_types(datasets) == expected


@pytest.mark.parametrize(
    "entity_name, tissue_type, expected",
    [
        ("UBERON:0000000", "tissue", "UBERON:0000000"),
        ("UBERON:0000000", "cell culture", "UBERON:0000000 (cell culture)"),
        ("UBERON:0000000", "organoid", "UBERON:0000000 (organoid)"),
        ("UBERON:0000000", "", "UBERON:0000000"),
        ("", "tissue", ""),
        ("", "cell culture", " (cell culture)"),
        ("", "organoid", " (organoid)"),
        ("", "", ""),
    ],
)
def test_tag_tissue_type(entity_name, tissue_type, expected):
    assert tag_tissue_type(entity_name, tissue_type) == expected


@pytest.mark.parametrize(
    "datasets, expected",
    [
        ([{"tissue": [{"ontology_term_id": "UBERON_0000000", "tissue_type": "test_tissue_type"}]}], ["UBERON:0000000"]),
        ([{"tissue": [{"ontology_term_id": "UBERON_0000000", "tissue_type": ""}]}], ["UBERON:0000000"]),
        ([{"tissue": []}], []),
        ([], []),
    ],
)
def test_extract_tissues(datasets, expected):
    assert extract_tissues(datasets) == expected


@pytest.mark.parametrize(
    "entity_names, expected",
    [(["UBERON:0000000"], {}), (["UBERON:0000000 (organoid)"], {"UBERON:0000000": "UBERON:0000000 (organoid)"})],
)
def test_key_organoids_by_ontology_term_id(entity_names, expected):
    assert key_organoids_by_ontology_term_id(entity_names) == expected


def test_build_descendants_by_entity():
    mock_ontology_parser = Mock()
    mock_ontology_parser.get_terms_descendants.return_value = {
        "a:1": ["a:0", "a:2", "a:3"],
        "A:1": ["UBERON:0000000, UBERON:0000003"],
        "UBERON:0000003": ["UBERON:0000000"],
        "UBERON:0000000": [],
    }
    heirarchy = [["UBERON:0000000"], ["UBERON:0000003", "UBERON:0000001", "UBERON:0000002"]]
    assert build_descendants_by_entity(heirarchy, mock_ontology_parser) == {
        "UBERON:0000001": ["UBERON:0000002", "UBERON:0000003"]
    }

    heirarchy = [["UBERON:0000000"], ["UBERON:0000001", "UBERON:0000002", "UBERON:0000003"]]
    assert build_descendants_by_entity(heirarchy, mock_ontology_parser) == {}
