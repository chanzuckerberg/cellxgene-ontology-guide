from unittest.mock import patch

import pytest
from cellxgene_ontology_guide.ontology_parser import OntologyParser
from cellxgene_ontology_guide.supported_versions import CXGSchema


@pytest.fixture
def ontology_dict():
    return {
        "CL:0000000": {"ancestors": {}, "label": "cell A", "description": "This is cell A.", "deprecated": False},
        "CL:0000001": {
            "ancestors": {"CL:0000000": 1},
            "label": "cell B",
            "deprecated": False,
            "consider": ["CL:0000004"],
            "synonyms": ["cell Beta", "cell Bravo"],
        },
        "CL:0000002": {"ancestors": {"CL:0000000": 1}, "label": "cell C", "deprecated": False},
        "CL:0000003": {
            "ancestors": {"CL:0000000": 1},
            "label": "obsolete cell",
            "deprecated": True,
            "replaced_by": "CL:0000004",
            "comments": ["this term was deprecated in favor of a descendant term of CL:0000001"],
            "term_tracker": "http://example.com/issue/1234",
        },
        "CL:0000004": {
            "ancestors": {"CL:0000000": 2, "CL:0000001": 1, "CL:0000002": 1},
            "label": "cell BC",
            "deprecated": False,
        },
        "CL:0000005": {
            "ancestors": {"CL:0000000": 2, "CL:0000001": 1, "CL:0000002": 1},
            "label": "cell BC2",
            "deprecated": False,
        },
        "CL:0000006": {"ancestors": {"CL:0000000": 2, "CL:0000001": 1}, "label": "cell B2", "deprecated": False},
        "CL:0000007": {"ancestors": {"CL:0000000": 2, "CL:0000001": 1}, "label": "cell B3", "deprecated": False},
        "CL:0000008": {"ancestors": {}, "label": "cell unrelated", "deprecated": False},
    }


@pytest.fixture
def ontology_dict_with_imports():
    return {
        "HANCESTRO:0000000": {
            "ancestors": {},
            "label": "root ancestry type",
            "description": "This is a root ancestry type.",
            "comments": ["this is an HANCESTRO term, not imported"],
            "term_tracker": "http://example.com/issue/HANCESTRO/1234",
            "synonyms": ["root ancestry synonym"],
            "deprecated": False,
        },
        "AfPO:0000000": {
            "ancestors": {"HANCESTRO:0000000": 1},
            "label": "specialized ancestry type",
            "description": "This is a specialized ancestry type.",
            "deprecated": False,
            "comments": ["this is an AfPO term imported into HANCESTRO"],
            "synonyms": ["specialized ancestry synonym"],
            "term_tracker": "http://example.com/issue/AfPO/1234",
            "replaced_by": "AfPO:0000001",
        },
        "HANCESTRO:0000001": {
            "ancestors": {"HANCESTRO:0000000": 2, "AfPO:0000000": 1},
            "label": "root ontology descendant of specialized ancestry type",
            "deprecated": False,
        },
    }


@pytest.fixture
def mock_CXGSchema(ontology_dict, ontology_dict_with_imports, mock_load_supported_versions, mock_load_ontology_file):
    mock_load_supported_versions.return_value = {
        "5.0.0": {
            "ontologies": {
                "CL": {"version": "2024-01-01", "source": "http://example.com", "filename": "cl.owl"},
                "HANCESTRO": {
                    "version": "2024-01-01",
                    "source": "http://example.com",
                    "filename": "cl.owl",
                    "additional_ontologies": ["AfPO"],
                },
            }
        }
    }
    cxg_schema = CXGSchema()
    cxg_schema.ontology_file_names = {
        "CL": "CL-ontology-2024-01-01.json.gz",
        "HANCESTRO": "HANCESTRO-ontology-2024-01-01.json.gz",
    }

    def get_mock_ontology_dict(file_name):
        if "CL" in file_name:
            return ontology_dict
        if "HANCESTRO" in file_name:
            return ontology_dict_with_imports
        return None

    mock_load_ontology_file.side_effect = get_mock_ontology_dict

    with patch("cellxgene_ontology_guide.ontology_parser.CXGSchema", return_value=cxg_schema) as mock:
        yield mock


