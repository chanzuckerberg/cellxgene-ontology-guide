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


class OntologyTreeNode:
    """
    Class to represent a node in an ontology term tree.
    """

    def __init__(self, term_id: str, children: List["OntologyTreeNode"] = None, term_counter: Dict[str, int] = None):
        self.term_id = term_id
        self.children = children if children else []
        self.term_counter = term_counter if term_counter else Counter({self.term_id: 1})

    def to_dict(self) -> Dict[str, Any]:
        return {self.term_id: [child.to_dict() for child in self.children]}
