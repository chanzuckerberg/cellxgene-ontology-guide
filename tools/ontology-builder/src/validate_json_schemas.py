import gzip
import json
import logging
import os.path
import sys

import env
from jsonschema import validate

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def get_schema_file_name(json_file_name: str, schema_dir: str = env.SCHEMA_DIR) -> str:
    """
    Get the schema from the json file
    :return: the schema
    """
    return os.path.join(schema_dir, f"{json_file_name.split('.')[0]}_schema.json")


def verify_json(schema_file_name: str, json_file_name: str) -> bool:
    """
    Verify that the json files match the schema
    :return: if the json file matches the schema
    """
    logger.info(f"Verifying {json_file_name} against {schema_file_name}")
    try:
        with open(schema_file_name) as f:
            schema = json.load(f)
    except Exception as e:
        logger.exception(f"Error loading {schema_file_name}: {e}")
        return False

    try:
        if json_file_name.endswith(".json.gz"):
            with gzip.open(json_file_name, "rt") as f:
                data = json.load(f)
        else:
            with open(json_file_name) as f:
                data = json.load(f)
    except Exception as e:
        logger.exception(f"Error loading {json_file_name}: {e}")
        return False

    try:
        validate(instance=data, schema=schema)
    except Exception as e:
        logger.exception(f"Error validating {json_file_name} against {schema_file_name}: {e}")
        return False
    return True


def main(path: str = env.ONTOLOGY_ASSETS_DIR) -> None:
    """
    Verify the curated JSON lists match their respective JSON schema in artifact-schemas
    :param path: The destination path for the json files
    :return:
    """
    files = os.listdir(path)
    if not (
        all(
            verify_json(get_schema_file_name(file), os.path.join(path, file))
            for file in files
            if file.endswith(".json")
        )
        and all(
            verify_json(get_schema_file_name("all_ontology"), os.path.join(path, file))
            for file in files
            if file.endswith(".json.gz")
        )
    ):
        sys.exit(1)


if __name__ == "__main__":
    main()