@pytest.fixture
def ontology_parser(mock_CXGSchema):
    return OntologyParser(schema_version="5.0.0")


def test_parse_ontology_name(ontology_parser):
    assert ontology_parser._parse_ontology_name("CL:0000001") == "CL"


@pytest.mark.parametrize("term_id", ["AfPO:0000001", "HANCESTRO:0000000"])
def test_parse_ontology_name__imported_term(ontology_parser, term_id):
    assert ontology_parser._parse_ontology_name(term_id) == "HANCESTRO"


def test_parse_ontology_name__wrong_format(ontology_parser):
    with pytest.raises(ValueError):
        ontology_parser._parse_ontology_name("CL_0000001")


def test_parse_ontology_name__not_supported(ontology_parser):
    with pytest.raises(ValueError):
        ontology_parser._parse_ontology_name("GO:0000001")


@pytest.mark.parametrize(
    "term_id,expected",
    [("CL:0000001", True), ("CL:0000003", True), ("CL:0000009", False), ("GO:0000001", False), ("AfPO:0000000", True)],
)
def test_is_valid_term_id(ontology_parser, term_id, expected):
    assert ontology_parser.is_valid_term_id(term_id) == expected


@pytest.mark.parametrize(
    "term_id,ontology,expected",
    [
        ("CL:0000001", "CL", True),
        ("CL:0000001", "UBERON", False),
        ("GO:0000001", "GO", False),
        ("AfPO:0000000", "HANCESTRO", True),
        ("AfPO:0000000", "AfPO", False),
        ("HANCESTRO:0000001", "AfPO", False),
    ],
)
def test_is_valid_term_id__with_ontology(ontology_parser, term_id, ontology, expected):
    assert ontology_parser.is_valid_term_id(term_id, ontology) == expected


def test_get_term_ancestors(ontology_parser):
    assert ontology_parser.get_term_ancestors("CL:0000004") == ["CL:0000000", "CL:0000001", "CL:0000002"]
    assert ontology_parser.get_term_ancestors("CL:0000004", include_self=True) == [
        "CL:0000000",
        "CL:0000001",
        "CL:0000002",
        "CL:0000004",
    ]
    assert ontology_parser.get_term_ancestors("unknown", include_self=True) == []
    assert ontology_parser.get_term_ancestors("AfPO:0000000") == ["HANCESTRO:0000000"]
    assert ontology_parser.get_term_ancestors("HANCESTRO:0000001") == ["HANCESTRO:0000000", "AfPO:0000000"]


def test_map_term_ancestors(ontology_parser):
    assert ontology_parser.map_term_ancestors(["CL:0000000", "CL:0000004"]) == {
        "CL:0000000": [],
        "CL:0000004": ["CL:0000000", "CL:0000001", "CL:0000002"],
    }
    assert ontology_parser.map_term_ancestors(["CL:0000000", "CL:0000004", "unknown"], include_self=True) == {
        "CL:0000000": ["CL:0000000"],
        "CL:0000004": ["CL:0000000", "CL:0000001", "CL:0000002", "CL:0000004"],
        "unknown": [],
    }
    assert ontology_parser.map_term_ancestors(["AfPO:0000000", "HANCESTRO:0000001"]) == {
        "AfPO:0000000": ["HANCESTRO:0000000"],
        "HANCESTRO:0000001": ["HANCESTRO:0000000", "AfPO:0000000"],
    }


def test_get_term_ancestors_with_distances(ontology_parser):
    assert ontology_parser.get_term_ancestors_with_distances("CL:0000004") == {
        "CL:0000000": 2,
        "CL:0000001": 1,
        "CL:0000002": 1,
    }
    assert ontology_parser.get_term_ancestors_with_distances("CL:0000004", include_self=True) == {
        "CL:0000000": 2,
        "CL:0000001": 1,
        "CL:0000002": 1,
        "CL:0000004": 0,
    }
    assert ontology_parser.get_term_ancestors_with_distances("unknown", include_self=True) == {}
    assert ontology_parser.get_term_ancestors_with_distances("AfPO:0000000") == {"HANCESTRO:0000000": 1}
    assert ontology_parser.get_term_ancestors_with_distances("HANCESTRO:0000001") == {
        "HANCESTRO:0000000": 2,
        "AfPO:0000000": 1,
    }


