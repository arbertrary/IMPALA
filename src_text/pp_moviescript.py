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
        text = text.strip()

        # text = re.sub('\n+', '', text)
        # print(text)

        # test = m.readlines()
        # test = [textwrap.dedent(line) for line in test]
        # test = [line.strip() for line in test]
        # test = [re.sub('\n+', '', line) for line in test]

        # test = '\n'.join(test)

        # print(test)


        # Eigentlich wurden die ja schon alle aussortiert in check_all_moviescripts
        # test = re.search(
        #     '(INT[.:]{0,1} |EXT[.:]{0,1} |INTERIOR[.:]{0,1} |EXTERIOR[.:]{0,1} )',
        #     text)
        # if(not test):
        #     raise ValueError('Inputfile not in correct format!')
        text = re.split(
            '(INT[.:]{0,1} |EXT[.:]{0,1} |INTERIOR[.:]{0,1} |EXTERIOR[.:]{0,1} )',
            text)

        i = 1
        scenelist = []
        while i < len(text):
            # print(text[i] + text[i + 1])
            scenelist.append(text[i] + text[i + 1])

            i += 2

        for scene in scenelist:
            print(scene)


def separate_scenes(movie_filename: str):
    """Separates the scenes of a movie script by splitting at scenes e.g. at INT. or EXT."""
    textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    movie_path = os.path.join(textdata_dir, movie_filename)

    with open(movie_path, 'r', encoding='utf-8') as movie:
        text = movie.read()
        text = text.strip()

        text = re.split(
            '((?:INT[.:]? |EXT[.:]? |INTERIOR[.:]? |EXTERIOR[.:]? )[^\n]+\n)',
            text)
        # print('\nSCENESPLIT '.join(text))

        i = 1
        scenelist = []
        while i < len(text):
            # print(text[i] + text[i + 1])
            scenelist.append(text[i] + text[i + 1])

            i += 2
    return scenelist


#TODO: check if scene_tuples actually extracts all scenes
def scene_tuples(movie_filename: str) -> List[Tuple[str, str]]:
    """Currently does the same as separate_scenes but returns tuples of (scene header, scene text)."""
    textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    movie_path = os.path.join(textdata_dir, movie_filename)

    with open(movie_path, 'r', encoding='utf-8') as movie:
        text = movie.read()
        text = text.strip()

        text = re.split(
            '((?:INT[.:]? |EXT[.:]? |INTERIOR[.:]? |EXTERIOR[.:]? )[^\n]+\n)',
            text)
        # print('\nSCENESPLIT '.join(text))

        i = 1
        scenelist = []
        while i < len(text):
            scenetuple = (text[i], text[i + 1])
            scenelist.append(scenetuple)


            i += 2
    return scenelist


# sollte ich dialog als list der lines extrahieren oder als string?
# ich wandle ja eh wieder in strings um fürs tokenizen
# TODO: Beim Extrahieren irgendeine Referenz auf die zugehörige Szene mitnehmen
def extract_moviedialogue(movie_filename: str):
    """extracts all dialogue from a moviescript and ignores metatext"""
    scenelist = separate_scenes(movie_filename)

    dialogue = []

    for scene in scenelist:
        lines = scene.split(os.linesep)

        i = 1
        while i < len(lines):
            if lines[i].strip().isupper():
                while i + 1 < len(lines) and lines[i + 1].strip():
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
    # print(extract_moviedialogue("testmovie.txt"))
    test = separate_scenes("testmovie.txt")

    print("\n".join(extract_moviedialogue("testmovie.txt")))


if __name__ == '__main__':
    main()
