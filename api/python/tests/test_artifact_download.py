import os

import pytest
from cellxgene_ontology_guide.artifact_download import load_artifact_by_schema
from cellxgene_ontology_guide.constants import ARTIFACT_DIR, CURRENT_SCHEMA_VERSION


def test_load_artifact_by_schema():
    assert load_artifact_by_schema(CURRENT_SCHEMA_VERSION, "ontology_info.yml") == os.path.join(
        ARTIFACT_DIR, "ontology_info.yml"
    )
    assert load_artifact_by_schema(CURRENT_SCHEMA_VERSION, "all_ontology.json.gz") == os.path.join(
        ARTIFACT_DIR, "all_ontology.json.gz"
    )


def test_load_artifact_by_schema_raises_value_error():
    with pytest.raises(ValueError):
        load_artifact_by_schema("0.0.0", "ontology_info.yml")
