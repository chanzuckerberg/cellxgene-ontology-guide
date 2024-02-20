import json

import pytest
from curation_list_validation import verify_json


@pytest.fixture
def schema_file(tmpdir):
    # Create a temporary schema file
    schema_data = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
        "required": ["name", "age"],
    }
    schema_file = tmpdir.join("schema.json")
    with open(str(schema_file), "w") as f:
        json.dump(schema_data, f)
    return str(schema_file)


class TestVerifyJson:
    def test_valid_json(self, schema_file, tmpdir):
        # Create a valid JSON file
        json_data = {"name": "John", "age": 30}
        json_file = tmpdir.join("valid.json")
        with open(str(json_file), "w") as f:
            json.dump(json_data, f)

        # Assert validation passes
        assert verify_json(schema_file, str(json_file)) is True

    def test_invalid_json(self, schema_file, tmpdir):
        # Create an invalid JSON file
        json_data = {"name": "John"}
        json_file = tmpdir.join("invalid.json")
        with open(str(json_file), "w") as f:
            json.dump(json_data, f)

        # Assert validation fails
        assert verify_json(schema_file, str(json_file)) is False

    def test_missing_schema_file(self, tmpdir):
        # Create a JSON file
        json_data = {"name": "John", "age": 30}
        json_file = tmpdir.join("missing_schema.json")
        with open(str(json_file), "w") as f:
            json.dump(json_data, f)

        # Assert validation fails due to missing schema file
        assert verify_json("nonexistent_schema.json", str(json_file)) is False

    def test_missing_json_file(self, schema_file):
        # Assert validation fails due to missing JSON file
        assert verify_json(schema_file, "nonexistent_json.json") is False

    def test_invalid_schema(self, schema_file, tmpdir):
        # Create an invalid schema file
        with open(schema_file, "w") as f:
            f.write("invalid_schema")

        # Create a JSON file
        json_data = {"name": "John", "age": 30}
        json_file = tmpdir.join("invalid_schema.json")
        with open(str(json_file), "w") as f:
            json.dump(json_data, f)

        # Assert validation fails due to invalid schema
        assert verify_json(schema_file, str(json_file)) is False
