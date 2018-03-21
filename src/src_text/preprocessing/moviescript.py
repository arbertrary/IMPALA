"""
The main moviescript module.
Contains functions that return everything that needs to be extracted from fully annotated XML moviescript
"""
import xml.etree.ElementTree as ET
from typing import List, Set, Tuple, Dict


def get_scenes_auto_annotated(xml_path: str) -> List[Tuple[str, List[str]]]:
    """Get scenes (each scene as a List of sentences) of an automatically annotated xml movie script
    only scenes with average or annotated time code
    :param xml_path: path to xml movie script
    :returns List of all scenes. (List consisting of time code and a list of all sentences in that scene)"""
    tree = ET.parse(xml_path)
    scenes = []
    for scene in tree.findall("scene"):
        sentences = []
        time = scene.get("time_avg") or scene.get("time_interpolated")

        if time:
            for child in scene:
                for sent in child:
                    sentences.append(sent.text)
        else:
            continue

        scenes.append((time, sentences))

    if len(scenes) == 0:
        raise Warning("The resulting list is empty! It might be that the movie script does not contain time codes "
                      "or is manually annotated")

    return scenes


def get_scenes_man_annotated(xml_path: str) -> List[Tuple[str, str, List[str], str]]:
    """Get scenes (each scene as a List of sentences) of a manually annotated movie script
    only scenes with start and end time code
    :returns List of all scenes. (List consisting of Tuples of start, end, List of Sentences, scene id)"""
    tree = ET.parse(xml_path)
    scenes = []
    for scene in tree.findall("scene"):
        sentences = []
        time = scene.get("start")
        end = scene.get("end")

        if time and end:
            for child in scene:
                for sent in child:
                    sentences.append(sent.text)
        else:
            continue

        scenes.append((time, end, sentences, scene.get("id")))

    if len(scenes) == 0:
        raise Warning("The resulting list is empty! It might be that the movie script does not contain time codes "
                      "or is automatically annotated.")

    return scenes


def get_scenes(xml_path: str) -> List[List[str]]:
    """simply returns scenes without time code
    :returns List of scenes with each scene being a List of sentences"""
    tree = ET.parse(xml_path)
    scenes = []
    for scene in tree.findall("scene"):
        sentences = []

        for child in scene:
            for sent in child:
                sentences.append(sent.text)

        scenes.append(sentences)
    return scenes


def get_all_sentences(xml_path: str):
    """:returns all individual sentences with either the actual time code or the time code of their scene"""
    tree = ET.parse(xml_path)

    sentences = tree.iter("s")
    text = []
    for s in sentences:
        text.append(s.text)

    return text


def get_characters(xml_path: str) -> Set[str]:
    """:returns the movie characters in a Set"""
    tree = ET.parse(xml_path)

    characters = set(str(char.get("name")).lower() for char in tree.iter("dialogue"))

    return characters


def get_char_dialogue(xml_path: str) -> Dict[str, List[str]]:
    """:returns Dict of character names and a list of all their dialogue sentences"""
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


def get_metatext(xml_path) -> List:
    """Get only the meta text from the movie script"""
    tree = ET.parse(xml_path)

    meta_tuples = []
    for scene in tree.findall("scene"):
        for m in scene.findall("meta"):
            text = []
            for child in m:
                text.append(child.text)
            meta_tuples.append((m.get("id"), text))

    return meta_tuples

if __name__ == '__main__':
    import os

    BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))

    file = os.path.join(BASE_DIR, "data/moviescripts_xml_time/10perc80ratio/the-matrix_annotated.xml")
    print(get_scenes_man_annotated(file))
