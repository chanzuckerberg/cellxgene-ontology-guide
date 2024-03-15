import os.path
from unittest.mock import Mock

import pytest
from descendent_mapping_generator import (
    build_descendants_by_term_id,
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
        ([{"cell_type": [{"ontology_term_id": "CL_0000000"}]}], ["CL:0000000"]),
        ([{"cell_type": []}], []),
        ([], []),
    ],
)
def test_extract_cell_types(datasets, expected):
    assert extract_cell_types(datasets) == expected


@pytest.mark.parametrize(
    "term_id, tissue_type, expected",
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
def test_tag_tissue_type(term_id, tissue_type, expected):
    assert tag_tissue_type(term_id, tissue_type) == expected


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
    "term_ids, expected",
    [(["UBERON:0000000"], {}), (["UBERON:0000000 (organoid)"], {"UBERON:0000000": "UBERON:0000000 (organoid)"})],
)
def test_key_organoids_by_ontology_term_id(term_ids, expected):
    assert key_organoids_by_ontology_term_id(term_ids) == expected


@pytest.fixture
def descendants_by_term_id():
    return {
        "a:0": ["a:1", "a:2", "a:3"],
        "a:1": ["a:2", "a:3"],
        "a:2": ["a:3"],
        "a:3": [],
    }


@pytest.fixture
def mock_ontology_parser(descendants_by_term_id):
    mock_ontology_parser = Mock()

    def map_term_descendants(term_ids):
        return {term_id: descendants_by_term_id[term_id] for term_id in term_ids}

    mock_ontology_parser.map_term_descendants = map_term_descendants
    return mock_ontology_parser


@pytest.mark.parametrize(
    "hierarchy, expected",
    [
        ([["a:3"], ["a:0", "a:1", "a:2"]], {}),
        ([["a:2", "a:3"], ["a:0", "a:1"]], {}),
        ([["a:1", "a:2", "a:3"], ["a:0"]], {}),
        ([["a:0", "a:1", "a:2", "a:3"], []], {}),
        ([["a:3"]], {}),
        ([["a:0"]], {}),
        ([["a:0"], ["a:1", "a:2", "a:3"]], {"a:0": ["a:1", "a:2", "a:3"]}),
        ([["a:0", "a:1"], ["a:2", "a:3"]], {"a:0": ["a:2", "a:3"], "a:1": ["a:2", "a:3"]}),
        ([["a:0", "a:1", "a:2"], ["a:3"]], {"a:0": ["a:3"], "a:1": ["a:3"], "a:2": ["a:3"]}),
    ],
)
def test_refine_descendants_by_term_id(hierarchy, mock_ontology_parser, expected):
    assert build_descendants_by_term_id(hierarchy, mock_ontology_parser) == expected


@pytest.mark.parametrize(
    "hierarchy, expected",
    [
        ([["a:0"], ["a:3 (organoid)"]], {"a:0": ["a:3 (organoid)"]}),
        ([["a:0"], ["a:3", "a:3 (organoid)"]], {"a:0": ["a:3", "a:3 (organoid)"]}),
        ([["a:0 (organoid)"], []], {}),
    ],
)
def test_refine_descendants_by_term_id_organoid(hierarchy, mock_ontology_parser, expected):
    assert build_descendants_by_term_id(hierarchy, mock_ontology_parser) == expected
