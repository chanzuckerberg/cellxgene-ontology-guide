import gzip
import json
import os
import urllib.request
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from all_ontology_generator import (
    _download_ontologies,
    _extract_cross_ontology_terms,
    _extract_ontology_term_metadata,
    _load_cross_ontology_map,
    _parse_ontologies,
    _parse_uniprot_xml,
    deprecate_previous_cellxgene_schema_versions,
    get_ontology_info_file,
    list_expired_cellxgene_schema_version,
    update_ontology_info,
)


@pytest.fixture
def mock_ontology_info():
    return {
        "ontology_name": {
            "source": "http://example.com",
            "version": "v1",
            "filename": "ontology_name.owl",
            "format": "owl",
            "cross_ontology_mapping": {
                "filename": "ontology_name.sssom.tsv",
                "format": "sssom.tsv",
            },
        }
    }


@pytest.fixture
def mock_ontology_info_file(tmpdir, mock_ontology_info):
    # Create a temporary ontology info file
    ontology_info_file = tmpdir.join("ontology_info.json")
    ontology_info = {"v1.0.0": True, "v2.0.0": mock_ontology_info}
    ontology_info_file.write(json.dumps(ontology_info))
    return str(ontology_info_file)


@pytest.fixture
def mock_raw_ontology_dir(tmpdir):
    # Create a temporary ontology file
    sub_dir_name = "raw_ontology"
    sub_dir = tmpdir.mkdir(sub_dir_name)
    onto_owl_file = tmpdir.join(sub_dir_name, "ontology_name.owl")
    onto_owl_file.write("")
    # Filename matches cross_ontology_mapping.filename in mock_ontology_info
    cross_onto_tsv_file = tmpdir.join(sub_dir_name, "ontology_name.sssom.tsv")
    cross_onto_tsv_file.write(
        """subject_id\tsubject_label\tpredicate_id\tobject_id\tobject_label\nFOO:000002\tTest Term\tsemapv:crossSpeciesExactMatch\tOOF:000002\ttest match term"""
    )
    return str(sub_dir)


@pytest.fixture
def mock_owl(tmpdir):
    import owlready2

    onto = owlready2.get_ontology("http://example.com/ontology_name.owl")
    onto.name = "FAKE"

    return onto


def test_get_ontology_info_file_default(mock_ontology_info_file):
    # Call the function
    ontology_info = get_ontology_info_file(ontology_info_file=mock_ontology_info_file)

    # Assertion
    assert "v1.0.0" in ontology_info
    assert "v2.0.0" in ontology_info


def test_download_ontologies(mock_ontology_info, mock_raw_ontology_dir):
    # Mocking urllib.request.urlretrieve, urllib.request.urlopen
    with patch("urllib.request.urlretrieve") as mock_urlretrieve, patch("urllib.request.urlopen") as mock_urlopen:
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.code = 200
        mock_urlopen.return_value = mock_response

        # Call the function
        _download_ontologies(ontology_info=mock_ontology_info, output_dir=mock_raw_ontology_dir)

        # One call per file: the main .owl + the cross_ontology_mapping .sssom.tsv
        expected_calls = sum(
            1 + (1 if info.get("cross_ontology_mapping") else 0) for info in mock_ontology_info.values()
        )
        assert mock_urlretrieve.call_count == expected_calls


def test_parse_ontologies(mock_ontology_info, mock_raw_ontology_dir, tmpdir):
    # Mocking _load_ontology_object and _extract_ontology_term_metadata
    with (
        patch("all_ontology_generator._load_ontology_object") as mock_load_ontology,
        patch("all_ontology_generator._load_cross_ontology_map") as mock_load_cross_ontology_map,
        patch("all_ontology_generator._extract_ontology_term_metadata") as mock_extract_metadata,
        patch("all_ontology_generator._extract_cross_ontology_terms") as mock_extract_cross_ontology_terms,
    ):
        # Mock return values
        MockOntologyObject = MagicMock()
        mock_load_ontology.return_value = MockOntologyObject
        mock_extract_metadata.return_value = {"term_id": {"label": "Term Label", "deprecated": False, "ancestors": {}}}
        mock_load_cross_ontology_map.return_value = {}
        mock_extract_cross_ontology_terms.return_value = {}

        # Mock output path
        output_path = tmpdir.mkdir("output")
        # Call the function — _parse_ontologies now iterates ontology_info keys, not the filesystem
        output_files = list(
            _parse_ontologies(
                ontology_info=mock_ontology_info, working_dir=mock_raw_ontology_dir, output_path=output_path
            )
        )

        num_ontologies = len(mock_ontology_info)

        # Assert the output file is created
        assert all(os.path.isfile(file) for file in output_files)

        # Assert one output file per ontology entry
        assert len(os.listdir(output_path)) == num_ontologies

        # Assert _load_ontology_object is called once per non-xml.gz ontology
        assert mock_load_ontology.call_count == num_ontologies

        # Assert _extract_ontology_term_metadata is called once per non-xml.gz ontology
        assert mock_extract_metadata.call_count == num_ontologies

        # Assert _load_cross_ontology_map is called once regardless of how many ontologies
        assert mock_load_cross_ontology_map.call_count == 1


