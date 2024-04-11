import gzip
import json
from unittest.mock import patch

import pytest
from cellxgene_ontology_guide.entities import Ontology
from cellxgene_ontology_guide.supported_versions import (
    CXGSchema,
    get_latest_schema_version,
    load_ontology_file,
    load_supported_versions,
)

MODULE_PATH = "cellxgene_ontology_guide.supported_versions"


@pytest.fixture
def initialized_CXGSchemaInfo(mock_load_supported_versions):
    mock_load_supported_versions.return_value = {
        "5.0.0": {
            "ontologies": {"CL": {"version": "v2024-01-01", "source": "http://example.com", "filename": "cl.owl"}}
        }
    }
    return CXGSchema()


@pytest.mark.parametrize("versions, expected", [(["v5.0.0", "v0.0.1"], "v5.0.0"), (["5.0.0", "0.0.1"], "v5.0.0")])
def test__get_latest_schema_version__OK(versions, expected):
    assert get_latest_schema_version(versions) == "5.0.0"


@pytest.fixture
def mock_ontology_file(tmpdir):
    with patch(f"{MODULE_PATH}.DATA_ROOT", tmpdir):
        # Create a temporary ontology file
        test_file_name = "test_ontology.json.gz"
        onto_file = tmpdir.join(test_file_name)
        file_contents = {"test": "file contents"}
        with gzip.open(str(onto_file), "wt") as onto_file:
            json.dump(file_contents, onto_file)
        yield test_file_name, file_contents


def test__load_ontology_file__OK(mock_ontology_file):
    test_file_name, file_contents = mock_ontology_file
    assert load_ontology_file(test_file_name) == file_contents
    assert load_ontology_file.cache_info().hits == 0
    assert load_ontology_file.cache_info().misses == 1
    load_ontology_file(test_file_name)
    assert load_ontology_file.cache_info().hits == 1
    assert load_ontology_file.cache_info().misses == 1


def test__clear_ontology_file_cache__OK(mock_ontology_file):
    test_file_name, _ = mock_ontology_file
    load_ontology_file(test_file_name)
    assert load_ontology_file.cache_info().misses == 1
    load_ontology_file.cache_clear()
    assert load_ontology_file.cache_info().misses == 0
    load_ontology_file(test_file_name)
    assert load_ontology_file.cache_info().misses == 1


def test__load_supported_versions__OK(tmpdir):
    with patch(f"{MODULE_PATH}.DATA_ROOT", tmpdir):
        # Create a temporary ontology_info.json file
        test_file_name = tmpdir.join("ontology_info.json")
        file_contents = {"test": "file contents"}
        with test_file_name.open("w") as f:
            json.dump(file_contents, f)
        assert load_supported_versions() == file_contents


@pytest.mark.parametrize("version, expected", [("v5.0.0", "5.0.0"), ("5.0.0", "5.0.0")])
def test_coerce_version(version, expected):
    assert get_latest_schema_version([version]) == expected


class TestCXGSchema:
    def test__init__defaults(self, mock_load_supported_versions):
        support_versions = {"5.0.0": {"ontologies": {}}, "0.0.1": {"ontologies": {}}}
        mock_load_supported_versions.return_value = support_versions
        cxgs = CXGSchema()
        assert cxgs.version == "5.0.0"
        assert cxgs.supported_ontologies == support_versions["5.0.0"]["ontologies"]

    @pytest.mark.parametrize("version", ["v0.0.1", "0.0.1"])
    def test__init__specific_version(self, version, mock_load_supported_versions):
        support_versions = {"5.0.0": {"ontologies": {}}, "0.0.1": {"ontologies": {}}}
        mock_load_supported_versions.return_value = support_versions
        cxgs = CXGSchema(version=version)
        assert cxgs.version == "0.0.1"
        assert cxgs.supported_ontologies == support_versions["0.0.1"]["ontologies"]

    def test__init__deprecated_version(self, mock_load_supported_versions):
        support_versions = {"5.0.0": {"ontologies": {}}, "0.0.1": {"ontologies": {}, "deprecated_on": "2024-01-01"}}
        mock_load_supported_versions.return_value = support_versions
        # catch the deprecation warning
        with pytest.warns(DeprecationWarning) as record:
            CXGSchema(version="0.0.1")
        warning = record.pop()
        assert warning.message.args[0] == (
            "Schema version 0.0.1 is deprecated as of 2024-01-01 00:00:00. It will be removed in a " "future version."
        )

    def test__init__unsupported_version(self, mock_load_supported_versions):
        mock_load_supported_versions.return_value = {}
        with pytest.raises(ValueError):
            CXGSchema(version="5.0.1")

    def test__ontology__unsupported_ontology_by_package(self, initialized_CXGSchemaInfo, mock_load_ontology_file):
        with pytest.raises(ValueError):
            initialized_CXGSchemaInfo.ontology("GO")
        mock_load_ontology_file.assert_not_called()

    def test__ontology__unsupported_ontology_by_schema(self, initialized_CXGSchemaInfo, mock_load_ontology_file):
        with pytest.raises(ValueError):
            initialized_CXGSchemaInfo.ontology("EFO")
        mock_load_ontology_file.assert_not_called()

    def test__ontology__OK(self, initialized_CXGSchemaInfo, mock_load_ontology_file):
        ontology_file_contents = {"CL:1234": "efgh"}
        mock_load_ontology_file.return_value = ontology_file_contents
        assert initialized_CXGSchemaInfo.ontology("CL") == {"CL:1234": "efgh"}


def test_get_ontology_download_url(initialized_CXGSchemaInfo, mock_load_ontology_file):
    assert initialized_CXGSchemaInfo.get_ontology_download_url(Ontology.CL) == "http://example.com/v2024-01-01/cl.owl"
