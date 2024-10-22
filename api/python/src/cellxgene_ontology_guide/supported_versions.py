import functools
import gzip
import json
import os
import warnings
from datetime import datetime
from typing import Any, Dict, List, Optional

from semantic_version import Version

from cellxgene_ontology_guide._constants import DATA_ROOT, ONTOLOGY_FILENAME_SUFFIX, ONTOLOGY_INFO_FILENAME
from cellxgene_ontology_guide.entities import Ontology


@functools.cache
def load_ontology_file(file_name: str) -> Any:
    """Load the ontology file from the data directory and return it as a dict."""
    with gzip.open(os.path.join(DATA_ROOT, file_name), "rt") as f:
        return json.load(f)


def clear_ontology_file_cache() -> None:
    """Clear the cache for the load_ontology_file function."""
    load_ontology_file.cache_clear()


def get_latest_schema_version(versions: List[str]) -> str:
    """Given a list of schema versions, return the latest version.

    :param versions: List[str] list of schema versions. Versions can be in the format "v5.0.0" or "5.0.0"
    :return: str latest version without the leading "v"
    """

    return str(sorted([coerce_version(version) for version in versions])[-1])


def coerce_version(version: str) -> Version:
    """Coerce a version string into a semantic_version.Version object.

    :param version: str version string to coerce
    :return: Version coerced version object
    """
    v = version[1:] if version[0] == "v" else version
    return Version.coerce(v)


def load_supported_versions() -> Any:
    """Load the ontology_info.json file and return it as a dict."""
    with open(os.path.join(DATA_ROOT, ONTOLOGY_INFO_FILENAME)) as f:
        return json.load(f)


class CXGSchema:
    """A class to represent the ontology information used by a cellxgene schema version."""

    version: str
    """The schema version used by the class instance."""
    supported_ontologies: Dict[str, Any]
    """A dictionary of supported ontologies for the schema version."""
    ontology_file_names: Dict[str, str]
    """A dictionary of ontology names and their corresponding file names."""

    def __init__(self, version: Optional[str] = None):
        """

        :param version: The schema version to use. If not provided, the latest schema version will be used.
        """
        ontology_info = load_supported_versions()
        if version is None:
            _version = get_latest_schema_version(ontology_info.keys())
        else:
            _version = str(coerce_version(version))
            if str(_version) not in ontology_info:
                raise ValueError(f"Schema version {_version} is not supported in this package version.")

        self.version = _version
        self.supported_ontologies = ontology_info[_version]["ontologies"]
        self.ontology_file_names: Dict[str, str] = {}
        self.deprecated_on = ontology_info[_version].get("deprecated_on")
        if self.deprecated_on:
            parsed_date = datetime.strptime(self.deprecated_on, "%Y-%m-%d")
            warnings.warn(
                f"Schema version {_version} is deprecated as of {parsed_date}. It will be removed in a future version.",
                DeprecationWarning,
                stacklevel=1,
            )

    def ontology(self, name: str) -> Any:
        """Return the ontology terms for the given ontology name. Load from the file cache if available.
        :param name: str name of the ontology to get the terms for
        :return: dict representation of the ontology terms
        """
        if name not in self.ontology_file_names:
            if getattr(Ontology, name, None) is None:
                raise ValueError(f"Ontology {name} is not supported in this package version.")

            try:
                onto_version = self.supported_ontologies[name]["version"]
            except KeyError as e:
                raise ValueError(f"Ontology {name} is not supported for schema version {self.version}") from e
            file_name = f"{name}-ontology-{onto_version}{ONTOLOGY_FILENAME_SUFFIX}"
            self.ontology_file_names[name] = file_name  # save to file name to access from cache
        return load_ontology_file(self.ontology_file_names[name])

    def get_ontology_download_url(self, ontology: Ontology) -> str:
        """
        Get the download URL for a given ontology file.

        Examples:
        get_ontology_download_url("CL") -> "http://example.com/2024-01-01/cl.owl"

        :param ontology: Ontology enum of the ontology to fetch
        :return: str download URL for the requested ontology file
        """
        source_url = self.supported_ontologies[ontology.name]["source"]
        version = self.supported_ontologies[ontology.name]["version"]
        filename = self.supported_ontologies[ontology.name]["filename"]
        return f"{source_url}/{version}/{filename}"
