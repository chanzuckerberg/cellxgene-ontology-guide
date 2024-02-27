from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

import pytest
from cellxgene_ontology_guide.artifact_download import load_artifact_by_schema
from cellxgene_ontology_guide.constants import ALL_ONTOLOGY_FILENAME, ONTOLOGY_ASSET_RELEASE_URL


@pytest.fixture
def mock_urlopen():
    """A fixture that mocks urlopen and simulates a successful response."""

    def get_mock_response(url):
        if url.endswith(ALL_ONTOLOGY_FILENAME):
            mock_response = Mock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=None)
            mock_response.read.return_value = b'{"key": "value"}'
            mock_response.status = 200
            return mock_response
        else:
            raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    with patch("cellxgene_ontology_guide.artifact_download.urlopen", side_effect=get_mock_response) as mock:
        yield mock


@pytest.fixture
def mock_urlopen_url_error():
    """A fixture that mocks urlopen and simulates a URLError."""
    with patch(
        "cellxgene_ontology_guide.artifact_download.urlopen", side_effect=URLError(reason="Network Unreachable")
    ) as mock:
        yield mock


def test_load_artifact_by_schema__success(mock_urlopen):
    schema_version = "5.0.0"
    expected_tag = "ontology-assets-v0.0.1"
    expected_resp_content = b'{"key": "value"}'

    result = load_artifact_by_schema(schema_version, ALL_ONTOLOGY_FILENAME)
    expected_download_url = f"{ONTOLOGY_ASSET_RELEASE_URL}/{expected_tag}/{ALL_ONTOLOGY_FILENAME}"

    mock_urlopen.assert_called_once_with(expected_download_url)
    assert result == expected_resp_content


def test_load_artifact_by_schema__unsupported_schema_version(mock_urlopen):
    schema_version = "v0.0.0"
    with pytest.raises(ValueError) as exc_info:
        load_artifact_by_schema(schema_version, ALL_ONTOLOGY_FILENAME)
    assert "Schema version v0.0.0 is not supported in this package version." in str(exc_info.value)
    mock_urlopen.assert_not_called()


def test_load_artifact_by_schema__http_error(mock_urlopen):
    schema_version = "5.0.0"
    filename = "missing.json"
    with pytest.raises(ValueError) as exc_info:
        load_artifact_by_schema(schema_version, filename)
    assert "Could not get missing.json for schema version 5.0.0 in GitHub Release Assets" in str(exc_info.value)
    mock_urlopen.assert_called_once()


def test_load_artifact_by_schema__url_error(mock_urlopen_url_error):
    schema_version = "5.0.0"
    filename = "all_ontology.json.gz"
    with pytest.raises(ValueError) as exc_info:
        load_artifact_by_schema(schema_version, filename)
    assert "URL error occurred: Network Unreachable" in str(exc_info.value)
    mock_urlopen_url_error.assert_called_once()
