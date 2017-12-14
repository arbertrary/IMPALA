"""Parsing moviescript from plain text/fountain format to xml """

import os
import re
import xml.etree.cElementTree as ET
from typing import List, Tuple
from nltk import sent_tokenize
from xml.dom import minidom

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"
DATA_DIR2 = "moviescripts_to_test"


def get_scene_tuples(movie_path: str) -> List[Tuple[str, str]]:
    """Separates movie script into scenes; returns tuples of (scene header, scene text)."""
    # textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    # textdata_dir = os.path.join(PAR_DIR, DATA_DIR2)

    # movie_path = os.path.join(textdata_dir, movie_filename)

    with open(movie_path, 'r', encoding='utf-8') as movie:
        text = movie.read()

        text = re.sub(
            r"FADE IN[.:]?|FADE TO[.:]?|CUT TO[.:]?|DISSOLVE TO[.:]?|FADE OUT[.:]?|FADE TO BLACK[.:]?\(?CONTINUED\)?",
            "", text)
        text = text.strip()

        text = re.split(
            r"\b((?:INT[.: ]?\b|EXT[.: ]?\b|INTERIOR[.: ]?\b|EXTERIOR[.: ]?\“)[^\n]+\n)",
            text)
        scenelist = [("MOVIEBEGINNING", text[0])]

        i = 1
        while i < len(text):
            scenetuple = (text[i], text[i + 1])
            scenelist.append(scenetuple)

            i += 2
    return scenelist


def moviescript_to_xml(movie_path: str):
    """Parses movie scripts in fountain plain text format to xml"""
    root = ET.Element("movie")
    scenelist = get_scene_tuples(movie_path)

    # char_pattern = re.compile(r"([ |\t]*\b[^(\-\d][^<>a-z\s\n][^<>a-z:!?\n]*[^<>a-z!?:.\n][ |\t]?\n)(?!\n)")
    # char_pattern = re.compile(r"[\s]*\b[^a-z!?<>]+[^a-z!.?<>]$")  # (?!\n)
    #
    # char_pattern = re.compile(r"\b[^a-z!?<>]*[^a-z!.?<>]+$")  # (?!\n)
    char_pattern = re.compile(r"\b[^a-z!?<>]*[^a-z!.?<>]+(\(.+\))*$")  # (?!\n)

    # remove the movie info (at end of file) and put it into own xml tree element
    temp = scenelist[-1]
    text = temp[1].split('\n\n')
    movieinfo = re.sub(r"\xa0|User Comments", " ", text[-1]).strip()
    scene_text = re.sub(text[-1], "", temp[1])
    scenelist[-1] = (temp[0], scene_text)
    ET.SubElement(root, "info").text = movieinfo

    for index, scene in enumerate(scenelist):
        scene_id = "s" + str(index)

        # From start to first scene = Beginning
        if scene[0] == "MOVIEBEGINNING":
            ET.SubElement(root, "beginning").text = scene[1]
            continue
        else:
            sc = ET.SubElement(root, "scene", id=scene_id)
            ET.SubElement(sc, "sceneheader").text = scene[0].strip()

        lines = scene[1].split(os.linesep)

        i = 1
        m = 1
        d = 1
        metatext = ""
        while i < len(lines):
            meta_id = scene_id + "m" + str(m)
            dialogue_id = scene_id + "d" + str(d)

            if re.fullmatch(char_pattern, lines[i].strip()):
                if metatext.strip():
                    ET.SubElement(sc, "meta", id=meta_id).text = metatext.strip()
                character = lines[i].strip()
                # char = ET.SubElement(sc, "char", name=character)

                dialogue = ""
                d += 1
                metatext = ""
                m += 1

                # Richtig hässlich hardcoded für eine einzelne leerzeile nach Character name
                # TODO: Sinnvoller machen! Oder rauslassen; eig nur nötig falls eine leerzeile nach dem charakter kommt

                try:
                    if not lines[i + 1].strip():
                        i += 1
                except IndexError:
                    pass
                    # print(movie_filename)
                    # print(lines[i])

                while i + 1 < len(lines) and lines[i + 1].strip() and not re.fullmatch(char_pattern,
                                                                                       lines[i + 1].strip()):
                    dialogue = (dialogue + " " + lines[i + 1].strip()).strip()
                    i += 1

                # Falls dialog an dieser stelle leer ist -> das gefundene war kein Charakter sondern eine Zeile in Großbuchstaben
                if dialogue.strip():
                    # char = ET.SubElement(sc, "char", name=character)
                    # ET.SubElement(char, "dialogue", id=dialogue_id).text = dialogue
                    char = ET.SubElement(sc, "dialogue", name=character, id=dialogue_id).text = dialogue
                else:
                    metatext = (metatext + " " + character.strip())
                i += 1

            else:
                metatext = (metatext + " " + lines[i].strip()).strip()
                i += 1

        if metatext.strip() and meta_id:
            ET.SubElement(sc, "meta", id=meta_id).text = metatext.strip()

    tree = ET.ElementTree(root)

    tree = sent_tokenize_moviescript(tree)

    xmlstr = minidom.parseString(ET.tostring(tree.getroot())).toprettyxml(indent="   ")

    with open("testfile.xml", "w", encoding="UTF-8") as f:
        f.write(xmlstr)


def sent_tokenize_moviescript(tree: ET.ElementTree) -> ET.ElementTree:
    """Sentence tokenizing of dialogue and meta text in movie script"""
    for scene in tree.findall("scene"):
        meta = scene.findall("meta")
        dialogue = scene.findall("dialogue")

        i = 1
        for m in meta:
            for s in sent_tokenize(m.text):
                m_sent_id = m.get("id") + "sent" + str(i)
                ET.SubElement(m, "s", id=m_sent_id).text = s
                i += 1
            m.text = ""
            i = 1
        j = 1
        for d in dialogue:
            for s in sent_tokenize(d.text):
                d_sent_id = d.get("id") + "sent" + str(j)
                ET.SubElement(d, "s", id=d_sent_id).text = s
                j += 1
            d.text = ""
            j = 1

    return tree


def main():
    """main"""
    path = os.path.join(PAR_DIR, DATA_DIR, "star-wars-4.txt")

    # sent_tokenize_moviescript("star-wars-4.xml")
    # get_scene_tuples("testmovie.txt")
    moviescript_to_xml(path)
    # moviescript_to_xml("empty_linesBetweenCharAndDialogue.txt")


if __name__ == '__main__':
    main()
