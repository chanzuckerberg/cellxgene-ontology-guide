import json
from unittest.mock import patch

import pytest
from cellxgene_ontology_guide.curated_ontology_term_lists import get_curated_ontology_term_list
from cellxgene_ontology_guide.entities import CuratedOntologyTermList

MODULE_PATH = "cellxgene_ontology_guide.curated_ontology_term_lists"


@pytest.fixture
def mock_curated_ontology_term_list_file(tmpdir):
    with patch(f"{MODULE_PATH}.DATA_ROOT", tmpdir):
        test_file_name = "cell_class_list.json"
        test_enum = CuratedOntologyTermList.CELL_CLASS
        onto_file = tmpdir.join(test_file_name)
        file_contents = ["cell class 1", "cell class 2"]
        with open(str(onto_file), "wt") as onto_file:
            json.dump(file_contents, onto_file)
        yield test_enum, file_contents


def test_get_curated_ontology_term_list(mock_curated_ontology_term_list_file):
    test_enum, file_contents = mock_curated_ontology_term_list_file
    assert get_curated_ontology_term_list(test_enum) == file_contents
    assert get_curated_ontology_term_list.cache_info().hits == 0
    assert get_curated_ontology_term_list.cache_info().misses == 1
    get_curated_ontology_term_list(test_enum)
    assert get_curated_ontology_term_list.cache_info().hits == 1
    assert get_curated_ontology_term_list.cache_info().misses == 1


def test__clear_curated_ontology_term_list_cache(mock_curated_ontology_term_list_file):
    test_enum, _ = mock_curated_ontology_term_list_file
    get_curated_ontology_term_list(test_enum)
    assert get_curated_ontology_term_list.cache_info().misses == 1
    get_curated_ontology_term_list.cache_clear()
    assert get_curated_ontology_term_list.cache_info().misses == 0
    get_curated_ontology_term_list(test_enum)
    assert get_curated_ontology_term_list.cache_info().misses == 1
