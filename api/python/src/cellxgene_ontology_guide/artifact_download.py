import os

from constants import ARTIFACT_DIR


def load_artifact_by_schema(schema_version: str, filename: str) -> str:
    """
    Load ontology files from GitHub Release Assets, based on the provided schema version.
    Returns ValueError if the schema version is not supported in this package version.

    :param schema_version: str version of the schema to load ontology files for
    :param filename: str name of the file to load
    :return: str path to the ontology file
    """
    artifact_filepath = os.path.join(ARTIFACT_DIR, schema_version, filename)
    if os.path.isfile(artifact_filepath):
        return artifact_filepath
    else:
        # TODO: Add support for loading ontology files from different schema versions
        raise ValueError(f"Schema version {schema_version} is not supported in this package version.")
