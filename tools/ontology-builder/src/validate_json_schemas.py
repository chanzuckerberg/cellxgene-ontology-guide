import functools
import json
import logging
import os.path
import re
import sys
from typing import Any, Dict, FrozenSet, Iterable, List, Set, Tuple

import env
import zstandard as zstd
from jsonschema import validate
from referencing import Registry, Resource

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def get_schema_file_name(json_file_name: str, schema_dir: str = env.SCHEMA_DIR) -> str:
    """
    Get the schema from the json file
    :return: the schema
    """
    return os.path.join(schema_dir, f"{json_file_name.split('.')[0]}_schema.json")


def register_schemas(schema_dir: str = env.SCHEMA_DIR) -> Registry:
    """
    Load all the schemas from the schema directory
    :return: a dictionary of schemas
    """

    def create_resource() -> Iterable[Tuple[str, Resource]]:
        for file_name in os.listdir(schema_dir):
            if file_name.endswith(".json"):
                with open(os.path.join(schema_dir, file_name)) as f:
                    try:
                        yield file_name, Resource.from_contents(json.load(f))
                    except Exception:
                        logger.exception(f"Error loading {file_name}")
                        raise

    registry = Registry().with_resources(create_resource())
    return registry


def verify_json(schema_file_name: str, json_file_name: str, registry: Registry) -> bool:
    """
    Verify that the json files match the schema
    :return: if the json file matches the schema
    """
    logger.info(f"Verifying {json_file_name} against {schema_file_name}")
    try:
        with open(schema_file_name) as f:
            schema = json.load(f)
    except Exception:
        logger.exception(f"Error loading {schema_file_name}")
        return False

    try:
        if json_file_name.endswith(".json.zst"):
            with open(json_file_name, "rb") as inf:
                data = inf.read()
            dctx = zstd.ZstdDecompressor()
            decom_str = dctx.decompress(data).decode("utf-8")
            data = json.loads(decom_str)
        else:
            with open(json_file_name) as f:
                data = json.load(f)
    except Exception:
        logger.exception(f"Error loading {json_file_name}")
        return False

    try:
        validate(instance=data, schema=schema, registry=registry)
    except Exception:
        logger.exception(f"Error validating {json_file_name} against {schema_file_name}")
        return False
    return True


@functools.cache
def _term_id_pattern(schema_dir: str = env.SCHEMA_DIR) -> "re.Pattern[str]":
    """
    Build a single compiled alternation of every supported term ID pattern.

    Derived from ontology_term_id_schema.json rather than hardcoded, so that adding an ontology to
    the schema automatically extends this check.

    :param str schema_dir: directory holding the asset schemas
    :rtype re.Pattern[str]
    :return compiled pattern matching any supported term ID
    """
    with open(os.path.join(schema_dir, "ontology_term_id_schema.json")) as f:
        definitions = json.load(f)["definitions"]
    patterns = [definitions[ref["$ref"].split("/")[-1]]["pattern"] for ref in definitions["supported_term_id"]["anyOf"]]
    return re.compile("|".join(f"(?:{pattern})" for pattern in patterns))


@functools.cache
def _term_fields(schema_dir: str = env.SCHEMA_DIR) -> Tuple[FrozenSet[str], FrozenSet[str]]:
    """
    Read the permitted and required per-term fields out of all_ontology_schema.json.

    :param str schema_dir: directory holding the asset schemas
    :rtype Tuple[FrozenSet[str], FrozenSet[str]]
    :return (permitted field names, required field names)
    """
    with open(os.path.join(schema_dir, "all_ontology_schema.json")) as f:
        term_schema = json.load(f)["additionalProperties"]
    return frozenset(term_schema["properties"]), frozenset(term_schema["required"])


def validate_ontology_terms(ontology_name: str, terms: Dict[str, Any]) -> bool:
    """
    Validate a generated ontology term dict against all_ontology_schema.json.

    Equivalent to running jsonschema against the asset, but ~500x faster: the schema checks its term ID
    pattern once per key occurrence, and NCBITaxon alone has ~57M ancestor references drawn from only
    ~2.7M distinct IDs. Here each distinct ID is checked once, and because ancestors are a subset of the
    file's own terms, ancestor references are validated by set difference rather than by regex.

    Also enforces referential integrity -- every ancestor must be a term defined in the same file -- which
    the JSON schema cannot express and which is the failure mode actually worth catching.

    :param str ontology_name: ontology being validated, for error messages
    :param Dict[str, Any] terms: generated term_id -> metadata mapping
    :rtype bool
    :return True if the term dict is valid
    """
    matches_term_id = _term_id_pattern().match
    permitted, required = _term_fields()
    errors: List[str] = []

    def record(message: str) -> None:
        if len(errors) < 10:  # a malformed asset produces millions of these; the first few suffice
            errors.append(message)

    for term_id in terms:
        if not matches_term_id(term_id):
            record(f"malformed term ID {term_id!r}")

    referenced: Set[str] = set()
    for term_id, metadata in terms.items():
        if missing := required - metadata.keys():
            record(f"{term_id} is missing required field(s) {sorted(missing)}")
        if unexpected := metadata.keys() - permitted:
            record(f"{term_id} has unexpected field(s) {sorted(unexpected)}")
        if not isinstance(metadata.get("label"), str):
            record(f"{term_id} has a non-string label {metadata.get('label')!r}")
        if not isinstance(metadata.get("deprecated"), bool):
            record(f"{term_id} has a non-boolean deprecated {metadata.get('deprecated')!r}")
        ancestors = metadata.get("ancestors")
        if not isinstance(ancestors, dict):
            record(f"{term_id} has non-object ancestors {ancestors!r}")
            continue
        referenced.update(ancestors)
        for ancestor, distance in ancestors.items():
            # bool is a subclass of int, but a boolean distance is not a valid integer distance
            if not isinstance(distance, int) or isinstance(distance, bool):
                record(f"{term_id} has a non-integer distance {distance!r} to ancestor {ancestor}")

    # Ancestors are expected to be terms of this same file. Anything else is either a malformed ID or a
    # reference to a term that was filtered out of the asset, and both make the ancestor unresolvable.
    for dangling in sorted(referenced - terms.keys()):
        record(f"ancestor {dangling} is referenced but not defined in this ontology")

    if errors:
        logger.error("%s failed validation:\n\t%s", ontology_name, "\n\t".join(errors))
        return False
    return True


def main(path: str = env.ONTOLOGY_ASSETS_DIR) -> None:
    """
    Verify the curated JSON lists match their respective JSON schema in asset-schemas
    :param path: The destination path for the json files
    :return:
    """
    registry = register_schemas()
    files = os.listdir(path)
    _json = [
        verify_json(get_schema_file_name(file), os.path.join(path, file), registry)
        for file in files
        if file.endswith(".json")
    ]
    _json_gz = [
        verify_json(get_schema_file_name("all_ontology"), os.path.join(path, file), registry)
        for file in files
        if file.endswith(".json.gz")
    ]
    if not all(_json + _json_gz):
        sys.exit(1)


if __name__ == "__main__":
    main()
