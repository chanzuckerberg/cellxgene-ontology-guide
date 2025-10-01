import gzip
import json
import os
import subprocess
from unittest.mock import MagicMock, patch

import owlready2
import pytest
from all_ontology_generator import (
    _convert_obo_to_owl,
    _get_ancestors,
    _load_ontology_object,
    get_ontology_file_name,
    save_ontology_info,
)
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

    def test_valid_json_gz(self, schema_file_fixture, tmpdir, registry_fixture):
        # Create a valid JSON GZ file
        json_data = {"name": "John", "age": 30}
        json_file = tmpdir.join("valid.json.gz")
        with gzip.open(str(json_file), "wt") as f:
            json.dump(json_data, f)

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


class TestGetAncestors:
    def test_get_ancestors_no_ancestors(self, sample_ontology):
        """Test handling of a class with no ancestors."""
        # Get the root class which should have no ancestors
        root_class = sample_ontology.FOO_000001
        allowed_ontologies = ["FOO"]

        result = _get_ancestors(root_class, allowed_ontologies)
        assert result == {}

    def test_get_ancestors_with_ancestors(self, sample_ontology):
        """Test handling of a class with ancestors."""
        # Get a class with known ancestors
        test_class = sample_ontology.FOO_000002
        allowed_ontologies = ["FOO"]

        result = _get_ancestors(test_class, allowed_ontologies)
        assert "FOO:000001" in result
        assert result["FOO:000001"] == 1  # Distance should be 1

    def test_get_ancestors_with_multiple_ancestors(self, sample_ontology):
        """Test handling of a class with multiple ancestors."""
        # Get a class with multiple ancestors
        test_class = sample_ontology.FOO_000004
        allowed_ontologies = ["FOO"]

        result = _get_ancestors(test_class, allowed_ontologies)
        assert "FOO:000001" in result
        assert "FOO:000003" in result
        assert result["FOO:000001"] == 2  # Distance should be 2
        assert result["FOO:000003"] == 1  # Distance should be 1

    def test_get_ancestors_with_filtered_ontologies(self, sample_ontology):
        """Test filtering of ancestors based on allowed ontologies."""
        # Get a class with ancestors from different ontologies
        test_class = sample_ontology.FOO_000004
        allowed_ontologies = ["FOO"]  # Only allow FOO ontology

        result = _get_ancestors(test_class, allowed_ontologies)
        # Should not include OOF:000002 as it's not in allowed_ontologies
        assert "OOF:000002" not in result
        assert "FOO:000001" in result
        assert "FOO:000003" in result

    def test_get_ancestors_with_multiple_allowed_ontologies(self, sample_ontology):
        """Test handling of multiple allowed ontologies."""
        # Get a class with ancestors from different ontologies
        test_class = sample_ontology.FOO_000004
        allowed_ontologies = ["FOO", "OOF"]  # Allow both ontologies

        result = _get_ancestors(test_class, allowed_ontologies)
        # Should include ancestors from both ontologies
        assert "OOF:000002" in result
        assert "FOO:000001" in result
        assert "FOO:000003" in result

    def test_get_ancestors_with_part_of_relationship(self, sample_ontology):
        """Test handling of part_of relationships."""
        # Create a class with a part_of relationship
        with sample_ontology:

            class BFO_0000050(owlready2.ObjectProperty):
                namespace = sample_ontology

            class FOO_000005(sample_ontology.FOO_000001):
                is_a = [BFO_0000050.some(sample_ontology.FOO_000003)]

        test_class = sample_ontology.FOO_000005
        allowed_ontologies = ["FOO"]

        result = _get_ancestors(test_class, allowed_ontologies)
        assert "FOO:000001" in result
        assert "FOO:000003" in result

    def test_get_ancestors_with_empty_allowed_ontologies(self, sample_ontology):
        """Test handling of empty allowed_ontologies list."""
        test_class = sample_ontology.FOO_000002
        allowed_ontologies = []

        result = _get_ancestors(test_class, allowed_ontologies)
        assert result == {}  # Should return empty dict when no ontologies are allowed


