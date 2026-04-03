import gzip
import json
import logging
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
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


def save_ontology_info(ontology_info: Dict[str, Any], ontology_info_file: str = env.ONTOLOGY_INFO_FILE) -> None:
    """
    Save ontology information to file

    :param Dict[str, Any] ontology_info: ontology information to save
    :param str ontology_info_file: path to file to save ontology information

    :rtype None
    """
    with open(ontology_info_file, "w") as f:
        json.dump(ontology_info, f, indent=2)


def _download_ontologies(ontology_info: Dict[str, Any], output_dir: str = env.RAW_ONTOLOGY_DIR) -> None:
    """
    Downloads the ontology files specified in 'ontology_info.json' into 'output_dir'

    :param str ontology_info: a dictionary with ontology names as keys and their respective URLs and versions
    :param str output_dir: path to writable directory where ontology files will be downloaded to

    :rtype None
    """

    def download(_ontology: str, _url: str, _fmt: str) -> None:
        logging.info(f"Start Downloading {_url}")
        if _fmt == "xml.gz":
            # Keep the file compressed; it will be parsed by a format-specific streaming parser.
            # Do NOT decompress: these files can be multiple GB when uncompressed and
            # would exceed GitHub Actions runner memory and disk limits.
            output_file = os.path.join(output_dir, _ontology + ".xml.gz")
            urllib.request.urlretrieve(_url, output_file)
        elif _fmt == "owl.gz":
            output_file = os.path.join(output_dir, _ontology + ".owl")
            urllib.request.urlretrieve(_url, output_file + ".gz")
            _decompress(output_file + ".gz", output_file)
            os.remove(output_file + ".gz")
        elif _fmt == "obo":
            # owlready2 auto-detects OBO format from the .obo extension, so the file
            # must be saved with that extension rather than renamed to .owl.
            output_file = os.path.join(output_dir, _ontology + ".obo")
            urllib.request.urlretrieve(_url, output_file)
        elif _fmt == "sssom.tsv":
            # Save using the filename declared in cross_ontology_mapping so that
            # _load_cross_ontology_map can locate the file by the same JSON-defined name.
            cross_filename = ontology_info[_ontology]["cross_ontology_mapping"]["filename"]
            output_file = os.path.join(output_dir, cross_filename)
            urllib.request.urlretrieve(_url, output_file)
        elif _fmt == "tsv":
            output_file = os.path.join(output_dir, _ontology + ".tsv")
            urllib.request.urlretrieve(_url, output_file)
        else:  # "owl"
            output_file = os.path.join(output_dir, _ontology + ".owl")
            urllib.request.urlretrieve(_url, output_file)
        logging.info(f"Finish Downloading {_url}")

    def _build_urls(_ontology: str) -> List[tuple[str, str]]:
        onto_ref_data = ontology_info[_ontology]
        onto_format = onto_ref_data.get("format", "owl")
        # Use direct URL when provided (e.g. for ontologies whose distribution does not
        # follow the standard {source}/{version}/{filename} versioned-path convention).
        if onto_ref_data.get("url"):
            main_url = onto_ref_data["url"]
        else:
            base_url = f"{onto_ref_data['source']}/{onto_ref_data['version']}"
            main_url = f"{base_url}/{onto_ref_data['filename']}"
        download_items = [(main_url, onto_format)]
        if onto_ref_data.get("cross_ontology_mapping"):
            base_url = f"{onto_ref_data['source']}/{onto_ref_data['version']}"
            cross_mapping = onto_ref_data["cross_ontology_mapping"]
            cross_url = f"{base_url}/{cross_mapping['filename']}"
            download_items.append((cross_url, cross_mapping["format"]))
        return download_items

    def _check_url(_ontology: str, _url: str) -> None:
        try:
            urllib.request.urlopen(_url)
        except HTTPError as e:
            raise Exception(f"{_ontology} with pinned URL {_url} returns status code {e.code}") from e
        except URLError as e:
            raise Exception(f"{_ontology} with pinned URL {_url} fails due to {e.reason}") from e

    threads = []
    for ontology, _ in ontology_info.items():
        for url, fmt in _build_urls(ontology):
            _check_url(ontology, url)
            t = Thread(target=download, args=(ontology, url, fmt))
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
        cross_filename = ontology_info[cross_ontology]["cross_ontology_mapping"]["filename"]
        try:
            with open(os.path.join(working_dir, cross_filename), "r") as f:
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
) -> Dict[str, Any]:
    """
    Extract relevant metadata from ontology object and save into a dictionary following our JSON Schema

    :param: onto: Ontology Object to Process
    :param: allowed_ontologies: List of term prefixes to filter out terms that are not direct children from this ontology
    :param: map_to_cross_ontologies: List of ontologies to map equivalent terms to
    :param: cross_ontology_map: str for each ontology with a mapping, map to known equivalent terms in other ontologies
    :return: Dict[str, Any] map of ontology term IDs to pertinent metadata from ontology files
    """
    term_dict: Dict[str, Any] = dict()
    for onto_term in onto.classes():
        term_id = onto_term.name.replace("_", ":")

        # Skip terms that are not direct children from this ontology
        term_id_parts = term_id.split(":")
        if len(term_id_parts) > 2 or term_id_parts[0] not in allowed_ontologies:
            continue
        # Gets ancestors
        ancestors = _get_ancestors(onto_term, allowed_ontologies)

        # Special Case: skip the current term if it is an NCBI Term, but not a descendant of 'NCBITaxon:33208'.
        if onto.name == "NCBITaxon" and "NCBITaxon:33208" not in ancestors:
            continue

        term_dict[term_id] = dict()

        # only write the ancestors if it's not NCBITaxon, as this saves a lot of disk space and there is
        # no current use-case for NCBITaxon
        term_dict[term_id]["ancestors"] = {} if onto.name == "NCBITaxon" else ancestors

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


