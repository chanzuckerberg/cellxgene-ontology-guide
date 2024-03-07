import re
from typing import Any, Dict, List, Union

from entities import Ontology, OntologyFileType, OntologyVariant

from cellxgene_ontology_guide.supported_versions import CXGSchema


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
        self.cxg_schema = CXGSchema(version=schema_version)

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
        if ontology_name not in self.cxg_schema.supported_ontologies:
            raise ValueError(f"{term_id} is not part of a supported ontology, its metadata cannot be fetched.")

        return ontology_name

    def get_term_ancestors(self, term_id: str, include_self: bool = False) -> List[str]:
        """
        Get the ancestor ontology terms for a given term. If include_self is True, the term itself will be included as
        an ancestor.

         Example: get_term_ancestors("CL:0000005") -> ["CL:0000000", ...]

        :param term_id: str ontology term to find ancestors for
        :param include_self: boolean flag to include the term itself as an ancestor
        :return: flattened List[str] of ancestor terms
        """
        ontology_name = self._parse_ontology_name(term_id)
        ancestors = list(self.cxg_schema.ontology(ontology_name)[term_id]["ancestors"].keys())
        return ancestors + [term_id] if include_self else ancestors

    def get_term_list_ancestors(self, term_ids: List[str], include_self: bool = False) -> Dict[str, List[str]]:
        """
        Get the ancestor ontology terms for each term in a list. If include_self is True, the term itself will be
        included as an ancestor.

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

    def map_high_level_terms(
        self, term_ids: List[str], high_level_terms: List[str], include_self: bool = True
    ) -> Dict[str, List[str]]:
        """
        Given a list of ontology term IDs and a list of high_level_terms to map them to, returns a dictionary with
        format

        {"CL:0000003": ["CL:0000000", ...], "CL:0000005": ["CL:0000000", ...]}

        Where each term_id is mapped to a List[str] of high-level terms that it is a descendant of

        :param term_ids: list of str ontology terms to map high level terms for
        :param high_level_terms: list of str ontology terms that can be mapped to descendant term_ids
        :param include_self: bool to map a term_id to itself if it is in high_level_terms
        :return: Dictionary mapping str term IDs to their respective List[str] of ancestor terms from the input list.
        Each key maps to empty list if there are no ancestors among the provided input.
        """
        ancestors = self.get_term_list_ancestors(term_ids, include_self)
        for term_id in term_ids:
            ancestors[term_id] = [
                high_level_term for high_level_term in ancestors[term_id] if high_level_term in high_level_terms
            ]
        return ancestors

    def get_distance_between_terms(self, ontology: Ontology, term_id_1: str, term_id_2: str) -> int:
        """
        Get the distance between two ontology terms. The distance is defined as the number of edges between the
        two terms. Terms must be from the same ontology.

        :param ontology: Ontology enum of the ontology to find distance for
        :param term_id_1: str ontology term to find distance for
        :param term_id_2: str ontology term to find distance for
        :return: int distance between the two terms, measured in number of edges between their shortest path.
        """
        lca = self.get_lowest_common_ancestor(ontology, term_id_1, term_id_2)
        return int(
            self.cxg_schema.ontology(ontology.name)[term_id_1]["ancestors"][lca]
            + self.cxg_schema.ontology(ontology.name)[term_id_2]["ancestors"][lca]
        )

    def get_lowest_common_ancestor(self, ontology: Ontology, term_id_1: str, term_id_2: str) -> str:
        """
        Get the lowest common ancestor between two ontology terms that is from the given ontology.
        Terms must be from the same ontology.

        :param ontology: Ontology enum of the ontology to find distance for
        :param term_id_1: str ontology term to find LCA for
        :param term_id_2: str ontology term to find LCA for
        :return: str term ID of the lowest common ancestor term
        """
        # include path to term itself
        ancestors_1 = self.cxg_schema.ontology(ontology.name)[term_id_1]["ancestors"] + {term_id_1: 0}
        ancestors_2 = self.cxg_schema.ontology(ontology.name)[term_id_2]["ancestors"] + {term_id_2: 0}
        common_ancestors = set(ancestors_1.keys()) & set(ancestors_2.keys())
        return str(min(common_ancestors, key=lambda x: ancestors_1[x] + ancestors_2[x]))

    def map_highest_level_term(
        self, term_ids: List[str], high_level_terms: List[str], include_self: bool = True
    ) -> Dict[str, Union[str, None]]:
        """
        Given a list of ontology term IDs and a list of high_level_terms to map them to, returns a dictionary with
        format

        {"CL:0000003": "CL:0000000", "CL:0000005": "CL:0000000"}

        Where each term_id is mapped to the highest level term that it is a descendant of, from the list provided. Maps
        to None if term_id does not map to any high level terms among the provided input.

        :param term_ids: list of str ontology terms to map high level terms for
        :param high_level_terms: list of str ontology terms that can be mapped to descendant term_ids
        :param include_self: bool to map a term_id to itself if it is in high_level_terms
        :return: Dictionary mapping str term IDs to their respective List[str] of ancestor terms from the input list.
        Each key maps to empty list if there are no ancestors among the provided input.
        """
        high_level_term_map = self.map_high_level_terms(term_ids, high_level_terms, include_self)
        highest_level_term_map = dict()
        for term_id in term_ids:
            ontology = self._parse_ontology_name(term_id)
            # map term_id to the high_level_term with the longest distance from term_id
            highest_level_term_map[term_id] = (
                max(
                    high_level_term_map[term_id],
                    key=lambda x: self.cxg_schema.ontology(ontology)[term_id]["ancestors"][x],
                )
                if high_level_term_map[term_id]
                else None
            )
        return highest_level_term_map

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
            for candidate_descendant, candidate_metadata in self.cxg_schema.ontology(ontology).items():
                for ancestor_id in descendants_dict:
                    ancestors = candidate_metadata["ancestors"].keys()
                    if ancestor_id in ancestors:
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
        is_deprecated: bool = self.cxg_schema.ontology(ontology_name)[term_id].get("deprecated")
        return is_deprecated

    def get_term_replacement(self, term_id: str) -> Union[str, None]:
        """
        Fetch the replacement term for a deprecated ontology term, if a replacement exists. Return None otherwise.

        Example: get_term_replacement("CL:0000003") -> "CL:0000000"

        :param term_id: str ontology term to check a replacement term for
        :return: replacement str term ID if it exists, None otherwise
        """
        ontology_name = self._parse_ontology_name(term_id)
        replaced_by: str = self.cxg_schema.ontology(ontology_name)[term_id].get("replaced_by")
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
            key: self.cxg_schema.ontology(ontology_name)[term_id].get(key, None)
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
        label: str = self.cxg_schema.ontology(ontology_name)[term_id]["label"]
        return label

    def get_ontology_download_url(
        self, ontology: Ontology, ontology_filetype: OntologyFileType, ontology_variant: OntologyVariant = None
    ) -> str:
        """
        Get the download URL for a given ontology file. If the ontology_variant is not provided, the default ontology
        file will be returned.

        Examples:
        get_ontology_download_url("CL", "owl") -> "http://example.com/2024-01-01/cl.owl"
        get_ontology_download_url("CL", "obo", "base") -> "http://example.com/2024-01-01/cl-base.obo"

        :param ontology: Ontology enum of the ontology to fetch
        :param ontology_filetype: OntologyFileType enum of the ontology file type to fetch
        :param ontology_variant: OntologyVariant enum of the ontology variant to fetch
        :return: str download URL for the requested ontology file
        """
        source_url = self.cxg_schema.supported_ontologies[ontology.name]["source"]
        version = self.cxg_schema.supported_ontologies[ontology.name]["version"]
        return (
            f"{source_url}/{version}/{ontology.value}-{ontology_variant.value}.{ontology_filetype.value}"
            if ontology_variant
            else f"{source_url}/{version}/{ontology.value}.{ontology_filetype.value}"
        )
