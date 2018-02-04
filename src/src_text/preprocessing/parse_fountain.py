"""Parsing moviescript from plain text/fountain format to xml """

import os
import re
import xml.etree.cElementTree as ET
from typing import List, Tuple
from nltk import sent_tokenize, word_tokenize
from xml.dom import minidom

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def moviescript_to_xml(movie_path: str, dest: str):
    """Parses movie scripts in fountain plain text format to xml"""
    root = ET.Element("movie")
    scenelist = __get_scene_tuples(movie_path)

    char_pattern = re.compile(r"\b[^a-z!?<>]*[^a-z!.?<>]+(\(.+\))*$")

    # remove the movie info (at end of file) and put it into own xml tree element
    temp = scenelist[-1]
    text = temp[1].split('\n\n')
    movieinfo = re.sub(r"\xa0|User Comments", " ", text[-1]).strip()
    scene_text = re.sub(text[-1], "", temp[1])
    scenelist[-1] = (temp[0], scene_text)
    minfo = ET.SubElement(root, "info")

    info = movieinfo.splitlines()
    title = info[0].strip()
    ET.SubElement(minfo, "title").text = title
    writers = info[1].split(":")[-1].strip()
    ET.SubElement(minfo, "writers").text = writers
    genres = info[2].split(":")[-1].strip()
    genres = word_tokenize(genres)
    genres = ','.join(genres)
    ET.SubElement(minfo, "genres").text = genres

    # Go through every scene and parse
    for index, scene in enumerate(scenelist):
        scene_id = "sc" + str(index)

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

    tree = __sent_tokenize_moviescript(tree)

    xmlstr = minidom.parseString(ET.tostring(tree.getroot())).toprettyxml(indent="   ")

    with open(dest, "w", encoding="UTF-8") as f:
        f.write(xmlstr)

    return dest


def __get_scene_tuples(movie_path: str) -> List[Tuple[str, str]]:
    """Separates movie script into scenes; returns tuples of (scene header, scene text)."""

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


def __sent_tokenize_moviescript(tree: ET.ElementTree) -> ET.ElementTree:
    """Sentence tokenizing of movie script"""

    # sent_tokenize the "intro text"
    beginning = tree.find("beginning")
    text = re.split("\n{2,}", beginning.text)
    text = [re.sub("\n |\s{2,}", " ", paragraph).strip() for paragraph in text]

    count = 1
    for p in text:
        for s in sent_tokenize(p):
            id = "bs" + str(count)
            ET.SubElement(beginning, "s", id=id).text = s
            count += 1
    beginning.text = ""

    # sent_tokenize all meta and dialogue text
    for scene in tree.findall("scene"):
        meta = scene.findall("meta")
        dialogue = scene.findall("dialogue")

        i = 1
        for m in meta:
            for s in sent_tokenize(m.text):
                m_sent_id = m.get("id") + "s" + str(i)
                ET.SubElement(m, "s", id=m_sent_id).text = s
                i += 1
            m.text = ""
            i = 1
        j = 1
        for d in dialogue:
            for s in sent_tokenize(d.text):
                d_sent_id = d.get("id") + "s" + str(j)
                ET.SubElement(d, "s", id=d_sent_id).text = s
                j += 1
            d.text = ""
            j = 1

    return tree


def main():
    """main"""
    # path = os.path.join(PAR_DIR, DATA_DIR, "hellraiser.txt")
    # dest = os.path.join(PAR_DIR, DATA_DIR, "hellraiser.xml")
    path = os.path.join(BASE_DIR, "src/testfiles/", "scream.txt")
    dest = os.path.join(BASE_DIR, "src/testfiles/", "scream.xml")
    # sent_tokenize_moviescript("star-wars-4.xml")
    # get_scene_tuples("testmovie.txt")
    moviescript_to_xml(path, dest)
    # moviescript_to_xml("empty_linesBetweenCharAndDialogue.txt")


if __name__ == '__main__':
    main()
