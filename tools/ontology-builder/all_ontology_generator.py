import env
import gzip
import json
import os
import re
import urllib.request
from threading import Thread
from typing import List
from urllib.error import HTTPError, URLError

import owlready2
import yaml


def _download_ontologies(onto_info_yml: str = env.ONTO_INFO_YAML, output_dir: str = env.RAW_ONTOLOGY_DIR):
    """
    Downloads the ontology files specified in 'ontology_info.yml' into 'output_dir'

    :param str onto_info_yml: path to yaml file with ontology information
    :param str output_dir: path to writable directory where ontology files will be downloaded to

    :rtype None
    """
    with open(onto_info_yml, "r") as onto_info_handle:
        ontology_info = yaml.safe_load(onto_info_handle)

    def download(_ontology, _url):
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

    def _build_url(_ontology: str):
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


def _decompress(infile: str, tofile: str):
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
    :return: 
    """
    world = owlready2.World()
    onto = world.get_ontology(onto_file)
    onto.load()
    return onto


def _get_ancestors(onto_class: owlready2.entity.ThingClass, onto_name: str) -> List[str]:
    """
    Returns a list of ancestors ids of the given onto class, only returns those belonging to ontology_name,
    it will format the id from the form CL_xxxx to CL:xxxx

    :param owlready2.entity.ThingClass onto_class: the class for which ancestors will be retrieved
    :param str onto_name: only ancestors from this ontology will be kept

    :rtype List[str]
    :return list of ancestors (term ids), it could be empty
    """

    ancestors = []

    for ancestor in onto_class.ancestors():
        if onto_class.name == ancestor.name:
            continue
        if ancestor.name.split("_")[0] == onto_name:
            ancestors.append(ancestor.name.replace("_", ":"))

    return ancestors


def _extract_ontology_term_metadata(onto: owlready2.entity.ThingClass) -> dict:
    """
    Extract relevant metadata from ontology object and save into a dictionary following our JSON Schema

    :param: onto: Ontology Object to Process
    :return: Dict[str, str] map of ontology term IDs to pertinent metadata from ontology files
    """
    term_dict = dict()
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
        term_dict[term_id]["ancestors"] = [] if onto.name == "NCBITaxon" else ancestors

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
            if hasattr(onto_term, "IAO_0000233") and onto_term.IAO_0000233:
                term_dict[term_id]["term_tracker"] = str(onto_term.IAO_0000233[0])

            # only need to record replaced_by OR considers
            if onto_term.IAO_0100001 and onto_term.IAO_0100001.first():
                # url --> term
                ontology_term = re.findall(r"[^\W_]+", str(onto_term.IAO_0100001[0]))
                term_dict[term_id]["replaced_by"] = f"{ontology_term[-2]}:{ontology_term[-1]}"
            else:
                if hasattr(onto_term, "consider") and onto_term.consider:
                    term_dict[term_id]["consider"] = [str(c) for c in onto_term.consider]
    return term_dict


def _parse_ontologies(
    working_dir: str = env.RAW_ONTOLOGY_DIR,
    output_json_file: str = env.PARSED_ONTOLOGIES_FILE,
):
    """
    Parse all ontology files in working_dir. Extracts information from all classes in the ontology file.
    The extracted information is written into a gzipped a json file with the following structure:
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

    :param str working_dir: path to folder with ontology files
    :param str output_json_file: path to output json file

    :rtype None
    """
    onto_dict = dict()
    for onto_file in os.listdir(working_dir):
        onto = _load_ontology_object(os.path.join(working_dir, onto_file))
        print(f"Processing {onto.name}")
        onto_dict[onto.name] = _extract_ontology_term_metadata(onto)

    with gzip.open(output_json_file, "wt") as output_json:
        json.dump(onto_dict, output_json, indent=2)


# Download and parse ontology files upon execution
if __name__ == "__main__":
    _download_ontologies()
    _parse_ontologies()
