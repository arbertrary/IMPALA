"""Reading moviescript from xml format BEFORE annotating with timecodes;
Only used for getting the dialogue"""

import os
import xml.etree.ElementTree as ET
from typing import List, Tuple

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


def get_moviedialogue(movie_path) -> List[Tuple[str, str, str]]:
    """Return List of Triples of (sentence_id, scene_id, sentence)"""

    tree = ET.parse(movie_path)
    dialogue_triples = []

    for scene in tree.findall("scene"):
        scene_id = scene.get("id")

        dialogue = scene.findall("dialogue")

        for d in dialogue:
            dialogue_triples += [(sent.get("id"), scene_id, sent.text) for sent in d.findall("s")]

    return dialogue_triples




def main():

    path = os.path.join(PAR_DIR, DATA_DIR)
    get_moviedialogue(os.path.join(path, "star-wars-4.xml"))


if __name__ == '__main__':
    main()
