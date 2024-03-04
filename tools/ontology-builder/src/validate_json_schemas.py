import json
import logging
import os.path
import sys

import env
from jsonschema import validate

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def verify_json(schema_file_name: str, json_file_name: str) -> bool:
    """
    Verify that the json files match the schema
    :return: if the json file matches the schema
    """
    logger.info(f"Verifying {json_file_name} against {schema_file_name}")
    try:
        with open(schema_file_name, "r") as f:
            schema = json.load(f)

        with open(json_file_name, "r") as f:
            data = json.load(f)
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
    if not all(
        [
            verify_json(
                os.path.join(env.SCHEMA_DIR, "system_list_schema.json"), os.path.join(path, "system_list.json")
            ),
            verify_json(os.path.join(env.SCHEMA_DIR, "organ_list_schema.json"), os.path.join(path, "organ_list.json")),
            verify_json(
                os.path.join(env.SCHEMA_DIR, "tissue_general_list_schema.json"),
                os.path.join(path, "tissue_general_list.json"),
            ),
            verify_json(
                os.path.join(env.SCHEMA_DIR, "cell_class_list_schema.json"), os.path.join(path, "cell_class_list.json")
            ),
            verify_json(
                os.path.join(env.SCHEMA_DIR, "cell_subclass_list_schema.json"),
                os.path.join(path, "cell_subclass_list.json"),
            ),
            verify_json(
                os.path.join(env.SCHEMA_DIR, "ontology_info_schema.json"), os.path.join(path, "ontology_info.json")
            ),
        ]
    ):
        sys.exit(1)


if __name__ == "__main__":
    main()
