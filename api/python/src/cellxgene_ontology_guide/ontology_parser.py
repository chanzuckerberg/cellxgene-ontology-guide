import re
from typing import Any, Dict, Iterable, List, Optional, Union

from cellxgene_ontology_guide._constants import VALID_NON_ONTOLOGY_TERMS
from cellxgene_ontology_guide.entities import OntologyNode
from cellxgene_ontology_guide.supported_versions import CXGSchema


class OntologyParser:
    """
    An object to parse ontology term metadata from ontologies corresponding to a given CellxGene Schema Version.
    """

    cxg_schema: CXGSchema
    """ CXGSchema object to fetch ontology metadata from """

    def __init__(self, schema_version: Optional[str] = None):
        """
        Initialize an OntologyParser object with the ontology metadata corresponding to the given CellxGene schema
        version. If not cached, it will make a network call to GitHub Release Assets to load in memory and
        parse the corresponding ontology metadata.

        :param schema_version: str version of the schema to load ontology metadata for. If not provided, the latest
        is loaded.
        """
        self.cxg_schema = CXGSchema(version=schema_version) if schema_version else CXGSchema()
        self.term_label_to_id_map: Dict[str, Dict[str, str]] = {
            ontology_name: dict() for ontology_name in self.cxg_schema.supported_ontologies
        }

    def get_term_label_to_id_map(self, ontology_name: str) -> Dict[str, str]:
        """
        Fetch the mapping of term labels to term IDs for a given ontology. Caches generated maps by ontology_name.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_label_to_id_map("CL") # doctest: +SKIP
        {'Label A': 'CL:0000000', ... }

        :param ontology_name: str name of ontology to get map of term labels to term IDs
        """
        if ontology_name not in self.cxg_schema.supported_ontologies:
            raise ValueError(f"{ontology_name} is not a supported ontology, its metadata cannot be fetched.")

        if self.term_label_to_id_map[ontology_name]:
            return self.term_label_to_id_map[ontology_name]

        for term_id, term_metadata in self.cxg_schema.ontology(ontology_name).items():
            self.term_label_to_id_map[ontology_name][term_metadata["label"]] = term_id

        return self.term_label_to_id_map[ontology_name]

    def _parse_ontology_name(self, term_id: str) -> str:
        """
        Parse the ontology name from a given term ID. If the term ID does not conform to the expected term format or
        is not from an ontology supported by cellxgene-ontology-guide, raise a ValueError.

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

    def is_valid_term_id(self, term_id: str, ontology: Optional[str] = None) -> bool:
        """
        Check if an ontology term ID is valid and defined in a supported ontology. If deprecated but defined
        in the ontology, it is considered valid. Optionally, specify an ontology to check against, and determine
        if the term is defined in that particular ontology. Otherwise, checks if term is valid in any supported ontology

        :param term_id: str ontology term to check
        :param ontology: str name of ontology to check against
        :return: boolean flag indicating whether the term is supported
        """
        try:
            ontology_name = self._parse_ontology_name(term_id)
            if ontology and ontology_name != ontology:
                return False
            if term_id in self.cxg_schema.ontology(ontology_name):
                return True
        except ValueError:
            return False
        return False

    def get_term_ancestors(self, term_id: str, include_self: bool = False) -> List[str]:
        """
        Get the ancestor ontology terms for a given term. If include_self is True, the term itself will be included as
        an ancestor. Raises ValueError if the term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_ancestors("CL:0000005") # doctest: +SKIP
        ['CL:0000000', 'CL:0000057', ...

        :param term_id: str ontology term to find ancestors for
        :param include_self: boolean flag to include the term itself as an ancestor
        :return: flattened List[str] of ancestor terms
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return []
        ontology_name = self._parse_ontology_name(term_id)
        ancestors = list(self.cxg_schema.ontology(ontology_name)[term_id]["ancestors"].keys())
        return ancestors + [term_id] if include_self else ancestors

    def map_term_ancestors(self, term_ids: Iterable[str], include_self: bool = False) -> Dict[str, List[str]]:
        """
        Get the ancestor ontology terms for each term in a list. If include_self is True, the term itself will be
        included as an ancestor. Raises ValueError if the term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.map_term_ancestors(["CL:0000003", "CL:0000005"], include_self=True) # doctest: +SKIP
        {
            'CL:0000003': ['CL:0000003'],
            'CL:0000005': ['CL:0000005', 'CL:0000000', ...]
        }

        :param term_ids: list of str ontology terms to find ancestors for
        :param include_self: boolean flag to include the term itself as an ancestor
        :return: Dictionary mapping str term IDs to their respective flattened List[str] of ancestor terms. Maps to
        empty
        list if there are no ancestors.
        """
        return {term_id: self.get_term_ancestors(term_id, include_self) for term_id in term_ids}

    def get_term_ancestors_with_distances(self, term_id: str, include_self: bool = False) -> Dict[str, int]:
        """
        Get the ancestor ontology terms for a given term, and their distance from the term_id. If include_self is True,
        the term itself will be included as an ancestor. Raises ValueError if the term ID is not valid member of a
        supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_ancestors_with_distances("CL:0000005") # doctest: +SKIP
        {'CL:0000057': 1, 'CL:0002320': 2, 'CL:0000000': 3}

        :param term_id: str ontology term to find ancestors for
        :param include_self: boolean flag to include the term itself as an ancestor
        :return: Dict[str, int] map of ancestor terms and their respective distances from the term_id
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return {}
        ontology_name = self._parse_ontology_name(term_id)
        ancestors: Dict[str, int] = self.cxg_schema.ontology(ontology_name)[term_id]["ancestors"]
        if include_self:
            ancestors[term_id] = 0
        return ancestors

    def map_term_ancestors_with_distances(
        self, term_ids: Iterable[str], include_self: bool = False
    ) -> Dict[str, Dict[str, int]]:
        """
        Get the ancestor ontology terms for each term in a list, and their distance from the term_id. If include_self is
        True, the term itself will be included as an ancestor. Raises ValueError if the term ID is not valid member of a
        supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.map_term_ancestors_with_distances(["CL:0000003", "CL:0000005"], include_self=True)
        {'CL:0000003': {'CL:0000003': 0}, 'CL:0000005': {'CL:0000057': 1, 'CL:0002320': 2, 'CL:0000000': 3,
        'CL:0000005': 0}}

        :param term_ids: list of str ontology terms to find ancestors for
        :param include_self: boolean flag to include the term itself as an ancestor
        :return: Dictionary mapping str term IDs to their respective Dict[str, int] map of ancestor terms and their
        respective distances from the term_id
        """
        return {term_id: self.get_term_ancestors_with_distances(term_id, include_self) for term_id in term_ids}

    def get_term_parents(self, term_id: str) -> List[str]:
        """
        Get the direct parent ontology terms for a given term. Raises ValueError if the term ID is not valid member of
        a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_parents("CL:0000101")
        ['CL:0000526']

        :param term_id: str ontology term to find parents for
        :return: List[str] of parent terms
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return []
        ontology_name = self._parse_ontology_name(term_id)
        ancestors: Dict[str, int] = self.cxg_schema.ontology(ontology_name)[term_id]["ancestors"]
        parents: List[str] = [ancestor for ancestor, distance in ancestors.items() if distance == 1]
        return parents

    def get_distance_between_terms(self, term_id_1: str, term_id_2: str) -> int:
        """
        Get the distance between two ontology terms. The distance is defined as the number of edges between the
        two terms. Terms must be from the same ontology. Returns -1 if terms are disjoint.
        Raises ValueError if term IDs are not valid members of a supported ontology.

        :param term_id_1: str ontology term to find distance for
        :param term_id_2: str ontology term to find distance for
        :return: int distance between the two terms, measured in number of edges between their shortest path.
        """
        lcas = self.get_lowest_common_ancestors(term_id_1, term_id_2)
        if not lcas:
            return -1
        return int(
            self.get_term_ancestors_with_distances(term_id_1, include_self=True)[lcas[0]]
            + self.get_term_ancestors_with_distances(term_id_2, include_self=True)[lcas[0]]
        )

    def get_lowest_common_ancestors(self, term_id_1: str, term_id_2: str) -> List[str]:
        """
        Get the lowest common ancestors between two ontology terms that is from the given ontology.
        Terms must be from the same ontology. Ontologies are DAGs, so there may be multiple lowest common ancestors.
        Raises ValueError if term IDs are not valid members of a supported ontology.

        :param term_id_1: str ontology term to find LCA for
        :param term_id_2: str ontology term to find LCA for
        :return: str term ID of the lowest common ancestor term
        """
        # include path to term itself
        ontology = self._parse_ontology_name(term_id_1)
        if ontology != self._parse_ontology_name(term_id_2):
            return []
        ancestors_1 = self.get_term_ancestors_with_distances(term_id_1, include_self=True)
        ancestors_2 = self.get_term_ancestors_with_distances(term_id_2, include_self=True)
        common_ancestors = set(ancestors_1.keys()) & set(ancestors_2.keys())
        min_sum_distances = float("inf")
        for ancestors in common_ancestors:
            sum_distances = ancestors_1[ancestors] + ancestors_2[ancestors]
            if sum_distances < min_sum_distances:
                min_sum_distances = sum_distances
        return [
            ancestor
            for ancestor in common_ancestors
            if ancestors_1[ancestor] + ancestors_2[ancestor] == min_sum_distances
        ]

    def get_high_level_terms(self, term_id: str, high_level_terms: List[str]) -> List[str]:
        """
        Get the high-level ontology terms for a given term. High-level terms are defined as the ancestors of the term
        that are part of the high-level ontology terms supported by cellxgene-ontology-guide. If more than 1
        high_level_term is matched, the returned list of matches preserves the order of the input high_level_terms list.
        Raises ValueError if term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_high_level_terms("CL:0000005", ["CL:0000000", "CL:0000001"])
        ['CL:0000000']

        :param term_id: str ontology term to find high-level terms for
        :param high_level_terms: list of str ontology terms to check for ancestry to term_id
        :return: List[str] of high-level terms that the term is a descendant of
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return []
        ancestors = self.get_term_ancestors(term_id, include_self=True)
        return [high_level_term for high_level_term in high_level_terms if high_level_term in ancestors]

    def map_high_level_terms(self, term_ids: List[str], high_level_terms: List[str]) -> Dict[str, List[str]]:
        """
        Given a list of ontology term IDs and a list of high_level_terms to map them to, returns a dictionary with
        format

        {"CL:0000003": ["CL:0000000", ...], "CL:0000005": ["CL:0000000", ...]}

        Where each term_id is mapped to a List[str] of high-level terms that it is a descendant of. Includes self
        as a descendant. Raises ValueError if term ID is not valid member of a supported ontology.

        :param term_ids: list of str ontology terms to map high level terms for
        :param high_level_terms: list of str ontology terms to be mapped to descendant term_ids
        :return: Dictionary mapping str term IDs to their respective List[str] of ancestor terms from the input list.
        Each key maps to empty list if there are no ancestors among the provided input.
        """
        return {term_id: self.get_high_level_terms(term_id, high_level_terms) for term_id in term_ids}

    def get_highest_level_term(self, term_id: str, high_level_terms: List[str]) -> Union[str, None]:
        """
        Get the highest level ontology term for a given term. The highest level term is defined as the ancestor of the
        term that is part of the high-level ontology terms supported by cellxgene-ontology-guide. Raises ValueError
        if term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_highest_level_term("CL:0000005", ["CL:0000000", "CL:0000001"])
        'CL:0000000'

        :param term_id: str ontology term to find highest level term for
        :param high_level_terms: list of str ontology terms to check for ancestry to term_id
        :return: str highest level term that the term is a descendant of, or None if it is not a descendant of any
        high-level terms
        """
        high_level_terms = self.get_high_level_terms(term_id, high_level_terms)
        term_ancestors_and_distances = self.get_term_ancestors_with_distances(term_id, include_self=True)
        if not high_level_terms:
            return None
        return max(high_level_terms, key=lambda high_level_term: term_ancestors_and_distances[high_level_term])

    def map_highest_level_term(self, term_ids: List[str], high_level_terms: List[str]) -> Dict[str, Union[str, None]]:
        """
        Given a list of ontology term IDs and a list of high_level_terms to map them to, returns a dictionary with
        format

        {"CL:0000003": "CL:0000000", "CL:0000005": "CL:0000000"}

        Where each term_id is mapped to the highest level term that it is a descendant of, from the list provided.
        Includes term itself as a descendant. Maps to None if term_id does not map to any high level terms among the
        provided input. Raises ValueError if term ID is not valid member of a supported ontology.

        :param term_ids: list of str ontology terms to map high level terms for
        :param high_level_terms: list of str ontology terms that can be mapped to descendant term_ids
        :return: Dictionary mapping str term IDs to their respective List[str] of ancestor terms from the input list.
        Each key maps to empty list if there are no ancestors among the provided input.
        """
        return {term_id: self.get_highest_level_term(term_id, high_level_terms) for term_id in term_ids}

    def get_term_descendants(self, term_id: str, include_self: bool = False) -> List[str]:
        """
        Get the descendant ontology terms for a given term. If include_self is True, the term itself will be included as
        a descendant. Raises ValueError if term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_descendants("CL:0000005") # doctest: +SKIP
        ['CL:0002363']

        :param term_id: str ontology term to find descendants for
        :param include_self: boolean flag to include the term itself as a descendant
        :return: List[str] of descendant terms
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return []
        ontology_name = self._parse_ontology_name(term_id)
        descendants = [term_id] if include_self else []
        for candidate_descendant, candidate_metadata in self.cxg_schema.ontology(ontology_name).items():
            ancestors = candidate_metadata["ancestors"].keys()
            if term_id in ancestors:
                descendants.append(candidate_descendant)
        return descendants

    def map_term_descendants(self, term_ids: Iterable[str], include_self: bool = False) -> Dict[str, List[str]]:
        """
        Get the descendant ontology terms for each term in a list. If include_self is True, the term itself will be
         included as a descendant. Raises ValueError if term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.map_term_descendants(["CL:0000003", "CL:0000005"], include_self=True) # doctest: +SKIP
        {
            'CL:0000003': ['CL:0000003', ...],
            'CL:0000005': ['CL:0000005', 'CL:0002363', ...]
        }

        :param term_ids: list of str ontology terms to find descendants for
        :param include_self: boolean flag to include the term itself as an descendant
        :return: Dictionary mapping str term IDs to their respective flattened List[str] of descendant terms. Maps to
        empty list if there are no descendants.
        """
        descendants_dict: Dict[str, List[str]] = dict()
        ontology_names = set()
        for term_id in term_ids:
            if term_id in VALID_NON_ONTOLOGY_TERMS:
                descendants_dict[term_id] = []
                continue
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

    def get_term_children(self, term_id: str) -> List[str]:
        """
        Get the direct children ontology terms for a given term. Raises ValueError if term ID is not valid member of a
        supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_children("CL:0000526")
        ['CL:0000101']

        :param term_id: str ontology term to find children for
        :return: List[str] of children terms
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return []
        ontology_name = self._parse_ontology_name(term_id)
        children = []
        for candidate_child, candidate_metadata in self.cxg_schema.ontology(ontology_name).items():
            for ancestor, distance in candidate_metadata["ancestors"].items():
                if ancestor == term_id and distance == 1:
                    children.append(candidate_child)
        return children

    def get_term_graph(self, term_id: str) -> OntologyNode:
        """
        Get the DAG of OntologyNode relationships, with the input term as the root node. Only includes terms from the
        same ontology as the root term ID. Raises ValueError if term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> root_node = ontology_parser.get_term_graph("CL:0000000")
        >>> root_node.term_id
        'CL:0000000'
        >>> root_node.to_dict() # doctest: +SKIP
        {
            "term_id": "CL:0000000",
            "name": "cell A",
            "children": [
                {
                    "term_id": "CL:0000001",
                    "name": "cell B",
                    "children": [...],
                },
                {
                    "term_id": "CL:0000002",
                    "name": "cell C",
                    "children": [...],
                },
                ...
            ]
        }
        >>> root_node.term_counter # doctest: +SKIP
        Counter({'CL:0002058': 48, 'CL:0002471': 48, ...

        :param term_id: str ontology term to build subtree for
        :return: OntologyNode representation of graph with term_id as root.
        """
        term_label = self.get_term_label(term_id)
        root = OntologyNode(term_id, term_label)
        for child_term_id in self.get_term_children(term_id):
            root.add_child(self.get_term_graph(child_term_id))
        return root

    def is_term_deprecated(self, term_id: str) -> bool:
        """
        Check if an ontology term is deprecated. Raises ValueError if term ID is not valid member of a supported
        ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.is_term_deprecated("CL:0000003")
        True

        :param term_id: str ontology term to check for deprecation
        :return: boolean flag indicating whether the term is deprecated
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return False
        ontology_name = self._parse_ontology_name(term_id)
        is_deprecated: bool = self.cxg_schema.ontology(ontology_name)[term_id].get("deprecated")
        return is_deprecated

    def get_term_replacement(self, term_id: str) -> Union[str, None]:
        """
        Fetch the replacement term for a deprecated ontology term, if a replacement exists. Return None otherwise.
        Raises ValueError if term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_replacement("CL:0000003")
        'CL:0000000'

        :param term_id: str ontology term to check a replacement term for
        :return: replacement str term ID if it exists, None otherwise
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return None
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

        All keys map to None if no metadata of that type is present. Raises ValueError if term ID is not valid member
        of a supported ontology.

        :param term_id: str ontology term to fetch metadata for
        :return: Dict with keys 'Comments', 'Term Tracker', and 'Consider' containing associated metadata.
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return {"comments": None, "term_tracker": None, "consider": None}
        ontology_name = self._parse_ontology_name(term_id)
        return {
            key: self.cxg_schema.ontology(ontology_name)[term_id].get(key, None)
            for key in {"comments", "term_tracker", "consider"}
        }

    def get_term_label(self, term_id: str) -> str:
        """
        Fetch the human-readable label for a given ontology term. Raises ValueError if term ID is not valid member of a
        supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_label("CL:0000005")
        'neural crest derived fibroblast'

        :param term_id: str ontology term to fetch label for
        :return: str human-readable label for the term
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return term_id
        ontology_name = self._parse_ontology_name(term_id)
        label: str = self.cxg_schema.ontology(ontology_name)[term_id]["label"]
        return label

    def map_term_labels(self, term_ids: Iterable[str]) -> Dict[str, str]:
        """
        Fetch the human-readable label for a given list of ontology terms. Raises ValueError if term ID is not valid
        member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.map_term_labels(["CL:0000005", "CL:0000003"])
        {'CL:0000005': 'neural crest derived fibroblast', 'CL:0000003': 'obsolete native cell'}

        :param term_ids: list of str ontology terms to fetch label for
        :return: Dict[str, str] mapping term IDs to their respective human-readable labels
        """
        return {term_id: self.get_term_label(term_id) for term_id in term_ids}

    def get_term_description(self, term_id: str) -> Optional[str]:
        """
        Fetch the description for a given ontology term. Raises ValueError if term ID is not valid member of a
        supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_description("CL:0000005")
        'Any fibroblast that is derived from the neural crest.'

        :param term_id: str ontology term to fetch description for
        :return: str description for the term
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return term_id
        ontology_name = self._parse_ontology_name(term_id)
        description: Optional[str] = self.cxg_schema.ontology(ontology_name)[term_id].get("description", None)
        return description

    def map_term_descriptions(self, term_ids: List[str]) -> Dict[str, Optional[str]]:
        """
        Fetch the descriptions for a given list of ontology terms. Raises ValueError if term ID is not valid member of
        a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.map_term_descriptions(["CL:0000005", "CL:0000146"])
        {'CL:0000005': 'Any fibroblast that is derived from the neural crest.', 'CL:0000146': None}

        :param term_ids: list of str ontology terms to fetch descriptions for
        :return: Dict[str, str] mapping term IDs to their respective descriptions
        """
        return {term_id: self.get_term_description(term_id) for term_id in term_ids}

    def get_term_synonyms(self, term_id: str) -> List[str]:
        """
        Fetch a list of synonym labels for a given ontology term. Returns empty list if no synonyms found.
        Raises ValueError if term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_synonyms("CL:0000019")
        ['sperm cell', 'spermatozoid', 'spermatozoon']

        :param term_id: str ontology term to fetch synonyms for
        :return: List[str] synonyms for the term
        """
        if term_id in VALID_NON_ONTOLOGY_TERMS:
            return []
        ontology_name = self._parse_ontology_name(term_id)
        synonyms: List[str] = self.cxg_schema.ontology(ontology_name)[term_id].get("synonyms", [])
        return synonyms

    def map_term_synonyms(self, term_ids: List[str]) -> Dict[str, List[str]]:
        """
        Fetch the synonym labels for a given list of ontology terms. Raises ValueError if term ID is not valid member of
        a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.map_term_synonyms(["CL:0000005", "CL:0000019"])
        {'CL:0000005': ['fibroblast neural crest derived'], 'CL:0000019': ['sperm cell', 'spermatozoid', 'spermatozoon']}

        :param term_ids: list of str ontology terms to fetch synonyms for
        :return: Dict[str, List[str]] mapping term IDs to their respective synonym lists
        """
        return {term_id: self.get_term_synonyms(term_id) for term_id in term_ids}

    def get_term_id_by_label(self, term_label: str, ontology_name: str) -> Optional[str]:
        """
        Fetch the ontology term ID from a given human-readable label. Filters by ontology_name. Raises ValueError if
        ontology_name is not a supported ontology.

        Returns None if term ID is not valid member of a supported ontology.

        Example
        >>> from cellxgene_ontology_guide.ontology_parser import OntologyParser
        >>> ontology_parser = OntologyParser()
        >>> ontology_parser.get_term_id_by_label("neural crest derived fibroblast", "CL")
        'CL:0000005'

        :param term_label: str human-readable label to fetch term ID for
        :param ontology_name: str name of ontology to search for term label in
        :return: Optional[str] term IDs with that label, or None if the label is not found in the ontology
        """
        ontology_term_label_to_id_map = self.get_term_label_to_id_map(ontology_name)
        return ontology_term_label_to_id_map.get(term_label)
