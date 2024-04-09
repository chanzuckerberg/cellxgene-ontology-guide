from collections import Counter
from enum import Enum
from typing import Any, Dict, List


class Ontology(Enum):
    """
    Enum for the set of ontologies supported by CZ CellXGene.
    """

    CL = "cl"
    EFO = "efo"
    MONDO = "mondo"
    UBERON = "uberon"
    HANCESTRO = "hancestro"
    HsapDv = "hsapdv"
    MmusDv = "mmusdv"
    PATO = "pato"
    NCBITaxon = "ncbitaxon"


class CuratedOntologyTermList(Enum):
    """
    Enum for the set of curated ontology term lists supported by CZ CellXGene
    """

    CELL_CLASS = "cell_class"
    CELL_SUBCLASS = "cell_subclass"
    ORGAN = "organ"
    SYSTEM = "system"
    TISSUE_GENERAL = "tissue_general"
    UBERON_DEVELOPMENT_STAGE = "uberon_development_stage"


class OntologyNode:
    """
    Class to represent an ontology term and its subclasses
    """

    def __init__(self, term_id: str, name: str):
        self._term_id = term_id
        self._name = name
        self._children: List["OntologyNode"] = []
        self._term_counter: Counter[str] = Counter({self.term_id: 1})

    @property
    def term_id(self) -> str:
        """
        Ontology term ID represented by this OntologyNode.
        """
        return self._term_id

    @property
    def name(self) -> str:
        """
        Human-readable label for ontology term represented by this OntologyNode.
        """
        return self._name

    @property
    def children(self) -> List["OntologyNode"]:
        """
        List of children OntologyNode of this OntologyNode.
        """
        return self._children

    @property
    def term_counter(self) -> Counter[str]:
        """
        Mapping of unique ontology term ID descendants of this OntologyNode to the number of times each term
        appears in the graph rooted at this node.
        :return:
        """
        return self._term_counter

    def add_child(self, child: "OntologyNode") -> None:
        self._children.append(child)
        self._term_counter.update(child.term_counter)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "term_id": self.term_id,
            "name": self.name,
            "children": [child.to_dict() for child in self.children],
        }
