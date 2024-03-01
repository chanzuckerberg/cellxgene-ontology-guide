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


class OntologyVariant(Enum):
    """
    Enum for the standard set of ontology variants. Each is curated for a specific purpose.

    See https://oboacademy.github.io/obook/explanation/owl-format-variants/ for more information on the distinction
    and use-cases for each variant.
    """

    FULL = "full"
    BASE = "base"
    SIMPLE = "simple"
    BASIC = "basic"


class OntologyFileType(Enum):
    """
    Enum for the standard set of ontology file types. Each requires different parsing tools, but relay the same
    information.
    """

    OWL = "owl"
    OBO = "obo"
    JSON = "json"
