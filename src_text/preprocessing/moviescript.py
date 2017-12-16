"""
The main moviescript module
Contains functions that return everything that needs to be extracted from fully annotated XML moviescript
TODO
"""

import os
import xml.etree.ElementTree as ET
from typing import List, Set
from annotate import annotate
from fountain import moviescript_to_xml

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


def parse(fountain_path: str, subs_path: str, dest_path: str):
    unannotated_xml = moviescript_to_xml(fountain_path, dest_path)

    annotate(unannotated_xml, subs_path, dest_path)


def main():
    path = os.path.join(PAR_DIR, DATA_DIR)
    fountain = os.path.join(path, "star-wars-4.txt")
    subs_path = os.path.join(path, "star-wars-4_sub.xml")
    dest_path = os.path.join(path, "star-wars-4_annotated.xml")

    # fountain = os.path.join(path, "hellraiser.txt")
    # subs_path = os.path.join(path, "hellraiser_sub.xml")
    # dest_path = os.path.join(path, "hellraiser_annotated.xml")

    parse(fountain, subs_path, dest_path)


def get_movieinfo(xml_path: str) -> str:
    tree = ET.parse(xml_path)
    info = tree.find("info").text

    return info


def get_characters(xml_path: str) -> Set[str]:
    """get the movie characters"""
    tree = ET.parse(xml_path)

    characters = set(char.get("name") for char in tree.iter("dialogue"))

    return characters


def get_dialogue(xml_path):
    """Get only the dialogue"""
    tree = ET.parse(xml_path)


def get_metatext(xml_path) -> List[str]:
    """Get only the meta text from the moviescript, together with a reference to the scene?"""
    tree = ET.parse(xml_path)

    meta_tuples = []
    for scene in tree.findall("scene"):
        meta_tuples += [(m.get("id"), m.text) for m in scene.findall("meta")]

    return meta_tuples


def get_genres(xml_path: str) -> List[str]:
    """Gets the genres as list of strings from the allgenres.txt file"""
    genres = []
    with open(os.path.join(PAR_DIR, "allgenres.txt"), "r") as allgenres:
        movies = allgenres.read().splitlines()
        name, ext = os.path.splitext(os.path.basename(xml_path))
        for m in movies:
            if name in m:
                genres = m.split(":")[1].split(",")

        if len(genres) == 0:
            raise ValueError("Movie not found in allgenres.txt")

    return genres


if __name__ == '__main__':
    main()