def test_download_ontologies_http_error(mock_ontology_info, mock_raw_ontology_dir):
    # Mocking urllib.request.urlopen to raise HTTPError
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="http://example.com", code=404, msg="Not Found", hdrs={}, fp=None
        )

        # Assertion
        with pytest.raises(Exception) as exc_info:
            _download_ontologies(ontology_info=mock_ontology_info, output_dir=mock_raw_ontology_dir)
        assert "returns status code 404" in str(exc_info.value)


def test_download_ontologies_url_error(mock_ontology_info, mock_raw_ontology_dir):
    # Mocking urllib.request.urlopen to raise URLError
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError(reason="Connection refused")

        # Assertion
        with pytest.raises(Exception) as exc_info:
            _download_ontologies(ontology_info=mock_ontology_info, output_dir=mock_raw_ontology_dir)
        assert "fails due to Connection refused" in str(exc_info.value)


@pytest.fixture
def mock_datetime():
    with patch("all_ontology_generator.datetime") as mock_datetime:
        mock_datetime.strptime = datetime.strptime
        mock_datetime.now.return_value = datetime(2024, 1, 1)
        yield mock_datetime


def test_list_expired_cellxgene_schema_version(mock_datetime):
    ontology_info = {
        "v1": {"deprecated_on": "2022-01-01"},  # Expired
        "v2": {"deprecated_on": "2023-07-05"},  # Not expired
        "v3": {"deprecated_on": "2024-01-01"},  # Now, Not expired
    }
    # Expected expired versions based on the mock data
    expected_expired_versions = ["v1"]

    # Call the function
    expired_versions = list_expired_cellxgene_schema_version(ontology_info)

    # Assert the result matches the expected expired versions
    assert expired_versions == expected_expired_versions


def test_list_expired_cellxgene_schema_version_no_deprecated_on(mock_datetime):
    # If no 'deprecated_on' field is provided, the version should not be considered expired
    ontology_info_no_deprecated_on = {
        "v1": {},  # No 'deprecated_on' field, Not expired
    }

    # Call the function
    expired_versions = list_expired_cellxgene_schema_version(ontology_info_no_deprecated_on)

    # Assert no versions are considered expired
    assert expired_versions == []


def test_list_expired_cellxgene_schema_version_future_date(mock_datetime):
    # If 'deprecated_on' is in the future, it should not be considered expired
    ontology_info_future_date = {
        "v1": {"deprecated_on": "2030-01-01"},  # Future date, Not expired
    }

    # Call the function
    expired_versions = list_expired_cellxgene_schema_version(ontology_info_future_date)

    # Assert no versions are considered expired
    assert expired_versions == []


def test_list_expired_cellxgene_schema_version_now(mock_datetime):
    # If 'deprecated_on' is today, it should be considered expired
    now = datetime(2024, 1, 1).strftime("%Y-%m-%d")
    ontology_info_today = {
        "v1": {"deprecated_on": now},  # Today's date, Not expired
    }

    # Call the function
    expired_versions = list_expired_cellxgene_schema_version(ontology_info_today)

    # Assert the version with 'deprecated_on' as now is not considered expired
    assert expired_versions == []


def test_update_ontology_info(mock_datetime):
    ontology_info = {
        "v1": {"deprecated_on": "2022-01-01", "ontologies": {"A": {"version": 1}, "B": {"version": 1}}},  # Expired
        "v2": {"deprecated_on": "2023-07-05", "ontologies": {"A": {"version": 2}, "B": {"version": 1}}},  # Not expired
    }
    expected_ontology_info = {
        "v2": {"deprecated_on": "2023-07-05", "ontologies": {"A": {"version": 2}, "B": {"version": 1}}},  # Not expired
    }
    expected_removed_files = {"A-ontology-1.json.gz"}

    # Call the function
    removed_files = update_ontology_info(ontology_info)

    # Assert the result matches the expected expired versions
    assert ontology_info == expected_ontology_info
    assert removed_files == expected_removed_files


