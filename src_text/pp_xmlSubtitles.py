"""Preprocessing/parsing the subtitles in xml format"""

import os
import xml.etree.ElementTree as ET
import string
from datetime import datetime

CUR_DIR = os.path.dirname(__file__)
PAR_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
DATA_DIR = "testfiles"


def main():
    path = os.path.join(PAR_DIR, DATA_DIR, "star-wars-4.xml")
    tree = ET.parse(path)
    root = tree.getroot()

    for sentence in root:
        # print(child.tag, child.attrib)
        dialogue = ""
        for child in sentence:

            if child.tag == "time" and str(child.get("id")).endswith("S"):
                # print(c.attrib)
                print(child.get("id"))
                print(child.get("value"))

            elif child.tag == "time" and str(child.get("id")).endswith("E"):
                continue
            else:
                word = str(child.text)
                if word.endswith("'"):
                    dialogue += word
                else:
                    if word not in string.punctuation:
                        dialogue = dialogue + word + " "
        print(dialogue.strip())


if __name__ == '__main__':
    main()
