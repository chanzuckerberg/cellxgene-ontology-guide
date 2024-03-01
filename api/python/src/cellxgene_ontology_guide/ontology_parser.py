import re
from typing import Any, Dict, List, Union

from artifact_download import load_artifact_by_schema
from constants import ALL_ONTOLOGY_FILENAME, ONTOLOGY_INFO_FILENAME
from entities import Ontology, OntologyFileType, OntologyVariant


class OntologyParser:
    """
    An object to parse ontology term metadata from ontologies corresponding to a given CellxGene Schema Version.
    """

    def __init__(self, schema_version: str):
        """
        Initialize an OntologyParser object with the ontology metadata corresponding to the given CellxGene schema
        version. If not cached, it will make a network call to GitHub Release Assets to load in memory and
        parse the corresponding ontology metadata.

        :param schema_version: str version of the schema to load ontology metadata for
        """
        self.ontology_dict = load_artifact_by_schema(schema_version, ALL_ONTOLOGY_FILENAME)
        self.supported_ontologies = load_artifact_by_schema(schema_version, ONTOLOGY_INFO_FILENAME)

    def _parse_ontology_name(self, term_id: str) -> str:
        """
        Parse the ontology name from a given term ID. If the term ID does not conform to the expected term format or is not
        from an ontology supported by cellxgene-ontology-guide, raise a ValueError.

        :param term_id: str ontology term to parse
        :return: str name of ontology that term belongs to
        """
        pattern = r"[A-Za-z]+:\d+"
        if not re.match(pattern, term_id):
            raise ValueError(f"{term_id} does not conform to expected regex pattern {pattern} and cannot be queried.")

        ontology_name = term_id.split(":")[0]
        if ontology_name not in self.supported_ontologies:
            raise ValueError(f"{term_id} is not part of a supported ontology, its metadata cannot be fetched.")

        return ontology_name

    def get_term_ancestors(self, term_id: str, include_self: bool = False) -> List[str]:
        """
        Get the ancestor ontology terms for a given term. If include_self is True, the term itself will be included as an
         ancestor.

         Example: get_term_ancestors("CL:0000005") -> ["CL:0000000", ...]

        :param term_id: str ontology term to find ancestors for
        :param include_self: boolean flag to include the term itself as an ancestor
        :return: flattened List[str] of ancestor terms
        """
        ontology_name = self._parse_ontology_name(term_id)
        ancestors: List[str] = self.ontology_dict[ontology_name][term_id]["ancestors"]
        return ancestors + [term_id] if include_self else ancestors

    def get_term_list_ancestors(self, term_ids: str, include_self: bool = False) -> Dict[str, List[str]]:
        """
        Get the ancestor ontology terms for each term in a list. If include_self is True, the term itself will be included
         as an ancestor.

         Example: get_term_list_ancestors(["CL:0000003", "CL:0000005"], include_self=True) -> {
            "CL:0000003": ["CL:0000003"],
            "CL:0000005": ["CL:0000005", "CL:0000000", ...]
        }

        :param term_ids: list of str ontology terms to find ancestors for
        :param include_self: boolean flag to include the term itself as an ancestor
        :return: Dictionary mapping str term IDs to their respective flattened List[str] of ancestor terms. Maps to empty
        list if there are no ancestors.
        """
        return {term_id: self.get_term_ancestors(term_id, include_self) for term_id in term_ids}

    def get_terms_descendants(self, term_ids: List[str], include_self: bool = False) -> Dict[str, List[str]]:
        """
        Get the descendant ontology terms for each term in a list. If include_self is True, the term itself will be included
         as a descendant.

        Example: get_terms_descendants(["CL:0000003", "CL:0000005"], include_self=True) -> {
            "CL:0000003": ["CL:0000003", "CL:0000004", ...],
            "CL:0000005": ["CL:0000005", "CL:0002363", ...]
        }

        :param term_ids: list of str ontology terms to find descendants for
        :param include_self: boolean flag to include the term itself as an descendant
        :return: Dictionary mapping str term IDs to their respective flattened List[str] of descendant terms. Maps to empty
        list if there are no descendants.
        """
        descendants_dict = dict()
        ontology_names = set()
        for term_id in term_ids:
            ontology_name = self._parse_ontology_name(term_id)
            descendants_dict[term_id] = [term_id] if include_self else []
            ontology_names.add(ontology_name)

        for ontology in ontology_names:
            for candidate_descendant, candidate_metadata in self.ontology_dict[ontology].items():
                for ancestor_id in descendants_dict:
                    if ancestor_id in candidate_metadata["ancestors"]:
                        descendants_dict[ancestor_id].append(candidate_descendant)

        return descendants_dict

    def is_term_deprecated(self, term_id: str) -> bool:
        """
        Check if an ontology term is deprecated.

        Example: is_term_deprecated("CL:0000003") -> True

        :param term_id: str ontology term to check for deprecation
        :return: boolean flag indicating whether the term is deprecated
        """
        ontology_name = self._parse_ontology_name(term_id)
        is_deprecated: bool = self.ontology_dict[ontology_name][term_id].get("deprecated")
        return is_deprecated

    def get_term_replacement(self, term_id: str) -> Union[str, None]:
        """
        Fetch the replacement term for a deprecated ontology term, if a replacement exists. Return None otherwise.

        Example: get_term_replacement("CL:0000003") -> "CL:0000000"

        :param term_id: str ontology term to check a replacement term for
        :return: replacement str term ID if it exists, None otherwise
        """
        ontology_name = self._parse_ontology_name(term_id)
        replaced_by: str = self.ontology_dict[ontology_name][term_id].get("replaced_by")
        return replaced_by if replaced_by else None

    def get_term_metadata(self, term_id: str) -> Dict[str, Any]:
        """
        Fetch metadata for a given ontology term. Returns a dict with format

        {"comments": ["...", ...], "term_tracker": "...", "consider": ["...", ...]}

        Comments maps to List[str] of ontology curator comments
        Term Tracker maps to a str url where there is discussion around this term's curation (or deprecation).
        Consider maps to List[str] of alternate ontology terms to consider using instead of this term

        All keys map to None if no metadata of that type is present.

        :param term_id: str ontology term to fetch metadata for
        :return: Dict with keys 'Comments', 'Term Tracker', and 'Consider' containing associated metadata.
        """
        ontology_name = self._parse_ontology_name(term_id)
        return {
            key: self.ontology_dict[ontology_name][term_id].get(key, None)
            for key in {"comments", "term_tracker", "consider"}
        }

    def get_term_label(self, term_id: str) -> str:
        """
        Fetch the human-readable label for a given ontology term.

        Example: get_term_label("CL:0000005") -> "fibroblast neural crest derived"

        :param term_id: str ontology term to fetch label for
        :return: str human-readable label for the term
        """
        ontology_name = self._parse_ontology_name(term_id)
        label: str = self.ontology_dict[ontology_name][term_id]["label"]
        return label

    def get_ontology_download_url(
        self, ontology_name: Ontology, ontology_filetype: OntologyFileType, ontology_variant: OntologyVariant = None
    ) -> str:
        """
        Get the download URL for a given ontology file. If the ontology_variant is not provided, the default ontology
        file will be returned.

        Examples:
        get_ontology_download_url("CL", "owl") -> "http://example.com/2024-01-01/cl.owl"
        get_ontology_download_url("CL", "obo", "base") -> "http://example.com/2024-01-01/cl-base.obo"

        :param ontology_name: str name of the ontology to fetch
        :param ontology_filetype: OntologyFileType enum of the ontology file type to fetch
        :param ontology_variant: OntologyVariant enum of the ontology variant to fetch
        :return: str download URL for the requested ontology file
        """
        if not Ontology.has_value(ontology_name):
            raise ValueError(f"Ontology {ontology_name} is not supported by cellxgene-ontology-guide.")
        if not OntologyFileType.has_value(ontology_filetype):
            raise ValueError(f"Ontology filetype {ontology_filetype} is not supported by cellxgene-ontology-guide.")
        if ontology_variant is not None and not OntologyVariant.has_value(ontology_variant):
            raise ValueError(f"Ontology variant {ontology_variant} is not supported by cellxgene-ontology-guide.")

        source_url = self.supported_ontologies[ontology_name]["source"]
        version = self.supported_ontologies[ontology_name]["version"]
        return (
            f"{source_url}/{version}/{ontology_name}-{ontology_variant}.{ontology_filetype}"
            if ontology_variant
            else f"{source_url}/{version}/{ontology_name}.{ontology_filetype}"
        )
