"""Helper Script: Parsing and annotating all available movie scripts"""

import os
import sys
from src.src_text.preprocessing.parse_fountain import moviescript_to_xml
from src.src_text.preprocessing.moviescript import annotate

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


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

        # print(os.path.join(dest_dir, xml_path))


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
            annotate(script, subs, dest)


def main():
    """ist halt die main, wofür will pylint da einen docstring"""
    # parse_all()
    # annotate_all()
    print("test")


if __name__ == '__main__':
    main()