def map_term_ancestors_with_distances(ontology_parser):
    assert ontology_parser.map_term_ancestors_with_distances(["CL:0000000", "CL:0000004"]) == {
        "CL:0000000": {},
        "CL:0000004": {"CL:0000000": 2, "CL:0000001": 1, "CL:0000002": 1},
    }
    assert ontology_parser.map_term_ancestors_with_distances(
        ["CL:0000000", "CL:0000004", "unknown"], include_self=True
    ) == {
        "CL:0000000": {"CL:0000000": 0},
        "CL:0000004": {"CL:0000000": 2, "CL:0000001": 1, "CL:0000002": 1, "CL:0000004": 0},
        "unknown": {},
    }
    assert ontology_parser.map_term_ancestors_with_distances(["AfPO:0000000", "HANCESTRO:0000001"]) == {
        "AfPO:0000000": {"HANCESTRO:0000000": 1},
        "HANCESTRO:0000001": {"HANCESTRO:0000000": 2, "AfPO:0000000": 1},
    }


def test_get_term_descendants(ontology_parser):
    assert ontology_parser.get_term_descendants("CL:0000000") == [
        "CL:0000001",
        "CL:0000002",
        "CL:0000003",
        "CL:0000004",
        "CL:0000005",
        "CL:0000006",
        "CL:0000007",
    ]
    assert ontology_parser.get_term_descendants("CL:0000004") == []
    assert ontology_parser.get_term_descendants("CL:0000004", include_self=True) == ["CL:0000004"]
    assert ontology_parser.get_term_descendants("na") == []
    assert ontology_parser.get_term_descendants("AfPO:0000000") == ["HANCESTRO:0000001"]
    assert ontology_parser.get_term_descendants("HANCESTRO:0000000") == ["AfPO:0000000", "HANCESTRO:0000001"]


def test_map_term_descendants(ontology_parser):
    assert ontology_parser.map_term_descendants(["CL:0000000", "CL:0000004"]) == {
        "CL:0000000": [
            "CL:0000001",
            "CL:0000002",
            "CL:0000003",
            "CL:0000004",
            "CL:0000005",
            "CL:0000006",
            "CL:0000007",
        ],
        "CL:0000004": [],
    }
    assert ontology_parser.map_term_descendants(["CL:0000000", "CL:0000004", "unknown"], include_self=True) == {
        "CL:0000000": [
            "CL:0000000",
            "CL:0000001",
            "CL:0000002",
            "CL:0000003",
            "CL:0000004",
            "CL:0000005",
            "CL:0000006",
            "CL:0000007",
        ],
        "CL:0000004": ["CL:0000004"],
        "unknown": [],
    }
    assert ontology_parser.map_term_descendants(["AfPO:0000000", "HANCESTRO:0000000"]) == {
        "AfPO:0000000": ["HANCESTRO:0000001"],
        "HANCESTRO:0000000": ["AfPO:0000000", "HANCESTRO:0000001"],
    }


def test_is_term_deprecated(ontology_parser):
    assert ontology_parser.is_term_deprecated("CL:0000003")
    assert not ontology_parser.is_term_deprecated("CL:0000004")
    assert not ontology_parser.is_term_deprecated("AfPO:0000000")


def test_get_term_replacement(ontology_parser):
    assert ontology_parser.get_term_replacement("CL:0000003") == "CL:0000004"
    assert ontology_parser.get_term_replacement("CL:0000004") is None
    assert ontology_parser.get_term_replacement("HANCESTRO:0000000") is None
    assert ontology_parser.get_term_replacement("AfPO:0000000") == "AfPO:0000001"


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
    assert ontology_parser.get_term_metadata("AfPO:0000000") == {
        "comments": ["this is an AfPO term imported into HANCESTRO"],
        "term_tracker": "http://example.com/issue/AfPO/1234",
        "consider": None,
    }
    assert ontology_parser.get_term_metadata("HANCESTRO:0000000") == {
        "comments": ["this is an HANCESTRO term, not imported"],
        "term_tracker": "http://example.com/issue/HANCESTRO/1234",
        "consider": None,
    }


