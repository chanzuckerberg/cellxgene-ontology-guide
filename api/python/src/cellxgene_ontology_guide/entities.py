from enum import Enum


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
