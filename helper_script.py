"""Multi-purpose helper script probably mostly outdated by now (4 Feb 2018)
Moving files and stuff
"""

import os
import re
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom
from src.src_text.preprocessing.moviescript import get_full_scenes

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

    subs_dir = os.path.join(BASE_DIR, "subtitles_xml")

    for film in filmliste:
        filename = film + "_subs.xml"

        if filename in os.listdir(subs_dir):
            src = os.path.join(subs_dir, filename)
            dest = os.path.join(BASE_DIR, "data_subtitles", filename)
            shutil.copy(src, dest)
            print(src, dest)

        else:
            print(filename)


def annotate_genres_to_subs():
    with open("allgenres.txt") as g:
        genres = g.read().splitlines(keepends=False)

        genre_dict = {}
        for film in genres:
            temp = film.split(":")
            genre_dict[temp[0]] = temp[1]

        # for f in genre_dict:
        #     print(f, genre_dict[f])

    for film in os.listdir("data_subtitles"):
        name = re.sub(r"_subs.xml", "", film)
        genres = genre_dict.get(name)

        if genres:
            print(film, genres)

        path = os.path.join("data_subtitles", film)

        tree = ET.parse(path)
        root = tree.getroot()
        test = ET.Element("genres")
        test.text = genres
        root.insert(0, test)

        tree.write(path)

    # path = os.path.join("subtitles_xml", "blade_subs.xml")
    # tree = ET.parse(path)
    # root = tree.getroot()
    # # test = ET.SubElement(root, "genre").text = "testgenre"
    # test= ET.Element("genre")
    # test.text = "testgenre"
    # root.insert(0, test)
    #
    # tree.write(path)


def genre_set():
    with open("allgenres2.txt") as g:
        genres = g.read().splitlines(keepends=False)

        genreset = []
        for film in genres:
            temp = film.split(":")[1].split(",")
            for g in temp:
                genreset.append(g)
        genreset = set(genreset)

        print(genreset)


def scene_counter(directory):
    with open("filmliste.txt") as f:
        filme = f.read().splitlines(keepends=False)

    scenecount = 0
    filmcount = 0
    for filename in os.listdir(directory):
        name = os.path.splitext(filename)[0]
        if name in filme:
            print(name)
            filmcount += 1

            path = os.path.join(directory, filename)
            tree = ET.parse(path)
            scenecount += len(tree.findall("scene"))
    print(scenecount, filmcount)


def check_scene_count():
    for filename in os.listdir("data_xml"):
        tree = ET.parse(os.path.join("data_xml", filename))
        scenes = tree.findall("scene")
        if len(scenes) < 20:
            print(filename, len(scenes))


def main():
    path = os.path.join(BASE_DIR, "moviescripts_xml_time_manually/the-matrix_man_TODO.xml")

    tree = ET.parse(path)
    scenes = tree.findall("scene")
    for scene in scenes:
        if scene.get("start") == "" and scene.get("end") == "":
            # scene.pop("start")
            # scene.pop("end")
            del scene.attrib["start"]
            del scene.attrib["end"]

    tree.write(path)



if __name__ == '__main__':
    main()
