"""Multi-purpose helper script for several utility functions. Often single-use"""

import os
import re
import sys
import shutil
import numpy as np
import xml.etree.ElementTree as ET
import src.src_text.preprocessing.moviescript as ms
from datetime import datetime
from nltk import word_tokenize
from src.src_text.preprocessing.parse_fountain import moviescript_to_xml
from src.src_text.preprocessing.subtitles import check_correctness

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


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
            if check2:
                incorrect_scripts.append(filename)
    print(incorrect_scripts)
    print(len(incorrect_scripts))

    for f in incorrect_scripts:
        print(f)


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


def rename_subs():
    all_subtitles = os.path.join(BASE_DIR, "subtitles_xml")
    test = os.listdir(all_subtitles)
    filename = test[0]
    print(os.path.join(all_subtitles, filename))
    print(os.path.join(all_subtitles, filename + "_subs.xml"))
    print(os.path.splitext(filename)[0] + "_subs.xml")

    for filename in os.listdir(all_subtitles):
        new_filename = os.path.splitext(filename)[0] + "_subs.xml"
        os.rename(os.path.join(all_subtitles, filename), os.path.join(all_subtitles, new_filename))


def parse_all():
    all_moviescripts = os.path.join(BASE_DIR, "moviescripts_fountain")
    dest_dir = os.path.join(BASE_DIR, "xml_moviescripts")
    list_dest_dir = os.listdir(dest_dir)
    for filename in os.listdir(all_moviescripts):
        path = os.path.join(all_moviescripts, filename)
        xml_path = os.path.splitext(filename)[0] + ".xml"
        try:
            if xml_path not in list_dest_dir:
                moviescript_to_xml(path, os.path.join(dest_dir, xml_path))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(filename)
            raise


def annotate_all():
    movies = []
    with open(os.path.join(BASE_DIR, "movies.txt")) as f:
        movies = f.readlines()
        movies = [l.strip() for l in movies]

    xml_moviescripts_dir = os.path.join(BASE_DIR, "xml_moviescripts")
    subtitles_dir = os.path.join(BASE_DIR, "data_subtitles")
    annotated_dir = os.path.join(BASE_DIR, "xml_moviescripts_annotated")
    print(os.listdir(annotated_dir)[0])
    for m in movies:
        script = os.path.join(xml_moviescripts_dir, m + ".xml")
        subs = os.path.join(subtitles_dir, m + "_subs.xml")

        new_filename = m + "_annotated.xml"
        dest = os.path.join(annotated_dir, new_filename)

        if new_filename not in os.listdir(annotated_dir):
            print(script)
            print(subs)
            print(dest)
            ms.annotate(script, subs, dest)


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
    lengths = []
    time_code_scenes = []
    not_continuous = []
    folder = "20perc90ratio"

    for filename in os.listdir("data/" + folder):
        times = []
        tree = ET.parse(os.path.join("data/" + folder, filename))
        scenes = tree.findall("scene")
        counter = 0
        for s in scenes:
            if s.get("time_avg"):
                times.append(s.get("time_avg"))
                counter += 1

        currenttime = datetime.strptime("00:00:00", '%H:%M:%S')
        for time in times:
            t = datetime.strptime(time, '%H:%M:%S')

            if t < currenttime:
                not_continuous.append(filename)
                break
            currenttime = t
        lengths.append(len(scenes))
        time_code_scenes.append(counter)

    print("avg. # of scenes:\n", np.mean(lengths))
    print("avg # of annotated scenes:\n", np.mean(time_code_scenes))
    print("# of scripts without continuous time codes:\n", len(not_continuous))
    print(not_continuous)


def main():
    check_scene_count()


if __name__ == '__main__':
    main()
