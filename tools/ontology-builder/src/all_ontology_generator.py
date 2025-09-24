import argparse
import gzip
import json
import logging
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta
from threading import Thread
from typing import Any, Dict, Iterator, List, Set
from urllib.error import HTTPError, URLError

import env
import owlready2
from cellxgene_ontology_guide.supported_versions import get_latest_schema_version
from validate_json_schemas import register_schemas, verify_json


def get_ontology_info_file(ontology_info_file: str = env.ONTOLOGY_INFO_FILE) -> Any:
    """
    Read ontology information from file

    :param str ontology_info_file: path to file with ontology information

    :rtype Any
    :return ontology information
    """
    with open(ontology_info_file, "r") as f:
        return json.load(f)


def save_ontology_info(
    ontology_info: Dict[str, Any],
    latest_ontology_info: Dict[str, Any],
    ontology_info_file: str = env.ONTOLOGY_INFO_FILE,
    latest_ontology_info_file: str = env.LATEST_ONTOLOGY_INFO_FILE,
) -> None:
    """
    Save ontology information to file

    :param Dict[str, Any] ontology_info: ontology information to save
    :param str ontology_info_file: path to file to save ontology information

    :rtype None
    """
    with open(ontology_info_file, "w") as f:
        json.dump(ontology_info, f, indent=2)

    with open(latest_ontology_info_file, "w") as f:
        json.dump(latest_ontology_info, f, indent=2)


def _download_ontologies(ontology_info: Dict[str, Any], output_dir: str = env.RAW_ONTOLOGY_DIR) -> None:
    """
    Downloads the ontology files specified in 'ontology_info.json' into 'output_dir'

    :param str ontology_info: a dictionary with ontology names as keys and their respective URLs and versions
    :param str output_dir: path to writable directory where ontology files will be downloaded to

    :rtype None
    """

    def download(_ontology: str, _url: str) -> None:
        logging.info(f"Start Downloading {_url}")
        # Format of ontology (handles cases where they are compressed)
        download_format = _url.split(".")[-1]
        output_file = os.path.join(output_dir, _ontology + ".owl")

        if download_format == "tsv":
            output_file = os.path.join(output_dir, _ontology + ".sssom.tsv")
            urllib.request.urlretrieve(_url, output_file)
        elif download_format == "obo":
            # Download OBO file first
            temp_obo_file = os.path.join(output_dir, _ontology + ".obo")
            urllib.request.urlretrieve(_url, temp_obo_file)
            # Convert OBO to OWL using Docker
            _convert_obo_to_owl(temp_obo_file, output_file)
            # Clean up temporary OBO file
            os.remove(temp_obo_file)
        elif download_format == "gz":
            urllib.request.urlretrieve(_url, output_file + ".gz")
            _decompress(output_file + ".gz", output_file)
            os.remove(output_file + ".gz")
        else:
            urllib.request.urlretrieve(_url, output_file)

        if _ontology == "CL" and output_file.endswith(".owl"):
            _remove_punning_terms_from_cl(output_file)

        logging.info(f"Finish Downloading {_url}")

    def _build_urls(_ontology: str) -> List[str]:
        onto_ref_data = ontology_info[_ontology]
        base_url = onto_ref_data["source"].replace("{version}", onto_ref_data["version"])

        download_urls = [base_url.replace("{filename}", onto_ref_data["filename"])]
        # this assumes the cross-ontology-map is part of the same repository.
        if onto_ref_data.get("cross_ontology_mapping"):
            download_urls.append(base_url.replace("{filename}", onto_ref_data["cross_ontology_mapping"]))
        return download_urls

    def _check_url(_ontology: str, _url: str) -> None:
        try:
            urllib.request.urlopen(_url)
        except HTTPError as e:
            raise Exception(f"{_ontology} with pinned URL {_url} returns status code {e.code}") from e
        except URLError as e:
            raise Exception(f"{_ontology} with pinned URL {_url} fails due to {e.reason}") from e

    threads = []
    for ontology, _ in ontology_info.items():
        urls = _build_urls(ontology)
        for url in urls:
            _check_url(ontology, url)
            t = Thread(target=download, args=(ontology, url))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()


