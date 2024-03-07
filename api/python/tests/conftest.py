from unittest.mock import patch

import pytest


@pytest.fixture
def mock_load_supported_versions(tmpdir):
    with patch("cellxgene_ontology_guide.supported_versions.load_supported_versions") as mock:
        yield mock


@pytest.fixture
def mock_load_ontology_file():
    with patch("cellxgene_ontology_guide.supported_versions.load_ontology_file") as mock:
        yield mock
