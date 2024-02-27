import os
import urllib.request
from unittest.mock import MagicMock, patch

import pytest
from all_ontology_generator import _download_ontologies, _parse_ontologies


@pytest.fixture
def mock_ontology_info(tmpdir):
    # Create a temporary ontology info file
    onto_info_file = tmpdir.join("ontology_info.json")
    onto_info_file.write('{"ontology_name": {"source": "http://example.com", "version": "v1", "filetype": "owl"}}')
    return str(onto_info_file)


@pytest.fixture
def mock_raw_ontology_dir(tmpdir):
    # Create a temporary directory for raw ontology files
    raw_ontology_dir = tmpdir.mkdir("raw_ontology")
    return str(raw_ontology_dir)


@pytest.fixture
def mock_parsed_ontology_file(tmpdir):
    # Create a temporary gzipped json file for parsed ontology data
    parsed_ontology_file = tmpdir.join("parsed_ontologies.json.gz")
    return str(parsed_ontology_file)


def test_download_ontologies(mock_ontology_info, mock_raw_ontology_dir):
    # Mocking urllib.request.urlretrieve, urllib.request.urlopen
    with patch("urllib.request.urlretrieve") as mock_urlretrieve, patch("urllib.request.urlopen") as mock_urlopen:
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.code = 200
        mock_urlopen.return_value = mock_response

        # Call the function
        _download_ontologies(onto_info_file=mock_ontology_info, output_dir=mock_raw_ontology_dir)

        mock_urlretrieve.assert_called_once()


def test_parse_ontologies(mock_raw_ontology_dir, mock_parsed_ontology_file):
    # Mocking _load_ontology_object and _extract_ontology_term_metadata
    with patch("all_ontology_generator._load_ontology_object") as mock_load_ontology, patch(
        "all_ontology_generator._extract_ontology_term_metadata"
    ) as mock_extract_metadata:
        # Mock return values
        mock_load_ontology.return_value = MagicMock(name="ontology_object")
        mock_extract_metadata.return_value = {"term_id": {"label": "Term Label", "deprecated": False, "ancestors": []}}

        # Call the function
        _parse_ontologies(working_dir=mock_raw_ontology_dir, output_json_file=mock_parsed_ontology_file)

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
            _download_ontologies(onto_info_file=mock_ontology_info, output_dir=mock_raw_ontology_dir)
        assert "returns status code 404" in str(exc_info.value)


def test_download_ontologies_url_error(mock_ontology_info, mock_raw_ontology_dir):
    # Mocking urllib.request.urlopen to raise URLError
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError(reason="Connection refused")

        # Assertion
        with pytest.raises(Exception) as exc_info:
            _download_ontologies(onto_info_file=mock_ontology_info, output_dir=mock_raw_ontology_dir)
        assert "fails due to Connection refused" in str(exc_info.value)
