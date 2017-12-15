"""
Check and clean all movie scripts in directory
"""

import os
import re
from nltk import word_tokenize
from fountain import scene_tuples

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = 'imsdbScripts'


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
    f = open(os.path.join(PAR_DIR, "allgenres2.txt"), 'w+')

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


def main():
    """ist halt die main, wofür will pylint da einen docstring"""
    print("Hello")
    # check_movieinfo_at_end_of_file(os.path.join(parentDir, dataDir))

    # get_all_genres(os.path.join(parentDir, dataDir))
    # check_all_moviescripts('imsdbScripts')
    # check_information_at_end_of_file('imsdbScripts')

    # testing if scene_tuples correctly extracts only scene headers
    directory = os.path.join(PAR_DIR, DATA_DIR)
    f = open(os.path.join(PAR_DIR, "scenetuplestest.txt"), 'w+')

    test = []
    for filename in os.listdir(directory):
        # print(filename)
        test2 = scene_tuples(filename)
        for t in test2:
            test.append("\t\t" + filename)
            if t[0].islower():
                raise ValueError("SCENE HEADER NOT CORRECT!")
            else:
                test.append(t[0])
            # print(t[0])
    f.write("\n".join(test).strip())
    f.close()


if __name__ == '__main__':
    main()