def test_deprecate_previous_cellxgene_schema_versions(mock_datetime):
    ontology_info = {
        "v1": {},  # current version
        "v2": {},  # not deprecated
        "v3": {},  # multiple versions to deprecate
        "v4": {"deprecated_on": "2023-01-01"},  # already deprecated
    }
    expected_ontology_info = {
        "v1": {},  # unchanged
        "v2": {"deprecated_on": "2024-01-01"},  # added deprecated_on
        "v3": {"deprecated_on": "2024-01-01"},  # added deprecated_on
        "v4": {"deprecated_on": "2023-01-01"},  # unchanged
    }

    # Call the function
    deprecate_previous_cellxgene_schema_versions(ontology_info, "v1")

    assert ontology_info == expected_ontology_info


@pytest.fixture
def sample_ontology(tmp_path):
    # Create a new ontology
    import owlready2

    onto = owlready2.get_ontology("http://test.org/onto.owl")
    onto.name = "FOO"

    with onto:

        class FOO_000001(owlready2.Thing):
            label = ["Test Root Term"]

        class FOO_000002(FOO_000001):
            label = ["Test Deprecated Descendant Term"]
            IAO_0000115 = ["Test description"]
            hasExactSynonym = ["Test synonym"]
            deprecated = [True]
            comment = ["Deprecated term", "See Links for more details"]
            IAO_0000233 = ["http://example.org/term_tracker"]
            IAO_0100001 = ["http://ontology.org/FOO_000003"]

        class FOO_000003(FOO_000001):
            label = ["Test Non-Deprecated Descendant Term"]

        class OOF_000001(owlready2.Thing):
            label = ["Test Unrelated Different Ontology Term"]

        class OOF_000002(FOO_000001):
            label = ["Test Descendant Different Ontology Term"]

        class FOO_000004(OOF_000002, FOO_000003):
            label = ["Test Ontology Term With Different Ontology Ancestors"]

    onto.save(file=str(tmp_path.joinpath("test_ontology.owl")))
    return onto


def test_extract_ontology_term_metadata(sample_ontology):
    allowed_ontologies = ["FOO"]
    result = _extract_ontology_term_metadata(
        sample_ontology, allowed_ontologies, map_to_cross_ontologies=[], cross_ontology_map={}
    )

    expected_result = {
        "FOO:000001": {
            "ancestors": {},
            "label": "Test Root Term",
            "deprecated": False,
        },
        "FOO:000002": {
            "ancestors": {"FOO:000001": 1},
            "label": "Test Deprecated Descendant Term",
            "description": "Test description",
            "synonyms": ["Test synonym"],
            "deprecated": True,
            "comments": ["Deprecated term", "See Links for more details"],
            "term_tracker": "http://example.org/term_tracker",
            "replaced_by": "FOO:000003",
        },
        "FOO:000003": {
            "ancestors": {"FOO:000001": 1},
            "label": "Test Non-Deprecated Descendant Term",
            "deprecated": False,
        },
        "FOO:000004": {
            "ancestors": {"FOO:000001": 2, "FOO:000003": 1},
            "label": "Test Ontology Term With Different Ontology Ancestors",
            "deprecated": False,
        },
    }

    assert result == expected_result


def test_extract_ontology_term_metadata_multiple_allowed_ontologies(sample_ontology):
    allowed_ontologies = ["FOO", "OOF"]
    result = _extract_ontology_term_metadata(
        sample_ontology, allowed_ontologies, map_to_cross_ontologies=[], cross_ontology_map={}
    )

    expected_result = {
        "FOO:000001": {
            "ancestors": {},
            "label": "Test Root Term",
            "deprecated": False,
        },
        "FOO:000002": {
            "ancestors": {"FOO:000001": 1},
            "label": "Test Deprecated Descendant Term",
            "description": "Test description",
            "synonyms": ["Test synonym"],
            "deprecated": True,
            "comments": ["Deprecated term", "See Links for more details"],
            "term_tracker": "http://example.org/term_tracker",
            "replaced_by": "FOO:000003",
        },
        "FOO:000003": {
            "ancestors": {"FOO:000001": 1},
            "label": "Test Non-Deprecated Descendant Term",
            "deprecated": False,
        },
        "FOO:000004": {
            "ancestors": {"FOO:000001": 2, "FOO:000003": 1, "OOF:000002": 1},
            "label": "Test Ontology Term With Different Ontology Ancestors",
            "deprecated": False,
        },
        "OOF:000001": {
            "ancestors": {},
            "label": "Test Unrelated Different Ontology Term",
            "deprecated": False,
        },
        "OOF:000002": {
            "ancestors": {"FOO:000001": 1},
            "label": "Test Descendant Different Ontology Term",
            "deprecated": False,
        },
    }

    assert result == expected_result


