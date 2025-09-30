"""Configuration for Docker images used in the project."""

import os
from pathlib import Path
from typing import Dict, Optional

# Cache for docker images
_docker_images: Optional[Dict[str, str]] = None


def _load_docker_images() -> Dict[str, str]:
    """
    Load all docker images from docker-versions.env file.

    :rtype Dict[str, str]
    :return: Dictionary mapping environment variable names to docker image strings
    """
    global _docker_images
    if _docker_images is not None:
        return _docker_images

    result = {}
    env_path = Path(__file__).parent.parent / "docker-versions.env"
    try:
        with open(env_path) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):  # allow comments
                    key, value = line.strip().split("=", 1)
                    result[key] = value
    except FileNotFoundError:
        pass

    _docker_images = result
    return result


def get_docker_image(key: str) -> str:
    """
    Get a docker image from environment or docker-versions.env file.

    :param str key: The environment variable name to look for
    :rtype str
    :return: The docker image string (e.g., "obolibrary/robot:v1.9.8")
    :raises ValueError: If the docker image is not found in environment or docker-versions.env
    """
    # First check environment variable for override
    if image := os.getenv(key):
        return image

    # Check cached images
    images = _load_docker_images()
    if key in images:
        return images[key]

    raise ValueError(f"Docker image {key} not found in environment or docker-versions.env")
