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
