"""Preprocessing/parsing the subtitles in xml format"""

import os
import xml.etree.ElementTree as ET
import string
from typing import List, Tuple
from datetime import datetime

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


# class Subtitles:


def get_subtitles(movie_filename: str) -> List[Tuple[str, str]]:
    path = os.path.join(PAR_DIR, DATA_DIR, movie_filename)
    tree = ET.parse(path)
    root = tree.getroot()

    subdialogue = []
    time = "00:00:00,000"
    for sentence in root:
        dialogue = ""
        for child in sentence:

            if child.tag == "time" and str(child.get("id")).endswith("S"):
                time = child.get("value")

            elif child.tag == "time" and str(child.get("id")).endswith("E"):
                continue
            else:
                word = str(child.text)
                if word.endswith("'"):
                    dialogue += word
                else:
                    if word not in string.punctuation:
                        dialogue = dialogue + word + " "

        sent_tuple = (time, dialogue.strip())
        subdialogue.append(sent_tuple)

        print(time, dialogue.strip())
    return subdialogue


def main():
    get_subtitles("star-wars-4_sub.xml")


if __name__ == '__main__':
    main()
