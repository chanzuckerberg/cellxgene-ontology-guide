from enum import Enum


class OntologyGuideEnum(Enum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Ontology(OntologyGuideEnum):
    """
    Enum for the set of ontologies supported by CZ CellXGene.
    """

    CL = "CL"
    EFO = "EFO"
    MONDO = "MONDO"
    UBERON = "UBERON"
    HANCESTRO = "HANCESTRO"
    HSAPDV = "HsapDv"
    MMUSDV = "MmusDv"
    PATO = "PATO"
    NCBITAXON = "NCBITaxon"


class OntologyVariant(OntologyGuideEnum):
    """
    Enum for the standard set of ontology variants. Each is curated for a specific purpose.

    See https://oboacademy.github.io/obook/explanation/owl-format-variants/ for more information on the distinction
    and use-cases for each variant.
    """

    FULL = "full"
    BASE = "base"
    SIMPLE = "simple"
    BASIC = "basic"


class OntologyFileType(OntologyGuideEnum):
    """
    Enum for the standard set of ontology file types. Each requires different parsing tools, but relay the same
    information.
    """

    OWL = "owl"
    OBO = "obo"
    JSON = "json"
