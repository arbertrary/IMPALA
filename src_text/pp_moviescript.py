"""Preprocessing movie scripts"""

import os
import re
from typing import List, Tuple


CUR_DIR = os.path.dirname(__file__)
PAR_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
DATA_DIR = "testfiles"


def clean_moviescript(movie_filename: str):
    """doesn't do that much atm because other functions do all the stuff now"""
    textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    movie_path = os.path.join(textdata_dir, movie_filename)

    with open(movie_path, 'r', encoding='utf-8') as movie:
        text = movie.read()
        #text = re.sub(r"\n+", "\n", text)

        text = text.split(os.linesep)
        text = [line.strip() for line in text]
        print("\n".join(text))

        # text = movie.readlines()
        # text = [line.strip() for line in text]
        # print("\n".join(text))






# TODO: check if scene_tuples actually extracts all scenes
def get_scene_tuples(movie_filename: str) -> List[Tuple[str, str]]:
    """Separates movie script into scenes; returns tuples of (scene header, scene text)."""
    textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    movie_path = os.path.join(textdata_dir, movie_filename)

    with open(movie_path, 'r', encoding='utf-8') as movie:
        text = movie.read()
        text = text.strip()

        text = re.split(
            '((?:INT[.:]? |EXT[.:]? |INTERIOR[.:]? |EXTERIOR[.:]? )[^\n]+\n)',
            text)

        scenelist = [(("MOVIEBEGINNING", text[0]))]

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

    dialogue = []

    for scene in scenelist:
        lines = scene[1].split(os.linesep)

        i = 1
        while i < len(lines):
            if lines[i].strip().isupper():
                while i + 1 < len(lines) and lines[i + 1].strip():
                    # ignore meta text below speaker name like (speaks slowly):
                    if re.search(r'[(|)]', lines[i + 1].strip()):
                        i += 1
                    else:
                        dialogue.append(lines[i + 1].strip().lower())
                        i += 1

                i += 1
            else:
                i += 1

    return dialogue


def main():
    """main"""
    print("\n".join(extract_moviedialogue("Cars-2.txt")))
    # clean_moviescript("Cars-2.txt")

if __name__ == '__main__':
    main()
