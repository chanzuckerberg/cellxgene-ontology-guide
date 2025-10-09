"""Integration tests that exercise ontology queries against packaged data assets."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterator, Tuple

import cellxgene_ontology_guide._constants as constants
import cellxgene_ontology_guide.curated_ontology_term_lists as curated_module
import cellxgene_ontology_guide.supported_versions as supported_versions
import pytest
from cellxgene_ontology_guide._constants import VALID_NON_ONTOLOGY_TERMS
from cellxgene_ontology_guide.entities import CuratedOntologyTermList
from cellxgene_ontology_guide.ontology_parser import OntologyParser

TermRecord = Tuple[str, Dict[str, object]]


def _iter_term_records(ontology_terms: Dict[str, Dict[str, object]]) -> Iterator[TermRecord]:
    for term_id, payload in ontology_terms.items():
        if isinstance(payload, dict) and payload:
            yield term_id, payload


@pytest.fixture(autouse=True)
def configure_data_root(monkeypatch: pytest.MonkeyPatch) -> None:
    data_root = Path(constants.PACKAGE_ROOT) / "data"
    assert data_root.exists(), f"Expected packaged ontology data at {data_root}"

    monkeypatch.setattr(constants, "DATA_ROOT", str(data_root))
    monkeypatch.setattr(supported_versions, "DATA_ROOT", str(data_root))
    monkeypatch.setattr(curated_module, "DATA_ROOT", str(data_root))

    supported_versions.clear_ontology_file_cache()
    curated_module.get_curated_ontology_term_list.cache_clear()

    yield

    supported_versions.clear_ontology_file_cache()
    curated_module.get_curated_ontology_term_list.cache_clear()


def test_all_supported_ontologies_are_queryable():
    versions = supported_versions.load_supported_versions()
    assert versions, "Expected at least one schema version in ontology_info.json"

    for schema_version in versions:
        parser = OntologyParser(schema_version=schema_version)
        schema = parser.cxg_schema

        for ontology_name in schema.supported_ontologies:
            terms = schema.ontology(ontology_name)
            assert (
                isinstance(terms, dict) and terms
            ), f"Ontology {ontology_name} for schema {schema_version} should be a non-empty dict"

            sample_term_id = None
            sample_label = None
            for term_id, payload in _iter_term_records(terms):
                sample_term_id = term_id
                sample_label = payload.get("label") if isinstance(payload, dict) else None
                break

            assert (
                sample_term_id
            ), f"Schema {schema_version} ontology {ontology_name} contains no queryable term metadata"

            assert parser.is_valid_term_id(sample_term_id, ontology=ontology_name)

            metadata = parser.get_term_metadata(sample_term_id)
            assert isinstance(metadata, dict)

            ancestors = parser.get_term_ancestors(sample_term_id, include_self=True)
            assert isinstance(ancestors, list)

            if sample_label:
                label = parser.get_term_label(sample_term_id)
                assert label == sample_label
                assert parser.get_term_id_by_label(sample_label, ontology_name) == sample_term_id


def test_curated_term_lists_map_to_supported_terms():
    parser = OntologyParser()

    for curated_list in CuratedOntologyTermList:
        terms = curated_module.get_curated_ontology_term_list(curated_list)
        assert isinstance(terms, list) and terms, f"Curated list {curated_list} must return a non-empty list"

        for term in terms:
            assert isinstance(term, str)
            if term in VALID_NON_ONTOLOGY_TERMS:
                continue
            assert parser.is_valid_term_id(term), f"Curated term {term} in {curated_list} is not queryable"


def test_query_metadata_for_sample_curated_terms():
    parser = OntologyParser()

    queried_terms = []

    for curated_list in CuratedOntologyTermList:
        terms = curated_module.get_curated_ontology_term_list(curated_list)
        for term in terms:
            if term in VALID_NON_ONTOLOGY_TERMS:
                continue

            label = parser.get_term_label(term)
            assert isinstance(label, str) and label

            description = parser.get_term_description(term)
            assert description is None or isinstance(description, str)

            synonyms = parser.get_term_synonyms(term)
            assert isinstance(synonyms, list)

            ancestors = parser.get_term_ancestors(term)
            assert isinstance(ancestors, list)

            queried_terms.append(term)
            break

    assert queried_terms, "Expected to query at least one curated ontology term"