def test_extract_cross_ontology_terms(mock_raw_ontology_dir, mock_ontology_info):
    cross_ontology_map = _load_cross_ontology_map(mock_raw_ontology_dir, mock_ontology_info)

    assert cross_ontology_map == {"ontology_name": {"OOF:000002": "FOO:000002"}}

    result = _extract_cross_ontology_terms("OOF:000002", ["ontology_name"], cross_ontology_map)

    expected_result = {"ontology_name": "FOO:000002"}

    assert result == expected_result


# ---------------------------------------------------------------------------
# UniProt XML streaming parser
# ---------------------------------------------------------------------------

_UNIPROT_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<uniprot xmlns="http://uniprot.org/uniprot">
  <entry dataset="Swiss-Prot">
    <accession>P05112</accession>
    <name>IL4_HUMAN</name>
  </entry>
  <entry dataset="Swiss-Prot">
    <accession>P08575</accession>
    <name>CD45_HUMAN</name>
  </entry>
</uniprot>
"""


@pytest.fixture
def mock_uniprot_xml_gz(tmp_path):
    xml_gz_path = tmp_path / "UniProt.xml.gz"
    with gzip.open(xml_gz_path, "wb") as f:
        f.write(_UNIPROT_XML.encode("utf-8"))
    return str(xml_gz_path)


def test_parse_uniprot_xml(mock_uniprot_xml_gz):
    result = _parse_uniprot_xml(mock_uniprot_xml_gz)
    assert result == {
        "uniprot:P05112": {"label": "IL4_HUMAN", "deprecated": False, "ancestors": {}},
        "uniprot:P08575": {"label": "CD45_HUMAN", "deprecated": False, "ancestors": {}},
    }


def test_parse_uniprot_xml_skips_entries_without_accession_or_name(tmp_path):
    xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<uniprot xmlns="http://uniprot.org/uniprot">
  <entry dataset="Swiss-Prot">
    <accession>P05112</accession>
  </entry>
  <entry dataset="Swiss-Prot">
    <name>ORPHAN_HUMAN</name>
  </entry>
</uniprot>
"""
    xml_gz_path = tmp_path / "UniProt.xml.gz"
    with gzip.open(xml_gz_path, "wb") as f:
        f.write(xml.encode("utf-8"))
    result = _parse_uniprot_xml(str(xml_gz_path))
    # Entry without <name> and entry without <accession> are both skipped
    assert result == {}


# ---------------------------------------------------------------------------
# xml.gz download path
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_xml_gz_ontology_info():
    return {
        "UniProt": {
            "source": "http://example.com",
            "version": "2025-10-08",
            "filename": "uniprot_sprot.xml.gz",
            "format": "xml.gz",
            "url": "http://example.com/uniprot_sprot.xml.gz",
        }
    }


def test_download_ontologies_xml_gz_format(mock_xml_gz_ontology_info, tmp_path):
    with patch("urllib.request.urlretrieve") as mock_urlretrieve, patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.code = 200
        mock_urlopen.return_value = mock_response

        _download_ontologies(ontology_info=mock_xml_gz_ontology_info, output_dir=str(tmp_path))

        assert mock_urlretrieve.call_count == 1
        saved_path = mock_urlretrieve.call_args[0][1]
        assert saved_path.endswith("UniProt.xml.gz"), f"Expected .xml.gz output, got: {saved_path}"


def test_parse_ontologies_xml_gz(mock_uniprot_xml_gz, tmp_path):
    xml_gz_ontology_info = {
        "UniProt": {
            "source": "http://example.com",
            "version": "2025-10-08",
            "filename": "uniprot_sprot.xml.gz",
            "format": "xml.gz",
        }
    }
    working_dir = str(tmp_path / "raw")
    os.makedirs(working_dir)
    # Place the pre-built xml.gz fixture where _parse_ontologies expects it
    import shutil

    shutil.copy(mock_uniprot_xml_gz, os.path.join(working_dir, "UniProt.xml.gz"))

    output_dir = str(tmp_path / "output")
    os.makedirs(output_dir)

    with patch("all_ontology_generator._load_cross_ontology_map", return_value={}):
        output_files = list(
            _parse_ontologies(ontology_info=xml_gz_ontology_info, working_dir=working_dir, output_path=output_dir)
        )

    assert len(output_files) == 1
    assert output_files[0].endswith("UniProt-ontology-2025-10-08.json.gz")
    assert os.path.isfile(output_files[0])

    with gzip.open(output_files[0], "rt") as f:
        result = json.load(f)

    assert "uniprot:P05112" in result
    assert result["uniprot:P05112"] == {"label": "IL4_HUMAN", "deprecated": False, "ancestors": {}}
