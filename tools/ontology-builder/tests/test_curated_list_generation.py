import pytest
from curation_list_generator import main, reformat_ontology_term_ids


@pytest.mark.parametrize(
    "test,expected",
    [(["CL_000001", "CL_000002"], ["CL:000001", "CL:000002"]), (["CL_000001"], ["CL:000001"]), ([], [])],
)
def test_reformat_ontology_term_ids(test, expected):
    assert reformat_ontology_term_ids(test) == expected


def test_main(tmp_path):
    main(tmp_path)
    assert (tmp_path / "system_list.json").exists()
    assert (tmp_path / "organ_list.json").exists()
    assert (tmp_path / "tissue_general_list.json").exists()
    assert (tmp_path / "cell_class_list.json").exists()
    assert (tmp_path / "cell_subclass_list.json").exists()
