import json
import os

import pytest
import zstandard as zstd
from referencing import Resource
from validate_json_schemas import get_schema_file_name, register_schemas, verify_json


@pytest.fixture
def schema_file_fixture(tmpdir):
    # Create a temporary schema file
    schema_data = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
        "required": ["name", "age"],
    }
    schema_file = tmpdir.join("schema.json")
    with open(str(schema_file), "w") as f:
        json.dump(schema_data, f)
    return str(schema_file)


@pytest.fixture
def registry_fixture(schema_file_fixture, tmpdir):
    return register_schemas(tmpdir)


def test_get_schema_file_name(tmpdir):
    # Create a temporary JSON file
    json_file = "test.json"

    # Assert the output file name is correct
    assert get_schema_file_name(str(json_file), tmpdir) == str(tmpdir.join("test_schema.json"))


def test_register_schemas(schema_file_fixture, tmpdir):
    registry = register_schemas(tmpdir)
    assert isinstance(registry["schema.json"], Resource)


def test_register_schema_invalid_json(tmpdir):
    # Create an invalid schema file
    schema_file = tmpdir.join("invalid_schema.json")
    with open(str(schema_file), "w") as f:
        f.write("invalid_schema")

    # Assert an exception is raised
    with pytest.raises(json.decoder.JSONDecodeError):
        register_schemas(tmpdir)


class TestVerifyJson:
    def test_valid_json(self, schema_file_fixture, tmpdir, registry_fixture):
        # Create a valid JSON file
        json_data = {"name": "John", "age": 30}
        json_file = tmpdir.join("valid.json")
        with open(str(json_file), "w") as f:
            json.dump(json_data, f)

        # Assert validation passes
        assert verify_json(schema_file_fixture, str(json_file), registry_fixture) is True

    def test_valid_json_zst(self, schema_file_fixture, tmpdir, registry_fixture):
        # Create a valid JSON GZ file
        json_data = {"name": "John", "age": 30}
        json_file = tmpdir.join("valid.json.zst")
        cctx = zstd.ZstdCompressor(level=22)  # Maximum compression level for zstd
        compressed = cctx.compress(json.dumps(json_data, separators=(",", ":")).encode("utf-8"))
        with open(json_file, "wb") as fp:
            fp.write(compressed)

        # Assert validation passes
        assert verify_json(schema_file_fixture, str(json_file), registry_fixture) is True

    def test_invalid_json(self, schema_file_fixture, tmpdir, registry_fixture):
        # Create an invalid JSON file
        json_data = {"name": "John"}
        json_file = tmpdir.join("invalid.json")
        with open(str(json_file), "w") as f:
            json.dump(json_data, f)

        # Assert validation fails
        assert verify_json(schema_file_fixture, str(json_file), registry_fixture) is False

    def test_missing_schema_file(self, tmpdir, registry_fixture):
        # Create a JSON file
        json_data = {"name": "John", "age": 30}
        json_file = tmpdir.join("missing_schema.json")
        with open(str(json_file), "w") as f:
            json.dump(json_data, f)

        # Assert validation fails due to missing schema file
        assert verify_json("nonexistent_schema.json", str(json_file), registry_fixture) is False

    def test_missing_json_file(self, schema_file_fixture, registry_fixture):
        # Assert validation fails due to missing JSON file
        assert verify_json(schema_file_fixture, "nonexistent_json.json", registry_fixture) is False

    def test_invalid_schema(self, schema_file_fixture, tmpdir, registry_fixture):
        # Create an invalid schema file
        with open(schema_file_fixture, "w") as f:
            f.write("invalid_schema")

        # Create a JSON file
        json_data = {"name": "John", "age": 30}
        json_file = tmpdir.join("invalid_schema.json")
        with open(str(json_file), "w") as f:
            json.dump(json_data, f)

        # Assert validation fails due to invalid schema
        assert verify_json(schema_file_fixture, str(json_file), registry_fixture) is False


class TestVerifyJsonCustomLogic:
    @pytest.fixture
    def ontology_info_schema_file_fixture(self, tmpdir):
        ontology_info_schema = os.path.join(
            os.path.realpath(__file__).rsplit("/", maxsplit=4)[0], "asset-schemas", "ontology_info_schema.json"
        )
        with open(ontology_info_schema, "r") as f:
            schema_data = json.load(f)
        schema_file = tmpdir.join("ontology_info_schema.json")
        with open(str(schema_file), "w") as f:
            json.dump(schema_data, f)
        return str(schema_file)

    @pytest.fixture
    def ontology_info_registry_fixture(self, ontology_info_schema_file_fixture, tmpdir):
        return register_schemas(tmpdir)

    @pytest.fixture
    def ontology_info_json_data(self):
        return {
            "2.0.0": {
                "ontologies": {
                    "A": {
                        "version": "v1",
                        "source": "https://example.org/ontology/download",
                        "filename": "a.owl",
                        "additional_ontologies": ["C"],
                    },
                    "B": {
                        "version": "v2",
                        "source": "https://example.org/ontology/download",
                        "filename": "b.owl",
                        "additional_ontologies": ["D"],
                    },
                }
            },
            "1.0.0": {
                "ontologies": {
                    "A": {
                        "version": "v1",
                        "source": "https://example.org/ontology/download",
                        "filename": "a.owl",
                    },
                    "B": {
                        "version": "v1",
                        "source": "https://example.org/ontology/download",
                        "filename": "b.owl",
                    },
                }
            },
        }

    def test_validate_unique_ontologies(
        self, ontology_info_json_data, ontology_info_schema_file_fixture, tmpdir, ontology_info_registry_fixture
    ):
        json_file = tmpdir.join("ontology_info.json")
        with open(str(json_file), "w") as f:
            json.dump(ontology_info_json_data, f)

        # Assert validation passes
        assert verify_json(ontology_info_schema_file_fixture, str(json_file), ontology_info_registry_fixture) is True
