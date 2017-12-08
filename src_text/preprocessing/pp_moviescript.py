"""Reading moviescript from xml format"""

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


def get_moviedialogue(movie_filename: str) -> List[Tuple[str, str]]:
    """Get only the dialogue from the moviescript, together with a reference to the scene?
    TODO: Vielleicht statt List[Tuple[id, satz] lieber mit dict {id: Tuple[sätze]}?
    Brauche ich nur die szenen-ID oder auch die dialog-id?
    """

    path = os.path.join(PAR_DIR, DATA_DIR, movie_filename)
    tree = ET.parse(path)
    dialogue_tuples = []

    for scene in tree.findall("scene"):
        scene_id = scene.get("id")

        dialogue = scene.findall("dialogue")

        for d in dialogue:
            dialogue_tuples += [(scene_id, sent) for sent in sent_tokenize(d.text)]

    # for d in dialogue_tuples:
    #     print(d)

    return dialogue_tuples


def get_characters(movie_filename: str) -> Set[str]:
    """get the characters"""
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
    print(get_genres("star-wars-4.xml"))
    # get_movieinfo("star-wars-4.xml")
    # print(get_characters("star-wars-4.xml"))
    # get_moviedialogue("star-wars-4.xml")
    # get_metatext("star-wars-4.xml")


if __name__ == '__main__':
    main()