def test_get_term_label(ontology_parser):
    assert ontology_parser.get_term_label("CL:0000004") == "cell BC"
    assert ontology_parser.get_term_label("AfPO:0000000") == "specialized ancestry type"
    assert ontology_parser.get_term_label("HANCESTRO:0000000") == "root ancestry type"


def test_map_term_labels(ontology_parser):
    assert ontology_parser.map_term_labels(
        ["CL:0000000", "CL:0000004", "AfPO:0000000", "HANCESTRO:0000000", "unknown", "na"]
    ) == {
        "CL:0000000": "cell A",
        "CL:0000004": "cell BC",
        "AfPO:0000000": "specialized ancestry type",
        "HANCESTRO:0000000": "root ancestry type",
        "unknown": "unknown",
        "na": "na",
    }


def test_get_term_description(ontology_parser):
    assert ontology_parser.get_term_description("CL:0000000") == "This is cell A."
    assert ontology_parser.get_term_description("CL:0000004") is None
    assert ontology_parser.get_term_description("HANCESTRO:0000000") == "This is a root ancestry type."
    assert ontology_parser.get_term_description("AfPO:0000000") == "This is a specialized ancestry type."


def test_map_term_description(ontology_parser):
    assert ontology_parser.map_term_descriptions(
        ["CL:0000000", "CL:0000004", "AfPO:0000000", "HANCESTRO:0000000", "unknown", "na"]
    ) == {
        "CL:0000000": "This is cell A.",
        "CL:0000004": None,
        "AfPO:0000000": "This is a specialized ancestry type.",
        "HANCESTRO:0000000": "This is a root ancestry type.",
        "unknown": "unknown",
        "na": "na",
    }


def test_get_term_synonyms(ontology_parser):
    assert ontology_parser.get_term_synonyms("CL:0000001") == ["cell Beta", "cell Bravo"]
    assert ontology_parser.get_term_synonyms("AfPO:0000000") == ["specialized ancestry synonym"]
    assert ontology_parser.get_term_synonyms("HANCESTRO:0000000") == ["root ancestry synonym"]


def test_map_term_synonyms(ontology_parser):
    assert ontology_parser.map_term_synonyms(
        ["CL:0000000", "CL:0000001", "AfPO:0000000", "HANCESTRO:0000000", "unknown", "na"]
    ) == {
        "CL:0000000": [],
        "CL:0000001": ["cell Beta", "cell Bravo"],
        "AfPO:0000000": ["specialized ancestry synonym"],
        "HANCESTRO:0000000": ["root ancestry synonym"],
        "unknown": [],
        "na": [],
    }


@pytest.mark.parametrize(
    "term_id,high_level_terms,expected",
    [
        ("CL:0000004", ["CL:0000000", "CL:0000001"], ["CL:0000000", "CL:0000001"]),
        ("CL:0000004", ["CL:0000001", "CL:0000000"], ["CL:0000001", "CL:0000000"]),  # preserve high level term order
        ("CL:0000008", ["CL:0000000", "CL:0000001"], []),
        ("CL:0000000", ["CL:0000000", "CL:0000001"], ["CL:0000000"]),
        ("CL:0000001", ["CL:0000000", "CL:0000001"], ["CL:0000000", "CL:0000001"]),
        ("HANCESTRO:0000001", ["HANCESTRO:0000000", "AfPO:0000000"], ["HANCESTRO:0000000", "AfPO:0000000"]),
        ("AfPO:0000000", ["HANCESTRO:0000000", "HANCESTRO:0000001"], ["HANCESTRO:0000000"]),
        ("na", ["CL:0000000", "CL:0000001"], []),
    ],
)
def test_get_high_level_terms(ontology_parser, term_id, high_level_terms, expected):
    assert ontology_parser.get_high_level_terms(term_id, high_level_terms) == expected


def test_map_high_level_terms(ontology_parser):
    assert ontology_parser.map_high_level_terms(
        term_ids=["CL:0000000", "CL:0000008", "CL:0000004", "unknown"],
        high_level_terms=["CL:0000000", "CL:0000001"],
    ) == {"CL:0000000": ["CL:0000000"], "CL:0000008": [], "CL:0000004": ["CL:0000000", "CL:0000001"], "unknown": []}