# UniProt XML namespace used in uniprot_sprot.xml.gz entries.
_UNIPROT_NS = "http://uniprot.org/uniprot"


def _parse_uniprot_xml(xml_gz_path: str) -> Dict[str, Any]:
    """
    Parse a gzip-compressed UniProt XML file (e.g. uniprot_sprot.xml.gz) using streaming
    to extract a term_id → metadata mapping compatible with all_ontology_schema.json.

    NOTE: UniProt is a special case. Unlike OBO/OWL ontologies, UniProt does not expose a
    parseable is_a hierarchy through this pipeline. The ``ancestors`` field is intentionally
    stored as an empty dict for every term. Hierarchy support (e.g. via Gene Ontology
    molecular-function annotations embedded in UniProt entries) would require a separate
    implementation pass and is not yet supported by cellxgene-ontology-guide.

    Term IDs use the lowercase ``uniprot:`` prefix (e.g. ``uniprot:P08575``) as required
    by the CXG schema. Labels are UniProt entry names (e.g. ``IL4_HUMAN``).

    :param str xml_gz_path: path to a gzip-compressed UniProt XML file
    :return Dict[str, Any]: mapping of ``uniprot:<accession>`` → {label, deprecated, ancestors}
    """
    term_dict: Dict[str, Any] = {}
    with gzip.open(xml_gz_path, "rb") as f:
        for _event, elem in ET.iterparse(f, events=("end",)):
            if elem.tag != f"{{{_UNIPROT_NS}}}entry":
                continue
            accessions = elem.findall(f"{{{_UNIPROT_NS}}}accession")
            name_elem = elem.find(f"{{{_UNIPROT_NS}}}name")
            if accessions and name_elem is not None:
                primary_accession = accessions[0].text
                entry_name = name_elem.text  # e.g. "IL4_HUMAN"
                term_dict[f"uniprot:{primary_accession}"] = {
                    "label": entry_name,
                    "deprecated": False,
                    "ancestors": {},
                }
            # Free the element immediately to avoid accumulating the entire tree in memory.
            elem.clear()
    return term_dict


def _parse_ontologies(
    ontology_info: Any,
    working_dir: str = env.RAW_ONTOLOGY_DIR,
    output_path: str = env.ONTOLOGY_ASSETS_DIR,
) -> Iterator[str]:
    """
    Parse all ontology files listed in ontology_info. Dispatches to a format-specific
    parser based on each entry's ``format`` field. Extracts term metadata and writes a
    gzipped JSON file per ontology following the schema at
    asset-schemas/all_ontology_schema.json.

    :param ANY ontology_info: the ontology references used to download the ontology files.
        Follows the schema at asset-schemas/ontology_info_schema.json.
    :param str working_dir: path to folder containing the downloaded ontology files
    :param str output_path: path to write output json.gz files

    :rtype Iterator[str]
    :return: paths to the output json.gz files, yielded one at a time
    """
    cross_ontology_map = _load_cross_ontology_map(working_dir, ontology_info)
    for onto_name, onto_info in ontology_info.items():
        onto_format = onto_info.get("format", "owl")
        version = onto_info["version"]
        output_file = os.path.join(output_path, get_ontology_file_name(onto_name, version))
        logging.info(f"Processing {output_file}")

        if onto_format == "xml.gz":
            onto_dict = _parse_uniprot_xml(os.path.join(working_dir, f"{onto_name}.xml.gz"))
        else:
            # owl, owl.gz (already decompressed to .owl by download), obo — all loaded by owlready2
            onto = _load_ontology_object(os.path.join(working_dir, f"{onto_name}.owl"))
            allowed_ontologies = [onto_name] + onto_info.get("additional_ontologies", [])
            map_to_cross_ontologies = onto_info.get("map_to", [])

            # Special case: NCBITaxon ancestor storage is skipped to save disk space;
            # see _extract_ontology_term_metadata for details.
            onto_dict = _extract_ontology_term_metadata(
                onto, allowed_ontologies, map_to_cross_ontologies, cross_ontology_map
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
    ontology_info = get_ontology_info_file()
    current_version = get_latest_schema_version(ontology_info.keys())
    latest_ontology_version = ontology_info[current_version]
    latest_ontologies = latest_ontology_version["ontologies"]
    _download_ontologies(latest_ontologies)
    _parse_ontologies(latest_ontologies)
    deprecate_previous_cellxgene_schema_versions(ontology_info, current_version)
    expired_files = update_ontology_info(ontology_info)
    logging.info("Removing expired files:\n\t", "\t\n".join(expired_files))
    for file in expired_files:
        os.remove(os.path.join(env.ONTOLOGY_ASSETS_DIR, file))
    save_ontology_info(ontology_info)
    # validate against the schema
    schema_file = os.path.join(env.SCHEMA_DIR, "all_ontology_schema.json")
    registry = register_schemas()
    result = [verify_json(schema_file, output_file, registry) for output_file in _parse_ontologies(latest_ontologies)]
    if not all(result):
        sys.exit(1)
