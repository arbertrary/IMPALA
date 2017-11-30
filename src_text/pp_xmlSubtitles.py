"""Preprocessing/parsing the subtitles in xml format"""

import os
import xml.etree.ElementTree as ET
import re

CUR_DIR = os.path.dirname(__file__)
PAR_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
DATA_DIR = "testfiles"


def main():
    path = os.path.join(PAR_DIR, DATA_DIR, "star-wars-4.xml")
    tree = ET.parse(path)
    root = tree.getroot()

    for child in root:
        print(child[0].tag)


if __name__ == '__main__':
    main()