def test_get_highest_level_term(ontology_parser):
    high_level_terms = ["CL:0000000", "CL:0000001"]
    assert ontology_parser.get_highest_level_term("CL:0000004", high_level_terms) == "CL:0000000"
    assert ontology_parser.get_highest_level_term("CL:0000000", high_level_terms) == "CL:0000000"
    assert ontology_parser.get_highest_level_term("CL:0000008", high_level_terms) is None
    assert ontology_parser.get_highest_level_term("na", high_level_terms) is None

    assert (
        ontology_parser.get_highest_level_term("AfPO:0000000", ["HANCESTRO:0000000", "AfPO:0000000"])
        == "HANCESTRO:0000000"
    )


def test_map_highest_level_term(ontology_parser):
    assert ontology_parser.map_highest_level_term(
        term_ids=["CL:0000000", "CL:0000008", "CL:0000004"],
        high_level_terms=["CL:0000000", "CL:0000001"],
    ) == {"CL:0000000": "CL:0000000", "CL:0000008": None, "CL:0000004": "CL:0000000"}
    assert ontology_parser.map_highest_level_term(
        term_ids=["AfPO:0000000", "HANCESTRO:0000001"],
        high_level_terms=["HANCESTRO:0000000", "AfPO:0000000"],
    ) == {"AfPO:0000000": "HANCESTRO:0000000", "HANCESTRO:0000001": "HANCESTRO:0000000"}


def test_get_lowest_common_ancestors(ontology_parser):
    # root node LCA
    assert ontology_parser.get_lowest_common_ancestors(term_id_1="CL:0000003", term_id_2="CL:0000005") == ["CL:0000000"]

    # sibling LCA
    assert ontology_parser.get_lowest_common_ancestors(term_id_1="CL:0000006", term_id_2="CL:0000007") == ["CL:0000001"]

    # parent-child LCA
    assert ontology_parser.get_lowest_common_ancestors(term_id_1="CL:0000002", term_id_2="CL:0000005") == ["CL:0000002"]

    # multiple node
    lcas = ontology_parser.get_lowest_common_ancestors(term_id_1="CL:0000004", term_id_2="CL:0000005")
    assert len(lcas) == 2
    assert "CL:0000001" in lcas
    assert "CL:0000002" in lcas

    # disjoint
    assert ontology_parser.get_lowest_common_ancestors(term_id_1="CL:0000001", term_id_2="CL:0000008") == []

    # diff ontology terms with a common ancestor
    assert ontology_parser.get_lowest_common_ancestors(term_id_1="AfPO:0000000", term_id_2="HANCESTRO:0000001") == [
        "AfPO:0000000"
    ]


def test_get_distance_between_terms(ontology_parser):
    # distance when root node is lca
    assert ontology_parser.get_distance_between_terms(term_id_1="CL:0000003", term_id_2="CL:0000005") == 3

    # parent-child distance
    assert ontology_parser.get_distance_between_terms(term_id_1="CL:0000002", term_id_2="CL:0000005") == 1

    # multiple LCAs distance
    assert ontology_parser.get_distance_between_terms(term_id_1="CL:0000004", term_id_2="CL:0000005") == 2

    # disjoint distance
    assert ontology_parser.get_distance_between_terms(term_id_1="CL:0000001", term_id_2="CL:0000008") == -1

    # diff ontology terms
    assert ontology_parser.get_distance_between_terms(term_id_1="AfPO:0000000", term_id_2="HANCESTRO:0000001") == 1


@pytest.mark.parametrize(
    "term_id,expected",
    [
        ("CL:0000005", ["CL:0000001", "CL:0000002"]),
        ("CL:0000002", ["CL:0000000"]),
        ("CL:0000000", []),
        ("unknown", []),
        ("AfPO:0000000", ["HANCESTRO:0000000"]),
        ("HANCESTRO:0000001", ["AfPO:0000000"]),
    ],
)
def test_get_term_parents(ontology_parser, term_id, expected):
    assert ontology_parser.get_term_parents(term_id) == expected


