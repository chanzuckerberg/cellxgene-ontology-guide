from cellxgene_ontology_guide.entities import Ontology
from cellxgene_ontology_guide.supported_versions import load_supported_versions


def test_all_supported_ontologies_in_dataclass():
    """
    Test that all supported ontologies are defined in the Ontology enum (and deprecated ontologies removed).
    Do not include additional ontologies.
    """
    ontology_info = load_supported_versions()
    supported_ontologies = set()
    for _, version_info in ontology_info.items():
        for ontology, _ in version_info["ontologies"].items():
            supported_ontologies.add(ontology)

    assert supported_ontologies == {ontology.name for ontology in Ontology}
