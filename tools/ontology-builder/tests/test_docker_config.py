"""Tests for docker_config.py."""

import os
from unittest.mock import mock_open, patch

import pytest
from src import docker_config


@pytest.fixture
def mock_env_file():
    """Sample content for docker-versions.env."""
    return (
        "ROBOT_DOCKER_IMAGE=obolibrary/robot:v1.9.8\n"
        "OTHER_DOCKER_IMAGE=example/image:v2.0.0\n"
        "# This is a comment\n"
        "EMPTY_DOCKER_IMAGE=\n"
    )


@pytest.fixture
def reset_docker_images():
    """Reset the cached docker images before each test."""
    docker_config._docker_images = None
    yield
    docker_config._docker_images = None


def test_load_docker_images(mock_env_file, reset_docker_images):
    """Test loading docker images from file."""
    with patch("builtins.open", mock_open(read_data=mock_env_file)):
        images = docker_config._load_docker_images()
        assert images == {
            "ROBOT_DOCKER_IMAGE": "obolibrary/robot:v1.9.8",
            "OTHER_DOCKER_IMAGE": "example/image:v2.0.0",
            "EMPTY_DOCKER_IMAGE": "",
        }


def test_load_docker_images_caching(mock_env_file, reset_docker_images):
    """Test that docker images are properly cached."""
    with patch("builtins.open", mock_open(read_data=mock_env_file)):
        # First call should read the file
        images1 = docker_config._load_docker_images()

        # Modify the cache to verify second call uses it
        docker_config._docker_images["TEST"] = "test"

        # Second call should use cache
        images2 = docker_config._load_docker_images()

        assert images1 != images2
        assert "TEST" in images2


def test_load_docker_images_file_not_found(reset_docker_images):
    """Test handling of missing docker-versions.env file."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        images = docker_config._load_docker_images()
        assert images == {}


def test_get_docker_image_from_env(reset_docker_images):
    """Test getting docker image from environment variable."""
    with patch.dict(os.environ, {"TEST_DOCKER_IMAGE": "test/image:v1.0.0"}):
        image = docker_config.get_docker_image("TEST_DOCKER_IMAGE")
        assert image == "test/image:v1.0.0"


def test_get_docker_image_from_file(mock_env_file, reset_docker_images):
    """Test getting docker image from docker-versions.env file."""
    with patch("builtins.open", mock_open(read_data=mock_env_file)):
        image = docker_config.get_docker_image("ROBOT_DOCKER_IMAGE")
        assert image == "obolibrary/robot:v1.9.8"


def test_get_docker_image_not_found(reset_docker_images):
    """Test error when docker image is not found."""
    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(ValueError) as exc_info:
            docker_config.get_docker_image("NONEXISTENT_DOCKER_IMAGE")
        assert "not found in environment or docker-versions.env" in str(exc_info.value)


def test_get_docker_image_empty_value(mock_env_file, reset_docker_images):
    """Test handling of empty docker image value."""
    with patch("builtins.open", mock_open(read_data=mock_env_file)):
        image = docker_config.get_docker_image("EMPTY_DOCKER_IMAGE")
        assert image == ""


def test_get_docker_image_env_precedence(mock_env_file, reset_docker_images):
    """Test that environment variables take precedence over file values."""
    env_value = "env/image:latest"
    with (
        patch.dict(os.environ, {"ROBOT_DOCKER_IMAGE": env_value}),
        patch("builtins.open", mock_open(read_data=mock_env_file)),
    ):
        image = docker_config.get_docker_image("ROBOT_DOCKER_IMAGE")
        assert image == env_value