@pytest.mark.parametrize(
    "term_id,expected",
    [
        ("CL:0000000", ["CL:0000001", "CL:0000002", "CL:0000003"]),
        ("CL:0000005", []),
        ("unknown", []),
        ("AfPO:0000000", ["HANCESTRO:0000001"]),
        ("HANCESTRO:0000000", ["AfPO:0000000"]),
    ],
)
def test_get_term_children(ontology_parser, term_id, expected):
    assert ontology_parser.get_term_children(term_id) == expected


def test_get_term_graph(ontology_parser):
    graph = ontology_parser.get_term_graph("CL:0000000")
    assert graph.to_dict() == {
        "term_id": "CL:0000000",
        "name": "cell A",
        "children": [
            {
                "term_id": "CL:0000001",
                "name": "cell B",
                "children": [
                    {"term_id": "CL:0000004", "name": "cell BC", "children": []},
                    {"term_id": "CL:0000005", "name": "cell BC2", "children": []},
                    {"term_id": "CL:0000006", "name": "cell B2", "children": []},
                    {"term_id": "CL:0000007", "name": "cell B3", "children": []},
                ],
            },
            {
                "term_id": "CL:0000002",
                "name": "cell C",
                "children": [
                    {"term_id": "CL:0000004", "name": "cell BC", "children": []},
                    {"term_id": "CL:0000005", "name": "cell BC2", "children": []},
                ],
            },
            {"term_id": "CL:0000003", "name": "obsolete cell", "children": []},
        ],
    }

    assert graph.term_counter == {
        "CL:0000000": 1,
        "CL:0000001": 1,
        "CL:0000002": 1,
        "CL:0000003": 1,
        "CL:0000004": 2,
        "CL:0000005": 2,
        "CL:0000006": 1,
        "CL:0000007": 1,
    }


def test_get_term_graph__imported_ontology(ontology_parser):
    graph = ontology_parser.get_term_graph("AfPO:0000000")
    assert graph.to_dict() == {
        "term_id": "AfPO:0000000",
        "name": "specialized ancestry type",
        "children": [
            {
                "term_id": "HANCESTRO:0000001",
                "name": "root ontology descendant of specialized ancestry type",
                "children": [],
            }
        ],
    }

    assert graph.term_counter == {
        "AfPO:0000000": 1,
        "HANCESTRO:0000001": 1,
    }


def test_get_term_label_to_id_map(ontology_parser):
    term_label_to_id_map_expected = {
        "cell A": "CL:0000000",
        "cell B": "CL:0000001",
        "cell C": "CL:0000002",
        "obsolete cell": "CL:0000003",
        "cell BC": "CL:0000004",
        "cell BC2": "CL:0000005",
        "cell B2": "CL:0000006",
        "cell B3": "CL:0000007",
        "cell unrelated": "CL:0000008",
    }
    assert ontology_parser.get_term_label_to_id_map("CL") == term_label_to_id_map_expected
    assert ontology_parser.term_label_to_id_map["CL"] == term_label_to_id_map_expected


@pytest.mark.parametrize("ontology_name", ["AfPO", "HANCESTRO"])
def test_get_term_label_to_id_map__imported_ontology(ontology_parser, ontology_name):
    term_label_to_id_map_expected = {
        "root ancestry type": "HANCESTRO:0000000",
        "specialized ancestry type": "AfPO:0000000",
        "root ontology descendant of specialized ancestry type": "HANCESTRO:0000001",
    }
    assert ontology_parser.get_term_label_to_id_map(ontology_name) == term_label_to_id_map_expected


@pytest.mark.parametrize(
    "label,ontology_name,expected",
    [
        ("cell A", "CL", "CL:0000000"),
        ("cell Z", "CL", None),
        ("root ancestry type", "HANCESTRO", "HANCESTRO:0000000"),
        ("specialized ancestry type", "AfPO", "AfPO:0000000"),
    ],
)
def test_get_term_id_by_label(ontology_parser, label, ontology_name, expected):
    assert ontology_parser.get_term_id_by_label(label, ontology_name) == expected


def test_get_term_id_by_label__unsupported_ontology_name(ontology_parser):
    with pytest.raises(ValueError):
        ontology_parser.get_term_id_by_label("gene A", "GO")
