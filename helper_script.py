"""
Check and clean all movie scripts in directory
"""

import os
import re
import shutil
from nltk import word_tokenize
from src.src_text.preprocessing.subtitles import check_correctness

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))


# removes movie scripts
# 1121 scripts at the beginning
# 29.10.: 974 remaining
# removed scripts that
# a) don't use EXT/INT or EXTERIOR/INTERIOR to separate scenes
# b) have some html tags remaining

# 30.10.17: 953 remaining
# (removed scripts that don't contain information about author and script at the end)

# 6.11.17: 908 remaining
# (removed more scripts that don't use EXT./INT. etc to separate scenes)


def check_all(directory: str):
    """Checks moviescripts in directory and deletes incorrect ones"""
    incorrect_scripts = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8-sig') as m:
            text = m.read()

            check1 = re.search(
                '(INT[.:] |EXT[.:] |INTERIOR[.:] |EXTERIOR[.:] )',
                text)
            check2 = re.search('<[^<]+?>', text)

            if not check1:
                incorrect_scripts.append(filename)
                # raise ValueError('Inputfile not in correct format!')
            if check2:
                incorrect_scripts.append(filename)
    print(incorrect_scripts)
    print(len(incorrect_scripts))

    # testset = set(incorrect_scripts)
    for f in incorrect_scripts:
        print(f)
        # os.remove(os.path.join(dirpath, f))


def check_movieinfo_at_end_of_file(directory: str):
    """Checks if there is a paragraph at the end of the file that contains writers and genre"""
    end = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as m:
            text = m.read()
            text = text.strip()

            text = text.split('\n\n')
            movieinfo = text[-1]
            if not ('writers' in movieinfo.lower() and 'Genres : ' in movieinfo):
                end.append(filename)

    # for f in end:
    # os.remove(os.path.join(directory, f))

    print(end)
    print(len(end))


def get_all_genres(directory: str):
    """Extracts genres from all moviescripts and writes them to new file"""
    f = open(os.path.join(BASE_DIR, "allgenres2.txt"), 'w+')

    allgenres = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as m:
            text = m.read()
            text = text.replace('\xa0', ' ')
            # print(text)
            text = text.strip()

            text = text.split('\n\n')
            movieinfo = text[-1]

            movieinfo = movieinfo.split("\n")

            genres = ''
            for line in movieinfo:
                if 'Genres : ' in line:
                    genres = re.sub('Genres : ', '', line)

                    genres = genres.strip()
                    genres = word_tokenize(genres)
                    genres = ','.join(genres)

            moviedata = re.sub('.txt', '', filename) + ':' + genres
            allgenres.append(moviedata)

    allgenres = sorted(allgenres)
    f.write(("\n".join(allgenres)).strip())
    f.close()


def check_all_subs(directory):
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)

        try:
            check_correctness(path)
        except ValueError:
            print(filename)


def move_subtitles():
    with open("filmliste.txt") as filme:
        filmliste = filme.read().splitlines(keepends=False)
        # print(filmliste)

    subs_dir = os.path.join(BASE_DIR, "all_subtitles")

    for film in filmliste:
        filename = film + "_subs.xml"

        if filename in os.listdir(subs_dir):
            src = os.path.join(subs_dir, filename)
            dest = os.path.join(BASE_DIR, "data_subtitles", filename)
            shutil.copy(src, dest)
            print(src, dest)

        else:
            print(filename)


def main():
    """ist halt die main, wofür will pylint da einen docstring"""
    subs_dir = os.path.join(BASE_DIR, "data_subtitles")
    print(subs_dir)

    # check_all_subs(subs_dir)
    # move_subtitles()


if __name__ == '__main__':
    main()