class TestGetOntologyFileName:
    def test_get_ontology_file_name_basic(self):
        """Test basic file name generation."""
        ontology_name = "TEST"
        version = "1.0.0"
        expected = "TEST-ontology-1.0.0.json.zst"

        result = get_ontology_file_name(ontology_name, version)
        assert result == expected

    def test_get_ontology_file_name_with_special_chars(self):
        """Test file name generation with special characters."""
        ontology_name = "TEST-123"
        version = "v1.0.0-beta"
        expected = "TEST-123-ontology-v1.0.0-beta.json.zst"

        result = get_ontology_file_name(ontology_name, version)
        assert result == expected

    def test_get_ontology_file_name_empty_strings(self):
        """Test file name generation with empty strings."""
        result = get_ontology_file_name("", "")
        assert result == "-ontology-.json.zst"

    def test_get_ontology_file_name_non_string_inputs(self):
        """Test file name generation with non-string inputs."""
        ontology_name = 123
        version = 1.0
        expected = "123-ontology-1.0.json.zst"

        result = get_ontology_file_name(ontology_name, version)
        assert result == expected


class TestSaveOntologyInfo:
    def test_save_ontology_info_success(self, tmp_path):
        """Test successful saving of ontology information."""
        # Create test data
        ontology_info = {"version": "1.0.0", "ontologies": {"TEST": {"version": "1.0", "source": "http://example.com"}}}
        latest_ontology_info = {
            "version": "1.0.0",
            "ontologies": {"TEST": {"version": "1.0", "source": "http://example.com"}},
        }

        # Create output file paths
        ontology_info_file = tmp_path / "ontology_info.json"
        latest_ontology_info_file = tmp_path / "latest_ontology_info.json"

        # Test saving the ontology information
        save_ontology_info(ontology_info, latest_ontology_info, str(ontology_info_file), str(latest_ontology_info_file))

        # Verify the files were created and contain correct data
        assert ontology_info_file.exists()
        assert latest_ontology_info_file.exists()

        with open(ontology_info_file) as f:
            saved_info = json.load(f)
            assert saved_info == ontology_info

        with open(latest_ontology_info_file) as f:
            saved_latest_info = json.load(f)
            assert saved_latest_info == latest_ontology_info

    def test_save_ontology_info_permission_error(self, tmp_path):
        """Test handling of permission error when saving files."""
        # Create test data
        ontology_info = {"test": "data"}
        latest_ontology_info = {"test": "latest"}

        # Create a read-only directory
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        ontology_info_file = readonly_dir / "ontology_info.json"
        latest_ontology_info_file = readonly_dir / "latest_ontology_info.json"

        # Make the directory read-only
        os.chmod(readonly_dir, 0o444)

        # Test that saving raises an error
        with pytest.raises(PermissionError):
            save_ontology_info(
                ontology_info, latest_ontology_info, str(ontology_info_file), str(latest_ontology_info_file)
            )

        # Clean up by making the directory writable again
        os.chmod(readonly_dir, 0o777)

    def test_save_ontology_info_invalid_path(self, tmp_path):
        """Test handling of invalid file paths."""
        # Create test data
        ontology_info = {"test": "data"}
        latest_ontology_info = {"test": "latest"}

        # Use non-existent directory in path
        ontology_info_file = tmp_path / "nonexistent" / "ontology_info.json"
        latest_ontology_info_file = tmp_path / "nonexistent" / "latest_ontology_info.json"

        # Test that saving raises an error
        with pytest.raises(FileNotFoundError):
            save_ontology_info(
                ontology_info, latest_ontology_info, str(ontology_info_file), str(latest_ontology_info_file)
            )

    def test_save_ontology_info_invalid_json(self, tmp_path):
        """Test handling of invalid JSON data."""
        # Create test data with non-serializable object
        ontology_info = {"test": object()}  # object() is not JSON serializable
        latest_ontology_info = {"test": "latest"}

        # Create output file paths
        ontology_info_file = tmp_path / "ontology_info.json"
        latest_ontology_info_file = tmp_path / "latest_ontology_info.json"

        # Test that saving raises an error
        with pytest.raises(TypeError):
            save_ontology_info(
                ontology_info, latest_ontology_info, str(ontology_info_file), str(latest_ontology_info_file)
            )


