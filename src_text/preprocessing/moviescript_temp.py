"""Reading moviescript from xml format BEFORE annotating with timecodes"""

import os
import xml.etree.ElementTree as ET
from typing import List, Tuple, Set
from nltk import sent_tokenize

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


# class MovieScript:
#     def __init__(self, movie_filename):
#         self.genres = get_genres(movie_filename)
#         self.characters = get_characters(movie_filename)
#         self.dialogue = get_moviedialogue(movie_filename)
#         self.metatext = get_metatext(movie_filename)


def get_movieinfo(movie_filename: str) -> str:
    path = os.path.join(PAR_DIR, DATA_DIR, movie_filename)
    tree = ET.parse(path)
    info = tree.find("info").text

    return info


def get_moviedialogue(movie_path) -> List[Tuple[str, str, str]]:
    """Return List of Triples of (sentence_id, scene_id, sentence)
    """

    tree = ET.parse(movie_path)
    dialogue_tuples = []

    for scene in tree.findall("scene"):
        scene_id = scene.get("id")

        dialogue = scene.findall("dialogue")

        for d in dialogue:
            dialogue_tuples += [(sent.get("id"), scene_id, sent.text) for sent in d.findall("s")]

    # for d in dialogue_tuples:
    #     print(d)
    return dialogue_tuples


def get_characters(movie_filename: str) -> Set[str]:
    """get the movie characters"""
    path = os.path.join(PAR_DIR, DATA_DIR, movie_filename)
    tree = ET.parse(path)
    temp = []

    for scene in tree.findall("scene"):
        temp += scene.findall("dialogue")

    characters = set([char.get("name") for char in temp])

    return characters


def get_metatext(movie_filename) -> List[str]:
    """Get only the meta text from the moviescript, together with a reference to the scene?"""
    path = os.path.join(PAR_DIR, DATA_DIR, movie_filename)
    tree = ET.parse(path)

    meta_tuples = []
    for scene in tree.findall("scene"):
        meta_tuples += [(m.get("id"), m.text) for m in scene.findall("meta")]

    # for m in meta_text:
    #     print(m)
    return meta_tuples


def get_genres(movie_filename: str) -> List[str]:
    """Gets the genres as list of strings from the allgenres.txt file"""
    genres = []
    with open(os.path.join(PAR_DIR, "allgenres.txt"), "r") as allgenres:
        movies = allgenres.read().splitlines()
        name, ext = os.path.splitext(movie_filename)
        for m in movies:
            if name in m:
                genres = m.split(":")[1].split(",")

        if len(genres) == 0:
            raise ValueError("Movie not found in allgenres.txt")

    return genres


def main():

    path = os.path.join(PAR_DIR, DATA_DIR)
    get_moviedialogue(os.path.join(path, "star-wars-4.xml"))
    # get_metatext("star-wars-4.xml")


if __name__ == '__main__':
    main()
