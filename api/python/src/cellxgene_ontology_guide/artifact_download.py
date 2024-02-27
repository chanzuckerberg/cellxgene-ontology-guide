from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from constants import ONTOLOGY_ASSET_RELEASE_URL, SCHEMA_VERSION_TO_ONTOLOGY_ASSET_TAG


def load_artifact_by_schema(schema_version: str, filename: str) -> bytes:
    """
    Load ontology files from GitHub Release Assets, based on the provided schema version.
    Returns ValueError if the schema version is not supported in this package version or filename is not found for
    given schema_version.

    :param schema_version: str version of the schema to load ontology assets for
    :param filename: str name of the asset to load
    :return: bytes content of the asset
    """
    try:
        ontology_asset_tag = SCHEMA_VERSION_TO_ONTOLOGY_ASSET_TAG[schema_version]
    except KeyError as e:
        raise ValueError(f"Schema version {schema_version} is not supported in this package version.") from e

    download_url = f"{ONTOLOGY_ASSET_RELEASE_URL}/{ontology_asset_tag}/{filename}"

    try:
        with urlopen(download_url) as response:
            if response.status == 200:
                content: bytes = response.read()
                return content
            else:
                raise ValueError(f"Server responded with status code: {response.status}")
    except HTTPError as e:
        raise ValueError(
            f"Could not get {filename} for schema version {schema_version} in GitHub Release Assets: {e}"
        ) from e
    except URLError as e:
        raise ValueError(f"URL error occurred: {e.reason}") from e
