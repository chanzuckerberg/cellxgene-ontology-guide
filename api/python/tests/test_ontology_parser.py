import pytest
from cellxgene_ontology_guide.ontology_parser import OntologyParser


@pytest.fixture(scope="module")
def ontology_dict():
    return {
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


@pytest.fixture(scope="module")
def supported_ontologies():
    return {"CL": {"version": "2024-01-01", "source": "http://example.com", "filetype": "owl"}}


@pytest.fixture(scope="module")
def ontology_parser(ontology_dict, supported_ontologies):
    parser = OntologyParser(schema_version="5.0.0")
    parser.ontology_dict = ontology_dict
    parser.supported_ontologies = supported_ontologies
    return parser


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
