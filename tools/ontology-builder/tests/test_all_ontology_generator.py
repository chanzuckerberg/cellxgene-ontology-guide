import json
import os
import urllib.request
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from all_ontology_generator import (
    _download_ontologies,
    _get_latest_version,
    _parse_ontologies,
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
    return str(sub_dir)


def test_get_latest_version():
    # Call the function
    latest_version = _get_latest_version(versions=["v1", "v2.0", "v3.0.0", "v3.0.1", "v3.1.0"])

    # Assertion
    assert latest_version == "v3.1.0"


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

        mock_urlretrieve.assert_called_once()


def test_parse_ontologies(mock_ontology_info, mock_raw_ontology_dir, tmpdir):
    # Mocking _load_ontology_object and _extract_ontology_term_metadata
    with (
        patch("all_ontology_generator._load_ontology_object") as mock_load_ontology,
        patch("all_ontology_generator._extract_ontology_term_metadata") as mock_extract_metadata,
    ):
        # Mock return values
        MockOntologyObject = MagicMock()
        MockOntologyObject.name = "ontology_name"  # Must match the name of the ontology file
        mock_load_ontology.return_value = MockOntologyObject
        mock_extract_metadata.return_value = {"term_id": {"label": "Term Label", "deprecated": False, "ancestors": {}}}

        # Mock output path
        output_path = tmpdir.mkdir("output")
        # Call the function
        output_files = _parse_ontologies(
            ontology_info=mock_ontology_info, working_dir=mock_raw_ontology_dir, output_path=output_path
        )

        # Assert the output file is created
        assert all(os.path.isfile(file) for file in output_files)

        # Assert output_path has the same number of files as mock_raw_ontology_dir.
        assert len(os.listdir(output_path)) == len(os.listdir(mock_raw_ontology_dir))

        # Assert _load_ontology_object is called for each ontology file
        assert mock_load_ontology.call_count == len(os.listdir(mock_raw_ontology_dir))

        # Assert _extract_ontology_term_metadata is called for each ontology object
        assert mock_extract_metadata.call_count == len(os.listdir(mock_raw_ontology_dir))


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
