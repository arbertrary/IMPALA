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
            r"\b((?:INT[.:]? |EXT[.:]? |INTERIOR[.:]? |EXTERIOR[.:]? )[^\n]+\n)",
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


def parse_moviescript(movie_filename: str):
    """ """
    root = ET.Element("movie")
    scenelist = get_scene_tuples(movie_filename)

    char_pattern = re.compile(r"([ |\t]*\b[^(-][^<>(a-z\s\n][^<>a-z:!?\n]+[^<>a-z(!?:\n][ \t]?\n{1})(?!\n)")

    for index, scene in enumerate(scenelist):
        scene_id = "s" + str(index)
        sc = ET.SubElement(root, "scene", id=scene_id)
        ET.SubElement(sc, "sceneheader").text = scene[0].strip()

        # From start to first scene = Beginning
        if scene[0] == "MOVIEBEGINNING":
            # ET.SubElement(root, "beginning").text = scene[1]
            continue
        # remove the movie info (at end of file) and put it into own xml tree element
        if index == len(scenelist) - 1:
            text = scene[1].split('\n\n')
            movieinfo = re.sub(r"\xa0|User Comments", "", text[-1]).strip()
            scene_text = re.sub(text[-1], "", scene[1])
            scene = (scene[0], scene_text)

        lines = scene[1].split(os.linesep)

        i = 1
        m = 1
        d = 1
        metatext = ""
        while i < len(lines):
            meta_id = scene_id + "m" + str(m)
            dialogue_id = scene_id + "d" + str(d)

            if re.fullmatch(char_pattern, lines[i] + "\n"):
                if metatext.strip():
                    ET.SubElement(sc, "meta", id=meta_id).text = metatext.strip()
                character = lines[i].strip()
                char = ET.SubElement(sc, "char", name=character)

                dialogue = ""
                d += 1
                metatext = ""
                m += 1

                # Richtig hässlich hardcoded für eine einzelne leerzeile nach Character name
                # TODO: Sinnvoller machen!
                if not lines[i + 1].strip():
                    i += 1

                while i + 1 < len(lines) and lines[i + 1].strip() and not re.fullmatch(char_pattern,
                                                                                       lines[i + 1] + "\n"):
                    dialogue = (dialogue + " " + lines[i + 1].strip()).strip()
                    i += 1

                ET.SubElement(char, "dialogue", id=dialogue_id).text = dialogue
                i += 1

            else:
                metatext = (metatext + " " + lines[i].strip()).strip()
                i += 1

        if metatext.strip():
            ET.SubElement(sc, "meta", id=meta_id).text = metatext.strip()

    ET.SubElement(root, "info").text = movieinfo
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open("filename.xml", "w") as f:
        f.write(xmlstr)


def main():
    """main"""

    # get_scene_tuples("testmovie.txt")

    parse_moviescript("testmovie.txt")
    #   parse_moviescript("American-Psycho.txt")


if __name__ == '__main__':
    main()
