import pytest
from cellxgene_ontology_guide import query


@pytest.fixture()
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


@pytest.fixture()
def supported_ontologies():
    return {"CL": {"version": "2024-01-01", "source": "http://example.com", "filetype": "owl"}}


@pytest.fixture
def module_globals_override(monkeypatch, ontology_dict, supported_ontologies):
    monkeypatch.setattr(query, "ONTOLOGY_DICT", ontology_dict)
    monkeypatch.setattr(query, "SUPPORTED_ONTOLOGIES", supported_ontologies)


def test_parse_ontology_name(module_globals_override):
    assert query._parse_ontology_name("CL:0000001") == "CL"


def test_parse_ontology_name__wrong_format(module_globals_override):
    with pytest.raises(ValueError):
        query._parse_ontology_name("CL_0000001")


def test_parse_ontology_name__not_supported(module_globals_override):
    with pytest.raises(ValueError):
        query._parse_ontology_name("GO:0000001")


def test_get_term_ancestors(module_globals_override):
    assert query.get_term_ancestors("CL:0000004") == ["CL:0000001", "CL:0000000"]
    assert query.get_term_ancestors("CL:0000004", include_self=True) == ["CL:0000001", "CL:0000000", "CL:0000004"]


def test_get_term_list_ancestors(module_globals_override):
    assert query.get_term_list_ancestors(["CL:0000000", "CL:0000004"]) == {
        "CL:0000000": [],
        "CL:0000004": ["CL:0000001", "CL:0000000"],
    }
    assert query.get_term_list_ancestors(["CL:0000000", "CL:0000004"], include_self=True) == {
        "CL:0000000": ["CL:0000000"],
        "CL:0000004": ["CL:0000001", "CL:0000000", "CL:0000004"],
    }


def test_get_terms_descendants(module_globals_override):
    assert query.get_terms_descendants(["CL:0000000", "CL:0000004"]) == {
        "CL:0000000": ["CL:0000001", "CL:0000002", "CL:0000003", "CL:0000004"],
        "CL:0000004": [],
    }
    assert query.get_terms_descendants(["CL:0000000", "CL:0000004"], include_self=True) == {
        "CL:0000000": ["CL:0000000", "CL:0000001", "CL:0000002", "CL:0000003", "CL:0000004"],
        "CL:0000004": ["CL:0000004"],
    }


def test_is_term_deprecated(module_globals_override):
    assert query.is_term_deprecated("CL:0000003")
    assert not query.is_term_deprecated("CL:0000004")


def test_get_term_replacement(module_globals_override):
    assert query.get_term_replacement("CL:0000003") == "CL:0000004"
    assert query.get_term_replacement("CL:0000004") is None


def test_get_term_metadata(module_globals_override):
    assert query.get_term_metadata("CL:0000003") == {
        "comments": ["this term was deprecated in favor of a descendant term of CL:0000001"],
        "term_tracker": "http://example.com/issue/1234",
        "consider": None,
    }
    assert query.get_term_metadata("CL:0000001") == {
        "comments": None,
        "term_tracker": None,
        "consider": ["CL:0000004"],
    }


def test_get_term_label(module_globals_override):
    assert query.get_term_label("CL:0000004") == "cell B2"
