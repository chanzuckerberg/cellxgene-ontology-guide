import gzip
import json
from unittest.mock import patch

import pytest
from cellxgene_ontology_guide.constants import ALL_ONTOLOGY_FILENAME, ONTOLOGY_INFO_FILENAME
from cellxgene_ontology_guide.ontology_parser import OntologyParser


@pytest.fixture(scope="module")
def ontology_dict():
    ontology_dict = {
        "CL": {
            "CL:0000000": {"ancestors": [], "label": "cell A", "deprecated": False},
            "CL:0000001": {
                "ancestors": ["CL:0000000"],
                "label": "cell B",
                "deprecated": False,
                "consider": ["CL:0000004"],
            },
            "CL:0000002": {"ancestors": ["CL:0000000"], "label": "cell C", "deprecated": False},
            "CL:0000003": {
                "ancestors": ["CL:0000000"],
                "label": "obsolete cell",
                "deprecated": True,
                "replaced_by": "CL:0000004",
                "comments": ["this term was deprecated in favor of a descendant term of CL:0000001"],
                "term_tracker": "http://example.com/issue/1234",
            },
            "CL:0000004": {"ancestors": ["CL:0000001", "CL:0000000"], "label": "cell B2", "deprecated": False},
        }
    }
    return gzip.compress(json.dumps(ontology_dict).encode("utf-8"))


@pytest.fixture(scope="module")
def supported_ontologies():
    return b'{"CL": {"version": "2024-01-01", "source": "http://example.com", "filetype": "owl"}}'


@pytest.fixture(scope="module")
def mock_load_artifact_by_schema(ontology_dict, supported_ontologies):
    def get_mock_artifact_by_schema(schema_version, filename):
        if filename == ALL_ONTOLOGY_FILENAME:
            return ontology_dict
        elif filename == ONTOLOGY_INFO_FILENAME:
            return supported_ontologies

    with patch(
        "cellxgene_ontology_guide.ontology_parser.load_artifact_by_schema", side_effect=get_mock_artifact_by_schema
    ) as mock:
        yield mock


@pytest.fixture(scope="module")
def ontology_parser(mock_load_artifact_by_schema):
    return OntologyParser(schema_version="5.0.0")


def test_parse_ontology_name(ontology_parser):
    assert ontology_parser._parse_ontology_name("CL:0000001") == "CL"


def test_parse_ontology_name__wrong_format(ontology_parser):
    with pytest.raises(ValueError):
        ontology_parser._parse_ontology_name("CL_0000001")


def test_parse_ontology_name__not_supported(ontology_parser):
    with pytest.raises(ValueError):
        ontology_parser._parse_ontology_name("GO:0000001")


def test_get_term_ancestors(ontology_parser):
    assert ontology_parser.get_term_ancestors("CL:0000004") == ["CL:0000001", "CL:0000000"]
    assert ontology_parser.get_term_ancestors("CL:0000004", include_self=True) == [
        "CL:0000001",
        "CL:0000000",
        "CL:0000004",
    ]


def test_get_term_list_ancestors(ontology_parser):
    assert ontology_parser.get_term_list_ancestors(["CL:0000000", "CL:0000004"]) == {
        "CL:0000000": [],
        "CL:0000004": ["CL:0000001", "CL:0000000"],
    }
    assert ontology_parser.get_term_list_ancestors(["CL:0000000", "CL:0000004"], include_self=True) == {
        "CL:0000000": ["CL:0000000"],
        "CL:0000004": ["CL:0000001", "CL:0000000", "CL:0000004"],
    }


def test_get_terms_descendants(ontology_parser):
    assert ontology_parser.get_terms_descendants(["CL:0000000", "CL:0000004"]) == {
        "CL:0000000": ["CL:0000001", "CL:0000002", "CL:0000003", "CL:0000004"],
        "CL:0000004": [],
    }
    assert ontology_parser.get_terms_descendants(["CL:0000000", "CL:0000004"], include_self=True) == {
        "CL:0000000": ["CL:0000000", "CL:0000001", "CL:0000002", "CL:0000003", "CL:0000004"],
        "CL:0000004": ["CL:0000004"],
    }


def test_is_term_deprecated(ontology_parser):
    assert ontology_parser.is_term_deprecated("CL:0000003")
    assert not ontology_parser.is_term_deprecated("CL:0000004")


def test_get_term_replacement(ontology_parser):
    assert ontology_parser.get_term_replacement("CL:0000003") == "CL:0000004"
    assert ontology_parser.get_term_replacement("CL:0000004") is None


def test_get_term_metadata(ontology_parser):
    assert ontology_parser.get_term_metadata("CL:0000003") == {
        "comments": ["this term was deprecated in favor of a descendant term of CL:0000001"],
        "term_tracker": "http://example.com/issue/1234",
        "consider": None,
    }
    assert ontology_parser.get_term_metadata("CL:0000001") == {
        "comments": None,
        "term_tracker": None,
        "consider": ["CL:0000004"],
    }


def test_get_term_label(ontology_parser):
    assert ontology_parser.get_term_label("CL:0000004") == "cell B2"


def test__init__multiple_ontology_parsers(mock_load_artifact_by_schema, ontology_parser):
    ontology_parser_duplicate = OntologyParser(schema_version="5.0.0")
    ontology_parser_4 = OntologyParser(schema_version="4.0.0")

    assert ontology_parser_duplicate is ontology_parser
    assert ontology_parser_4 is not ontology_parser
