import gzip
import json
import os
import re
import urllib.request
from threading import Thread
from typing import Any, Dict, List, Optional, Set
from urllib.error import HTTPError, URLError

import env
import owlready2
import semantic_version


def _get_latest_version(versions: List[str]) -> str:
    return "v" + str(sorted([semantic_version.Version.coerce(version[1:]) for version in versions])[-1])


def _get_ontology_info_file(
    ontology_info_file: str = env.ONTOLOGY_INFO_FILE, cellxgene_schema_version: Optional[str] = None
) -> Any:
    """
    Read ontology information from file

    :param str ontology_info_file: path to file with ontology information

    :rtype Any
    :return ontology information
    """
    with open(ontology_info_file, "r") as f:
        ontology_info = json.load(f)
        if cellxgene_schema_version:
            ontology_info_version = ontology_info[cellxgene_schema_version]
        else:
            ontology_info_version = ontology_info[_get_latest_version(ontology_info.keys())]
        return ontology_info_version


def _download_ontologies(ontology_info: Dict[str, Any], output_dir: str = env.RAW_ONTOLOGY_DIR) -> None:
    """
    Downloads the ontology files specified in 'ontology_info.json' into 'output_dir'

    :param str ontology_info: a dictionary with ontology names as keys and their respective URLs and versions
    :param str output_dir: path to writable directory where ontology files will be downloaded to

    :rtype None
    """

    def download(_ontology: str, _url: str) -> None:
        print(f"Start Downloading {_ontology}")
        # Format of ontology (handles cases where they are compressed)
        download_format = _url.split(".")[-1]

        output_file = os.path.join(output_dir, _ontology + ".owl")
        if download_format == "gz":
            urllib.request.urlretrieve(_url, output_file + ".gz")
            _decompress(output_file + ".gz", output_file)
            os.remove(output_file + ".gz")
        else:
            urllib.request.urlretrieve(_url, output_file)
        print(f"Finish Downloading {_ontology}")

    def _build_url(_ontology: str) -> str:
        onto_ref_data = ontology_info[_ontology]
        return f"{onto_ref_data['source']}/{onto_ref_data['version']}/{ontology.lower()}.{onto_ref_data['filetype']}"

    threads = []
    for ontology, _ in ontology_info.items():
        url = _build_url(ontology)
        try:
            urllib.request.urlopen(url)
        except HTTPError as e:
            raise Exception(f"{ontology} with pinned URL {url} returns status code {e.code}") from e
        except URLError as e:
            raise Exception(f"{ontology} with pinned URL {url} fails due to {e.reason}") from e

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


def _get_ancestors(onto_class: owlready2.entity.ThingClass, onto_name: str) -> Set[str]:
    """
    Returns a list of ancestors ids of the given onto class, only returns those belonging to ontology_name,
    it will format the id from the form CL_xxxx to CL:xxxx

    :param owlready2.entity.ThingClass onto_class: the class for which ancestors will be retrieved
    :param str onto_name: only ancestors from this ontology will be kept

    :rtype List[str]
    :return list of ancestors (term ids), it could be empty
    """

    def _get_branch_ancestors(term: owlready2.entity.ThingClass) -> Set[str]:
        # a branch ancestor is defined in ontology files as having a "part_of" (BFO_0000050) relationship with a term
        branch_ancestors = set()
        for subclass in term.is_a:
            if (
                hasattr(subclass, "property")
                and subclass.property.name == "BFO_0000050"
                and isinstance(subclass.value, owlready2.entity.ThingClass)
            ):
                branch_ancestor_name = subclass.value.name.replace("obo.", "").replace("_", ":")
                if branch_ancestor_name.split(":")[0] == onto_name:
                    branch_ancestors.add(branch_ancestor_name)
                    branch_ancestors.update(_get_ancestors(subclass.value, onto_name))
        return branch_ancestors

    ancestors = set()
    for ancestor in onto_class.ancestors():
        if ancestor.name.split("_")[0] == onto_name:
            ancestors.add(ancestor.name.replace("_", ":"))
            if onto_name != "NCBITaxon":
                ancestors.update(_get_branch_ancestors(ancestor))

    # remove self
    ancestors.remove(onto_class.name.replace("_", ":"))
    return ancestors


def _extract_ontology_term_metadata(onto: owlready2.entity.ThingClass) -> Dict[str, Any]:
    """
    Extract relevant metadata from ontology object and save into a dictionary following our JSON Schema

    :param: onto: Ontology Object to Process
    :return: Dict[str, Any] map of ontology term IDs to pertinent metadata from ontology files
    """
    term_dict: Dict[str, Any] = dict()
    for onto_term in onto.classes():
        term_id = onto_term.name.replace("_", ":")

        # Skip terms that are not direct children from this ontology
        if onto.name != term_id.split(":")[0]:
            continue
        # Gets ancestors
        ancestors = _get_ancestors(onto_term, onto.name)

        # Special Case: skip the current term if it is an NCBI Term, but not a descendant of 'NCBITaxon:33208'.
        if onto.name == "NCBITaxon" and "NCBITaxon:33208" not in ancestors:
            continue

        term_dict[term_id] = dict()

        # only write the ancestors if it's not NCBITaxon, as this saves a lot of disk space and there is
        # no current use-case for NCBITaxon
        term_dict[term_id]["ancestors"] = [] if onto.name == "NCBITaxon" else list(ancestors)

        # Gets label
        term_dict[term_id]["label"] = onto_term.label[0] if onto_term.label else ""

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
                term_dict[term_id]["replaced_by"] = f"{ontology_term[-2]}:{ontology_term[-1]}"
            elif getattr(onto_term, "consider", None):
                term_dict[term_id]["consider"] = [str(c) for c in onto_term.consider]
    return term_dict


def _parse_ontologies(
    ontology_info: Any,
    working_dir: str = env.RAW_ONTOLOGY_DIR,
    output_path: str = env.ONTOLOGY_ASSETS_DIR,
) -> None:
    """
    Parse all ontology files in working_dir. Extracts information from all classes in the ontology file.
    The extracted information is written into a gzipped a json file with the following [schema](
    artifact-schemas/all_ontology_schema.json):
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
    ./artifact-schemas/ontology_info_schema.json)
    :param str working_dir: path to folder with ontology files
    :param str output_path: path to output json files

    :rtype None
    """
    for onto_file in os.listdir(working_dir):
        if onto_file.startswith("."):
            continue
        onto = _load_ontology_object(os.path.join(working_dir, onto_file))
        version = ontology_info[onto.name]["version"]
        output_file = f"{onto.name}-ontology-{version}.json.gz"
        print(f"Processing {output_file}")

        onto_dict = _extract_ontology_term_metadata(onto)

        with gzip.open(os.path.join(output_path, output_file), "wt") as output_json:
            json.dump(onto_dict, output_json, indent=2)


# Download and parse ontology files upon execution
if __name__ == "__main__":
    ontology_info = _get_ontology_info_file()
    _download_ontologies(ontology_info)
    _parse_ontologies(ontology_info)
    # comment