class TestLoadOntologyObject:
    def test_load_ontology_object_success(self, tmp_path):
        """Test successful loading of an ontology file."""
        # Create a simple test ontology file
        owl_file = tmp_path / "test.owl"
        owl_content = """<?xml version="1.0"?>
        <rdf:RDF xmlns="http://test.org/onto.owl#"
                 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                 xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                 xmlns:owl="http://www.w3.org/2002/07/owl#">
            <owl:Ontology rdf:about="http://test.org/onto.owl"/>
            <owl:Class rdf:about="#TestClass">
                <rdfs:label>Test Class</rdfs:label>
            </owl:Class>
        </rdf:RDF>"""
        owl_file.write_text(owl_content)

        # Test loading the ontology
        onto = _load_ontology_object(str(owl_file))

        # Verify the ontology was loaded correctly
        assert onto is not None
        assert isinstance(onto, owlready2.namespace.Ontology)

    def test_load_ontology_object_invalid_file(self, tmp_path):
        """Test handling of invalid ontology file."""
        # Create an invalid ontology file
        owl_file = tmp_path / "invalid.owl"
        owl_file.write_text("This is not a valid OWL file")

        # Test that loading raises an error
        with pytest.raises(ValueError) as exc_info:
            _load_ontology_object(str(owl_file))
        assert "Could not load ontology" in str(exc_info.value)  # Keep this one as is since it's from owlready2


class TestConvertOboToOwl:
    def test_convert_obo_to_owl_success(self, tmp_path):
        """Test successful conversion of OBO to OWL."""
        # Create test OBO file
        obo_file = tmp_path / "test.obo"
        obo_file.write_text("format-version: 1.2\nontology: test\n")

        # Output OWL file path
        owl_file = tmp_path / "test.owl"

        # Mock successful Docker command execution
        with (
            patch("subprocess.run") as mock_run,
            patch("docker_config.get_docker_image", return_value="test-robot-image"),
        ):
            mock_run.return_value = MagicMock(stdout="Conversion successful", returncode=0)

            # Test conversion
            _convert_obo_to_owl(str(obo_file), str(owl_file))

            # Verify Docker command was called correctly
            mock_run.assert_called_once()
            cmd_args = mock_run.call_args[0][0]
            assert "docker" in cmd_args
            assert "robot" in cmd_args
            assert "convert" in cmd_args
            assert "--format" in cmd_args
            assert "owl" in cmd_args

    def test_convert_obo_to_owl_docker_error(self, tmp_path):
        """Test handling of Docker command failure."""
        # Create test OBO file
        obo_file = tmp_path / "test.obo"
        obo_file.write_text("format-version: 1.2\nontology: test\n")

        # Output OWL file path
        owl_file = tmp_path / "test.owl"

        # Mock Docker command failure
        with (
            patch("subprocess.run") as mock_run,
            patch("docker_config.get_docker_image", return_value="test-robot-image"),
        ):
            mock_run.side_effect = subprocess.CalledProcessError(
                returncode=1, cmd="docker run", output="Error output", stderr="Error message"
            )

            # Test that conversion raises error
            with pytest.raises(subprocess.CalledProcessError):
                _convert_obo_to_owl(str(obo_file), str(owl_file))

    def test_convert_obo_to_owl_docker_not_found(self, tmp_path):
        """Test handling of Docker not being installed."""
        # Create test OBO file
        obo_file = tmp_path / "test.obo"
        obo_file.write_text("format-version: 1.2\nontology: test\n")

        # Output OWL file path
        owl_file = tmp_path / "test.owl"

        # Mock Docker command not found
        with (
            patch("subprocess.run") as mock_run,
            patch("docker_config.get_docker_image", return_value="test-robot-image"),
        ):
            mock_run.side_effect = FileNotFoundError()

            # Test that conversion raises error
            with pytest.raises(FileNotFoundError):
                _convert_obo_to_owl(str(obo_file), str(owl_file))

    def test_convert_obo_to_owl_invalid_paths(self, tmp_path):
        """Test handling of invalid file paths."""
        # Test with non-existent input file
        with pytest.raises(FileNotFoundError):
            _convert_obo_to_owl(str(tmp_path / "nonexistent.obo"), str(tmp_path / "output.owl"))


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
