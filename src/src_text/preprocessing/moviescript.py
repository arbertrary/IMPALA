"""
The main moviescript module
Contains functions that return everything that needs to be extracted from fully annotated XML moviescript
"""

import os
import functools
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Set, Tuple, Dict

from annotate import annotate
from parse_fountain import moviescript_to_xml

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


# PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
# DATA_DIR = "testfiles"


def parse(fountain_path: str, subs_path: str, dest_path: str):
    """Complete parse-pipeline from fountain movie script + xml subtitles to annotated xml movie script"""
    unannotated_xml = moviescript_to_xml(fountain_path, dest_path)

    annotate(unannotated_xml, subs_path, dest_path)


def main():
    path = os.path.join(BASE_DIR, "src/testfiles/")
    # fountain = os.path.join(path, "star-wars-4.txt")
    # subs_path = os.path.join(path, "star-wars-4_sub.xml")
    dest_path = os.path.join(path, "star-wars-4_annotated.xml")

    # fountain = os.path.join(path, "hellraiser.txt")
    # subs_path = os.path.join(path, "hellraiser_sub.xml")
    dest_path = os.path.join(path, "hellraiser_annotated.xml")

    # parse(fountain, subs_path, dest_path)
    scenes = get_full_scenes(dest_path)
    # test = get_char_dialogue(dest_path)
    # print(test.get("THREEPIO"))

    for index, scene in enumerate(scenes):
        print("scene: ", index, " time: ", scene[0])


def get_full_scenes(xml_path: str) -> List[Tuple[str, str, List[str]]]:
    """:returns List of all scenes. (List consisting of time code and a list of all sentences in that scene)"""
    tree = ET.parse(xml_path)
    scenes = []
    for scene in tree.findall("scene"):
        sentences = []
        # time = scene.get("time_avg") or scene.get("time_interpolated")
        time = scene.get("start")
        end = scene.get("end")

        # if time:
        if time and end:
            for child in scene:
                for sent in child:
                    sentences.append(sent.text)
        else:
            continue

        # scenes.append((time, sentences))
        scenes.append((time, end, sentences))
    return scenes


def get_all_sentences(xml_path: str):
    """:returns all individual sentences with either the actual time code or the time code of their scene"""
    tree = ET.parse(xml_path)

    sentences = []

    for scene in tree.findall("scene"):
        time = scene.get("time_avg") or scene.get("time_interpolated")

        for child in scene:
            for sent in child:
                if sent.get("time"):
                    sentences.append((sent.get("time"), sent.text))
                else:
                    sentences.append((time, sent.text))

    return sentences


def get_characters(xml_path: str) -> Set[str]:
    """:returns the movie characters"""
    tree = ET.parse(xml_path)

    characters = set(char.get("name") for char in tree.iter("dialogue"))

    return characters


def get_char_dialogue(xml_path: str) -> Dict[str, List[str]]:
    """:returns Dict of character names and a list of all their sentences"""
    tree = ET.parse(xml_path)

    dialogue = {}
    for d in tree.iter("dialogue"):
        dialogue_list = []
        for child in d:
            dialogue_list.append(child.text)

        if dialogue.get(d.get("name")):
            dialogue[d.get("name")] += dialogue_list
        else:
            dialogue[d.get("name")] = dialogue_list

    return dialogue


def get_metatext(xml_path) -> List[str]:
    """Get only the meta text from the moviescript, together with a reference to the scene?"""
    tree = ET.parse(xml_path)

    meta_tuples = []
    for scene in tree.findall("scene"):
        meta_tuples += [(m.get("id"), m.text) for m in scene.findall("meta")]

    return meta_tuples


if __name__ == '__main__':
    main()
