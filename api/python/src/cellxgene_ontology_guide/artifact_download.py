import requests

from constants import ONTOLOGY_ASSET_RELEASE_URL, SCHEMA_VERSION_TO_ONTOLOGY_ASSET_TAG


# TODO: add caching?
def load_artifact_by_schema(schema_version: str, filename: str) -> bytes:
    """
    Load ontology files from GitHub Release Assets, based on the provided schema version.
    Returns ValueError if the schema version is not supported in this package version.

    :param schema_version: str version of the schema to load ontology files for
    :param filename: str name of the file to load
    :return: str path to the ontology file
    """
    try:
        ontology_asset_tag = SCHEMA_VERSION_TO_ONTOLOGY_ASSET_TAG[schema_version]
    except KeyError:
        raise ValueError(f"Schema version {schema_version} is not supported in this package version.")

    response = requests.get(ONTOLOGY_ASSET_RELEASE_URL)
    download_url = None
    for release in response.json():  # TODO: account for pagination
        if release["tag_name"] == ontology_asset_tag:
            for asset in release["assets"]:
                if asset["name"] == filename:
                    download_url = asset["browser_download_url"]
    if not download_url:
        raise ValueError(f"Could not find {filename} for schema version {schema_version} in GitHub Release Assets.")

    return requests.get(download_url).content
