from cellxgene_ontology_guide import query


def test_get_ancestors():
    # TODO: use mock all_ontology pytest fixture
    ancestors = query.get_ancestors("UBERON:0000966")
    assert len(ancestors) == 39
