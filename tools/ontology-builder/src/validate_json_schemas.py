import concurrent.futures
import json
import logging
import os.path
import sys
from typing import Iterable, Tuple

import env
import zstandard as zstd
from jsonschema import validate
from referencing import Registry, Resource

logging.basicConfig(level=logging.INFO)
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


def main(path: str = env.ONTOLOGY_ASSETS_DIR) -> None:
    """
    Verify the curated JSON lists match their respective JSON schema in asset-schemas
    :param path: The destination path for the json files
    :return:
    """
    registry = register_schemas()
    files = os.listdir(path)

    def verify_json_file(file: str) -> bool:
        if file.endswith(".json"):
            return verify_json(get_schema_file_name(file), os.path.join(path, file), registry)
        elif file.endswith(".json.zst"):
            return verify_json(get_schema_file_name("all_ontology"), os.path.join(path, file), registry)
        return True  # Ignore non-json files

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(verify_json_file, files))

    if not all(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