def _decompress(infile: str, tofile: str) -> None:
    """
    Decompresses a gziped file

    :param str infile: path gziped file
    :param str tofile: path to output decompressed file

    :rtype None
    """
    with open(infile, "rb") as inf, open(tofile, "w", encoding="utf8") as tof:
        decom_str = gzip.decompress(inf.read()).decode("utf-8")
        tof.write(decom_str)


def _convert_obo_to_owl(obo_file: str, owl_output_file: str) -> None:
    """
    Convert an OBO file to OWL format using Docker with obolibrary/robot

    :param str obo_file: path to input OBO file (should be in raw-files directory)
    :param str owl_output_file: path to output OWL file (should be in raw-files directory)

    :rtype None
    """
    # Get relative paths from project root
    obo_relative_path = os.path.relpath(obo_file, env.RAW_ONTOLOGY_DIR)
    owl_relative_path = os.path.relpath(owl_output_file, env.RAW_ONTOLOGY_DIR)

    # Docker command to convert OBO to OWL
    docker_cmd = [
        "docker",
        "run",
        "-v",
        f"{env.RAW_ONTOLOGY_DIR}:/work",
        "-w",
        "/work",
        "--rm",
        "obolibrary/robot",
        "robot",
        "convert",
        "--input",
        f"./{obo_relative_path}",
        "--format",
        "owl",
        "-o",
        f"./{owl_relative_path}",
    ]

    logging.info(f"Converting {obo_file} to OWL format using Docker")
    logging.info(f"Running command: {' '.join(docker_cmd)}")

    try:
        result = subprocess.run(docker_cmd, check=True, capture_output=True, text=True)
        logging.info(f"Successfully converted {obo_file} to {owl_output_file}")
        if result.stdout:
            logging.info(f"Docker output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to convert {obo_file} to OWL format: {e}")
        if e.stdout:
            logging.error(f"Docker stdout: {e.stdout}")
        if e.stderr:
            logging.error(f"Docker stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        logging.error("Docker not found. Please make sure Docker is installed and available in PATH")
        raise


def _remove_punning_terms_from_cl(onto_file: str) -> None:
    """
    Remove punning terms from CL ontology file using robot running in docker.
    This is due to owlready2 not supporting "punning" see:
    https://github.com/obophenotype/cell-ontology/issues/3237#issuecomment-3207136184

    robot remove --input cl.owl \
             --term http://purl.obolibrary.org/obo/STATO_0000416 \
             --term http://purl.obolibrary.org/obo/STATO_0000663 \
             --allow-punning true \
             --output cl-without-stato.owl

    :param str onto_file: path to input OWL file (should be in raw-files directory)

    :rtype None
    """
    # Get relative paths from project root
    owl_relative_path = os.path.relpath(onto_file, env.RAW_ONTOLOGY_DIR)
    cleaned_owl_output_file = onto_file.replace(".owl", "-cleaned.owl")
    cleaned_owl_relative_path = os.path.relpath(cleaned_owl_output_file, env.RAW_ONTOLOGY_DIR)

    # Docker command to remove punning terms using robot
    docker_cmd = [
        "docker",
        "run",
        "-v",
        f"{env.RAW_ONTOLOGY_DIR}:/work",
        "-w",
        "/work",
        "--rm",
        "obolibrary/robot",
        "robot",
        "remove",
        "--input",
        f"./{owl_relative_path}",
        "--term",
        "http://purl.obolibrary.org/obo/STATO_0000416",
        "--term",
        "http://purl.obolibrary.org/obo/STATO_0000663",
        "--allow-punning",
        "true",
        "--output",
        f"./{cleaned_owl_relative_path}",
    ]

    logging.info(f"Removing punning terms from {onto_file} using Docker")
    logging.info(f"Running command: {' '.join(docker_cmd)}")

    try:
        result = subprocess.run(docker_cmd, check=True, capture_output=True, text=True)
        logging.info(f"Successfully removed punning terms from {onto_file}, output saved to {cleaned_owl_output_file}")
        if result.stdout:
            logging.info(f"Docker output: {result.stdout}")
        # Replace original file with cleaned file
        os.replace(cleaned_owl_output_file, onto_file)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to remove punning terms from {onto_file}: {e}")
        if e.stdout:
            logging.error(f"Docker stdout: {e.stdout}")
        if e.stderr:
            logging.error(f"Docker stderr: {e.stderr}")
        raise
    except FileNotFoundError:
        logging.error("Docker not found. Please make sure Docker is installed and available in PATH")
        raise


def _load_ontology_object(onto_file: str) -> owlready2.entity.ThingClass:
    """
    Read ontology data from file and write into a python object

    :param onto_file: filepath to ontology file

    :return: owlready2.entity.ThingClass: Ontology Term Object, with metadata parsed from ontology file
    """
    world = owlready2.World()
    onto = world.get_ontology(onto_file)
    onto.load()
    return onto


def _load_cross_ontology_map(working_dir: str, ontology_info: Any) -> Dict[str, Dict[str, str]]:
    """
    Load cross ontology mapping from file and write into python dict

    :param str working_dir: path to folder with ontology files
    :param ANY ontology_info: the ontology references used to download the ontology files. It follows this [schema](
    ./asset-schemas/ontology_info_schema.json)
    :return Dict[str, Dict[str, str]]: per ontology, a dict of known equivalent term IDs in other ontologies
    """
    cross_ontology_map: Dict[str, Dict[str, str]] = {}
    cross_ontologies = [
        ontology for ontology, info in ontology_info.items() if info.get("cross_ontology_mapping") is not None
    ]
    for cross_ontology in cross_ontologies:
        cross_ontology_map[cross_ontology] = {}
        # load tsv, assume SSSOM format for now
        try:
            with open(os.path.join(working_dir, f"{cross_ontology}.sssom.tsv"), "r") as f:
                for line in f:
                    if not line.startswith("#") and not line.startswith("subject_id"):
                        cols = line.split("\t")
                        cross_ontology_map[cross_ontology][cols[3]] = cols[0]
        except FileNotFoundError:
            logging.warning(f"Cross ontology mapping file for {cross_ontology} not found")
    return cross_ontology_map


def _get_ancestors(onto_class: owlready2.entity.ThingClass, allowed_ontologies: list[str]) -> Dict[str, int]:
    """
    Returns a list of unique ancestor ontology term ids of the given onto class. Only returns those belonging to
    ontology_name, it will format the id from the form CL_xxxx to CL:xxxx. Ancestors are returned in ascending order
    of distance from the given term.

    :param owlready2.entity.ThingClass onto_class: the class for which ancestors will be retrieved
    :param listp[str] allowed_ontologies: only ancestors from these ontologies will be kept

    :rtype List[str]
    :return list of ancestors (term ids), it could be empty
    """
    ancestors: Dict[str, int] = dict()
    queue = [(onto_class, 1)]
    while queue:
        term, distance = queue.pop(0)
        for parent in term.is_a:
            # a branch ancestor is defined as having a "part_of" (BFO_0000050) relationship with a term
            if (
                hasattr(parent, "property")
                and parent.property.name == "BFO_0000050"
                and isinstance(parent.value, owlready2.entity.ThingClass)
            ):
                branch_ancestor_name = parent.value.name.replace("obo.", "").replace("_", ":")
                if branch_ancestor_name in ancestors:
                    ancestors[branch_ancestor_name] = min(ancestors[branch_ancestor_name], distance)
                else:
                    queue.append((parent.value, distance + 1))
                    if branch_ancestor_name.split(":")[0] in allowed_ontologies:
                        ancestors[branch_ancestor_name] = distance
            elif hasattr(parent, "name") and not hasattr(parent, "Classes"):
                parent_name = parent.name.replace("_", ":")
                if parent_name in ancestors:
                    ancestors[parent_name] = min(ancestors[parent_name], distance)
                else:
                    queue.append((parent, distance + 1))
                    ancestors[parent_name] = distance

    # filter out ancestors that are not from the ontology we are currently processing
    return {
        ancestor: distance
        for ancestor, distance in sorted(ancestors.items(), key=lambda item: item[1])
        if ancestor.split(":")[0] in allowed_ontologies
    }


def _extract_cross_ontology_terms(
    term_id: str, map_to_cross_ontologies: List[str], cross_ontology_map: Dict[str, Dict[str, str]]
) -> Dict[str, str]:
    """
    Extract mapping of ontology term ID to equivalent term IDs in another ontology.

    :param: term_id: Ontology Term ID to find equivalent terms for
    :param: map_to_cross_ontologies: List of ontologies to map equivalent terms to
    :param: cross_ontology_map: str for each ontology with a mapping, map to known equivalent terms in other ontologies
    :return: Dict[str, str] map of ontology to the equivalent term ID in that ontology for the given
    term_id, i.e. ZFA:0000001 -> {"UBERON": "UBERON:0000001", "CL": "CL:0000001",...}
    """
    cross_ontology_terms = {}
    for cross_ontology in map_to_cross_ontologies:
        if term_id in cross_ontology_map[cross_ontology]:
            cross_ontology_terms[cross_ontology] = cross_ontology_map[cross_ontology][term_id]
    return cross_ontology_terms


def _extract_ontology_term_metadata(
    onto: owlready2.entity.ThingClass,
    allowed_ontologies: List[str],
    map_to_cross_ontologies: List[str],
    cross_ontology_map: Dict[str, Dict[str, str]],
    id_separator: str = ":",
) -> Dict[str, Any]:
    """
    Extract relevant metadata from ontology object and save into a dictionary following our JSON Schema

    :param: onto: Ontology Object to Process
    :param: allowed_ontologies: List of term prefixes to filter out terms that are not direct children from this
    ontology
    :param: map_to_cross_ontologies: List of ontologies to map equivalent terms to
    :param: cross_ontology_map: str for each ontology with a mapping, map to known equivalent terms in other ontologies
    :param: id_separator: separator to use for ontology term IDs, typically ":" or "_"
    :return: Dict[str, Any] map of ontology term IDs to pertinent metadata from ontology files
    """
    term_dict: Dict[str, Any] = dict()
    for onto_term in onto.classes():
        term_id = onto_term.name.replace("_", id_separator)

        # Skip terms that are not direct children from this ontology
        term_id_parts = term_id.split(id_separator)
        if len(term_id_parts) > 2 or term_id_parts[0] not in allowed_ontologies:
            continue
        # Gets ancestors
        ancestors = _get_ancestors(onto_term, allowed_ontologies)

        # Special Case: skip the current term if it is an NCBI Term, but not a descendant of 'NCBITaxon:33208' (Animal)
        if onto.name == "NCBITaxon" and "NCBITaxon:33208" not in ancestors:
            continue

        term_dict[term_id] = dict()
        term_dict[term_id]["ancestors"] = ancestors

        if cross_ontology_terms := _extract_cross_ontology_terms(term_id, map_to_cross_ontologies, cross_ontology_map):
            term_dict[term_id]["cross_ontology_terms"] = cross_ontology_terms

        term_dict[term_id]["label"] = onto_term.label[0] if onto_term.label else ""

        # optional description, if available
        if getattr(onto_term, "IAO_0000115", None):
            term_dict[term_id]["description"] = onto_term.IAO_0000115[0]
        # optional synonym list, if available
        if hasExactSynonym := getattr(onto_term, "hasExactSynonym", None):
            term_dict[term_id]["synonyms"] = [str(x) for x in hasExactSynonym]
        # Add the "deprecated" status and associated metadata if True
        term_dict[term_id]["deprecated"] = False
        if onto_term.deprecated and onto_term.deprecated.first():
            # if deprecated, include information to determine replacement term(s)
            term_dict[term_id]["deprecated"] = True
            if onto_term.comment:
                term_dict[term_id]["comments"] = [str(c) for c in onto_term.comment]
            # stores term tracking URL, such as a github issue discussing deprecated term
            if getattr(onto_term, "IAO_0000233", None):
                term_dict[term_id]["term_tracker"] = str(onto_term.IAO_0000233[0])
            # only need to record replaced_by OR considers
            if onto_term.IAO_0100001:
                # url --> term
                ontology_term = re.findall(r"[^\W_]+", str(onto_term.IAO_0100001[0]))
                # It is accepted that this term may not be in the same ontology as the original term.
                term_dict[term_id]["replaced_by"] = f"{ontology_term[-2]}:{ontology_term[-1]}"
            elif getattr(onto_term, "consider", None):
                term_dict[term_id]["consider"] = [str(c) for c in onto_term.consider]
    return term_dict


def get_ontology_file_name(ontology_name: str, ontology_version: str) -> str:
    return f"{ontology_name}-ontology-{ontology_version}.json.gz"


def check_version(onto_file: str, version: str) -> None:
    version_iri = version_info = ""
    with open(onto_file, "r") as f:
        for line in f:
            if "versioniri" in line.lower():
                if version in line or version.strip("v") in line:
                    return
                version_iri = line
            elif "versioninfo" in line.lower():
                if version in line or version.strip("v") in line:
                    return
                version_info = line
            elif version_iri and version_info:
                logging.warning(f"VersionIRI mismatch in {onto_file}: {version_iri.strip()}")
                logging.warning(f"VersionINFO mismatch in {onto_file}: {version_info.strip()}")
                break
        logging.warning(f"No version match found in {onto_file} for version {version}")


def _parse_ontologies(
    ontology_info: Any,
    working_dir: str = env.RAW_ONTOLOGY_DIR,
    output_path: str = env.ONTOLOGY_ASSETS_DIR,
) -> Iterator[str]:
    """
    Parse all ontology files in working_dir. Extracts information from all classes in the ontology file.
    The extracted information is written into a gzipped a json file with the following [schema](
    asset-schemas/all_ontology_schema.json):
    {
        "ontology_name":
            {
            "term_id": {
                "label": "..."
                "deprecated": True
                "ancestors": [
                    "ancestor1_term_id_1",
                    "ancestor2_term_id_2"
                    ]
                }
            }

            "term_id2": {
                ...
            }

            ...
            }
    }
    :param ANY ontology_info: the ontology references used to download the ontology files. It follows this [schema](
    ./asset-schemas/ontology_info_schema.json)
    :param str working_dir: path to folder with ontology files
    :param str output_path: path to output json files

    :rtype str
    :return: path to the output json file
    """
    cross_ontology_map = _load_cross_ontology_map(working_dir, ontology_info)
    for onto_file in os.listdir(working_dir):
        if not onto_file.endswith(".owl"):
            continue
        elif onto_file.rstrip(".owl") not in ontology_info:
            logging.info(f"Skipping {onto_file} as it is not in the ontology_info.json")
            continue
        onto_file_path = os.path.join(working_dir, onto_file)
        onto = _load_ontology_object(onto_file_path)

        version = ontology_info[onto.name].get("version")
        check_version(onto_file_path, version)

        output_file = os.path.join(output_path, get_ontology_file_name(onto.name, version))
        logging.info(f"Processing {output_file}")
        allowed_ontologies = [onto.name] + ontology_info[onto.name].get("additional_ontologies", [])
        map_to_cross_ontologies = ontology_info[onto.name].get("map_to", [])
        id_separator = ontology_info[onto.name].get("id_separator", ":")
        onto_dict = _extract_ontology_term_metadata(
            onto, allowed_ontologies, map_to_cross_ontologies, cross_ontology_map, id_separator
        )
        with gzip.GzipFile(output_file, mode="wb", mtime=0) as fp:
            fp.write(json.dumps(onto_dict, indent=2).encode("utf-8"))
        yield output_file


def update_ontology_info(ontology_info: Dict[str, Any]) -> Set[str]:
    """
    Update ontology_info in place by removing expired versions and returning a list of the ontology files that
    can be removed.
    :param ontology_info: the ontology information from ontology_info.json
    :return: a list of ontology files that can be removed
    """
    expired = list_expired_cellxgene_schema_version(ontology_info)  # find expired cellxgene schema versions
    current = set(ontology_info.keys()) - set(expired)  # find current cellxgene schema versions
    logging.info("Expired versions:\n\t", "\t\n".join(expired))

    def _get_ontology_files(schema_versions: List[str]) -> Set[str]:
        """
        find all ontologies that are in the list of schema_versions

        :param schema_versions: list of schema versions
        :return: ontology_files: set of ontology files
        """

        ontology_files = set()
        for version in schema_versions:
            for ontology, info in ontology_info[version]["ontologies"].items():
                ontology_files.add(get_ontology_file_name(ontology, info["version"]))
        return ontology_files

    expired_files = _get_ontology_files(expired)  # find all ontology files that are in the expired versions
    current_files = _get_ontology_files(list(current))  # find all ontology files that are in the current versions
    # find the ontology files that are in the expired versions but not in the current versions
    remove_files = expired_files - current_files
    # remove expired versions from ontology_info
    for version in expired:
        del ontology_info[version]
    return remove_files


def deprecate_previous_cellxgene_schema_versions(ontology_info: Dict[str, Any], current_version: str) -> None:
    """
    Deprecate previous versions of the cellxgene schema. This modifies the ontology_info.json file in place.
    :param ontology_info: the ontology information from ontology_info.json
    :param current_version: the current cellxgene schema version
    :return:
    """
    for schema_version in ontology_info:
        if schema_version != current_version and "deprecated_on" not in ontology_info[schema_version]:
            ontology_info[schema_version]["deprecated_on"] = datetime.now().strftime("%Y-%m-%d")


def resolve_version(schema_info: Dict[str, Any]) -> None:
    """
    Resolve the version of each ontology in the schema. If the version is not specified, it will be
    parsed from the version_url. This modifies the schema dict in place.
    :param schema_info: the schema information from ontology_info.json
    :return:
    """
    for ontology, info in schema_info["ontologies"].items():
        if info.get("version"):
            continue
        elif info.get("version_url"):
            try:
                # Special case for Cellosaurus
                if ontology == "CVCL":
                    request = urllib.request.urlretrieve(info["version_url"])
                    with open(request[0], "r") as f:
                        version_info = json.load(f)
                        info["version"] = version_info["Cellosaurus"]["header"]["release"]["version"]
                else:
                    raise NotImplementedError()
            except Exception as e:
                raise ValueError(f"Could not retrieve version for {ontology} from {info['version_url']}: {e}") from e
        else:
            raise ValueError(f"Version not specified for ontology {ontology} and no version_url provided")


def list_expired_cellxgene_schema_version(ontology_info: Dict[str, Any]) -> List[str]:
    """
    Lists cellxgene schema version that are deprecated and should be removed from the ontology_info.json file
    :param ontology_info: the ontology information from ontology_info.json
    :return: a list of expired schema versions
    """
    expired_versions = []
    now = datetime.now()
    for schema_version in ontology_info:
        deprecated_on = ontology_info[schema_version].get("deprecated_on")
        if deprecated_on:
            parsed_date = datetime.strptime(deprecated_on, "%Y-%m-%d")
            expiration_date = parsed_date + timedelta(days=6 * 30)  # 6 months
            if expiration_date < now:
                expired_versions.append(schema_version)
    return expired_versions


# Download and parse ontology files upon execution
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--diff",
        action="store_true",
        help="If set to true, only download and parse ontologies that have changed since the last run.",
    )
    args = parser.parse_args()

    ontology_info = get_ontology_info_file()
    current_version = get_latest_schema_version(ontology_info.keys())
    resolve_version(ontology_info[current_version])
    latest_ontology_version = ontology_info[current_version]
    ontologies_to_process = latest_ontology_version["ontologies"]

    # only process ontologies that have changed since the last run
    if args.diff:
        previous_ontology_info = get_ontology_info_file(env.LATEST_ONTOLOGY_INFO_FILE)
        previous_ontologies = previous_ontology_info["ontologies"]
        diff_ontologies = {
            ontology: info
            for ontology, info in ontologies_to_process.items()
            if previous_ontologies.get(ontology) != info
        }
        ontologies_to_process = diff_ontologies
        logging.info(
            "Processing the following ontologies that have changed since the last run:\n\t",
            "\t\n".join(diff_ontologies.keys()),
        )

    # download and parse ontologies and generate ontology assets
    _download_ontologies(ontologies_to_process)
    _parse_ontologies(ontologies_to_process)
    deprecate_previous_cellxgene_schema_versions(ontology_info, current_version)
    expired_files = update_ontology_info(ontology_info)
    logging.info("Removing expired files:\n\t", "\t\n".join(expired_files))
    for file in expired_files:
        os.remove(os.path.join(env.ONTOLOGY_ASSETS_DIR, file))
    save_ontology_info(ontology_info, latest_ontology_version)

    # validate against the schema
    schema_file = os.path.join(env.SCHEMA_DIR, "all_ontology_schema.json")
    registry = register_schemas()
    result = [
        verify_json(schema_file, output_file, registry) for output_file in _parse_ontologies(ontologies_to_process)
    ]
    if not all(result):
        sys.exit(1)
