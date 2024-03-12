import functools
import gzip
import json
import os
from typing import Any, Dict, List, Optional

from semantic_version import Version

from cellxgene_ontology_guide.constants import DATA_ROOT, ONTOLOGY_FILENAME_SUFFIX, ONTOLOGY_INFO_FILENAME
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
    :return: str latest version with a "v" prefix
    """

    def _coerce(v: str) -> Version:
        return Version.coerce(v[1:]) if v[0] == "v" else Version.coerce(v)

    return "v" + str(sorted([_coerce(version) for version in versions])[-1])


def load_supported_versions() -> Any:
    """Load the ontology_info.json file and return it as a dict."""
    with open(os.path.join(DATA_ROOT, ONTOLOGY_INFO_FILENAME)) as f:
        return json.load(f)


class CXGSchema:
    """A class to represent the ontology information used by a cellxgene schema version."""

    def __init__(self, version: Optional[str] = None):
        """

        :param version: The schema version to use. If not provided, the latest schema version will be used.
        """
        ontology_info = load_supported_versions()
        if version is None:
            version = get_latest_schema_version(ontology_info.keys())
        elif version not in ontology_info:
            raise ValueError(f"Schema version {version} is not supported in this package version.")

        self.version = version
        self.supported_ontologies = ontology_info[version]
        self.ontology_file_names: Dict[str, str] = {}

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
