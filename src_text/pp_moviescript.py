"""Preprocessing movie scripts"""

import os
import re
import xml.etree.cElementTree as ET
from typing import List, Tuple
from xml.dom import minidom

CUR_DIR = os.path.dirname(__file__)
PAR_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
DATA_DIR = "testfiles"


def clean_moviescript(movie_filename: str):
    """doesn't do that much atm because other functions do all the stuff now"""
    textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    movie_path = os.path.join(textdata_dir, movie_filename)

    with open(movie_path, 'r', encoding='utf-8') as movie:
        text = movie.readlines()


# TODO: check if scene_tuples actually extracts all scenes
def get_scene_tuples(movie_filename: str) -> List[Tuple[str, str]]:
    """Separates movie script into scenes; returns tuples of (scene header, scene text)."""
    textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    movie_path = os.path.join(textdata_dir, movie_filename)

    with open(movie_path, 'r', encoding='utf-8') as movie:
        text = movie.read()
        text = text.strip()

        text = re.split(
            r"((?:INT[.:]? |EXT[.:]? |INTERIOR[.:]? |EXTERIOR[.:]? )[^\n]+\n)",
            text)
        scenelist = [("MOVIEBEGINNING", text[0])]

        i = 1
        while i < len(text):
            scenetuple = (text[i], text[i + 1])
            scenelist.append(scenetuple)

            i += 2
    return scenelist


# sollte ich dialog als list der lines extrahieren oder als string?
# ich wandle ja eh wieder in strings um fürs tokenizen
# TODO: Beim Extrahieren irgendeine Referenz auf die zugehörige Szene mitnehmen
def extract_moviedialogue(movie_filename: str) -> List[str]:
    """extracts all dialogue from a movie script and ignores meta text"""
    scenelist = get_scene_tuples(movie_filename)

    char_pattern = re.compile(r"([ |\t]*[^-][^<>a-z\s\n][^<>a-z:!\?\n]+[^<>a-z\(!\?:\n][ \t]?)\n{1}(?!\n)")

    dialogue = []
    for scene in scenelist:
        lines = scene[1].split(os.linesep)

        i = 1
        while i < len(lines):
            if lines[i].strip().isupper():
                character = lines[i]
                while i + 1 < len(lines) and lines[i + 1].strip():
                    # ignore meta text below speaker name like (speaks slowly):
                    if re.search(r'[(|)]', lines[i + 1].strip()):
                        metatext = lines[i + 1]
                        i += 1
                    else:
                        dialogue.append(lines[i + 1].strip())  # .lower())
                        i += 1

                i += 1
            else:
                i += 1

    return dialogue


def extract_moviedialogue_2(movie_filename: str) -> List[Tuple[str, str]]:
    """ """
    root = ET.Element("movie")

    scenelist = get_scene_tuples(movie_filename)

    char_pattern = re.compile(r"([ |\t]*[^-][^<>a-z\s\n][^<>a-z:!\?\n]+[^<>a-z\(!\?:\n][ \t]?)\n{1}(?!\n)")
    temp = []

    for index, scene in enumerate(scenelist):
        sc = ET.SubElement(root, "scene")
        ET.SubElement(sc, "sceneheader", id=str(index)).text = scene[0]

        if scene[0] == "MOVIEBEGINNING":
            sc = ET.SubElement(root, "beginning").text = scene[1]
            continue

        lines = scene[1].split(os.linesep)
        i = 1
        metatext = ""
        while i < len(lines):
            if re.match(char_pattern, lines[i] + "\n"):
                dialogue = ""
                temp.append(("meta:", metatext))
                ET.SubElement(sc, "meta").text = metatext

                metatext = ""

                character = lines[i]
                char = ET.SubElement(sc, "char", name=character)

                while i + 1 < len(lines) and lines[i + 1].strip():
                    # ignore meta text below speaker name e.g. (speaks slowly):
                    if re.search(r'[(|)]', lines[i + 1].strip()):
                        metatext = lines[i + 1]
                        i += 1
                    else:
                        dialogue += " " + lines[i + 1].strip()
                        i += 1
                temp.append(("dialogue:", dialogue))
                ET.SubElement(char, "dialogue").text = dialogue

                i += 1

            else:
                metatext += " " + lines[i].strip()
                i += 1

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open("filename.xml", "w") as f:
        f.write(xmlstr)

    return temp


def main():
    """main"""
    # root = ET.Element("movie")
    # scene = ET.SubElement(root, "scene")
    # ET.SubElement(scene, "sceneheader", id="1").text = "e"
    # ET.SubElement(scene, "metatext", name="metatext").text = "This is some metatext"
    # ET.SubElement(scene, "dialogue", name="dialogue").text = "This is some dialogue"
    # xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    # with open("filename.xml", "w") as f:
    #     f.write(xmlstr)

    # extract_moviedialogue_2("Cars-2.txt")
    get_scene_tuples("testmovie.txt")

    # for e in extract_moviedialogue_2("testmovie.txt"):
    #     print(e)


if __name__ == '__main__':
    main()
