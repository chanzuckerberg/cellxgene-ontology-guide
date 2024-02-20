from cellxgene_ontology_guide import query


def test_get_ancestors():
    ancestors = query.get_ancestors("UBERON:0000966")
    assert len(ancestors) == 39
