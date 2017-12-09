"""Comparing movie scripts and subtitle file.
Upcoming: annotating movie scripts with time codes from subtitles """

import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from pp_xmlSubtitles import get_subtitles
from pp_moviescript import get_moviedialogue
from typing import List, Tuple, Dict


PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"

def get_scene_timecodes(movie_filename: str, subs_filename: str) -> Dict[str, List[datetime]]:
    """Find closest matching sentences"""
    subs_dialogue = get_subtitles(subs_filename)
    # [(timecode, sentence), (timecode, sentence) ...]

    movie_dialogue = get_moviedialogue(movie_filename)
    # [(sceneID, sentence), (sceneID, sentence) ...]

    scene_times = {"s1" : []}

    done1 =[]
    done2 = []
    count = 0
    for i, subsent in enumerate(subs_dialogue):
        for j, moviesent in enumerate(movie_dialogue):
            if j < (i-200):
                continue
            elif j > (i+200):
                break
            else:
                if moviesent[1] not in done2 and subsent[1] not in done1:
                    ratio = fuzz.ratio(subsent[1].lower(), moviesent[1].lower())
        # best between 88 and 89
                    if ratio > 80:
                        done1.append(subsent[1])
                        done2.append(moviesent[1])
                        count += 1

                        # time = subsent[0]
                        time = datetime.strptime(subsent[0], '%H:%M:%S,%f')#.time()

                        sceneID = moviesent[0]
                        if sceneID in scene_times:
                            scene_times[sceneID].append(time)
                        else:
                            scene_times[sceneID] = [time]

                        print(i, j)
                        print(moviesent[1])
                        print(subsent[1])
                        print(ratio)
                        # print("\n")

                    else:
                        continue

    # print("sentences in subs: ", len(subs_dialogue))
    # print("sentences in movie: ", len(movie_dialogue))
    # print("found: ", count)

    # print(scene_times["s1"])
    return scene_times


def get_avg_scene_times(movie_filename: str, subs_filename: str) -> List[Tuple[str, datetime]]:
    """Returns the average timecode for scenes with dialogue"""

    scene_times = get_scene_timecodes(movie_filename, subs_filename)

    scene_times_tuples = []
    for scene in scene_times:
        times = scene_times[scene]

        temp = []

        for t in times:
            # asdf = datetime.strptime(t, '%H:%M:%S,%f')

            millis = t.timestamp() * 1000
            # print(millis)
            temp.append(millis)

        avg = sum(temp) / len(temp)

        dt = datetime.fromtimestamp(avg / 1000)
        # print(scene, dt.time())
        scene_times_tuples.append((scene, dt.time()))

    # print(len(scene_times_tuples))
    # for s in scene_times_tuples:
    #     print(s)

    return scene_times_tuples


def annotate_time(movie_filename: str, subs_filename: str):
    times = get_avg_scene_times(movie_filename, subs_filename)
    path = os.path.join(PAR_DIR, DATA_DIR, movie_filename)

    tree = ET.parse(path)

    scenes = tree.findall("scene")

    for scene_time in times:
        for scene_xml in scenes:
            id = scene_time[0]
            time = scene_time[1]

            if scene_xml.attrib["id"] == id:
                scene_xml.set("timecode", time.strftime('%H:%M:%S'))
    tree.write("annotated.xml")



    # return "test"



# def test_needleman(movie_filename: str, subs_filename: str):
#     """testing nwalign3"""
#
#     subs_dialogue = ' '.join(extract_subdialogue(subs_filename))
#     subs_dialogue = word_tokenize(subs_dialogue)
#
#     movie_dialogue = ' '.join(extract_moviedialogue(movie_filename))
#     movie_dialogue = word_tokenize(movie_dialogue)
#
#     for subsent in subs_dialogue:
#         for moviesent in movie_dialogue:
#             test = nw.global_align(subsent, moviesent)
#
#
#             score = nw.score_alignment(test[0].upper(), test[1].upper(), gap_open=-10, gap_extend=-5, matrix='PAM250')
#             if score > 10:
#                 print(test[0])
#                 print(test[1])
#                 print(score)


def main():
    """main function"""
    # find_closest_sentences("star-wars-4.xml", "star-wars-4_sub.xml")
    #get_avg_scene_times("testmovie.xml", "testsubs.xml")

    time = datetime.now()
    annotate_time("star-wars-4.xml", "star-wars-4_sub.xml")
    # annotate_time("testmovie.xml", "testsubs.xml")

    time2 = datetime.now()

    diff = time2-time
    print(diff)





    #test = nw.global_align("est", "testlul")

    # print(test[0].upper())
    # print(test[1])

    #print(nw.score_alignment(test[0].upper(), test[1].upper(), gap_open=-5, gap_extend=-2, matrix='PAM250'))
    # print(nw.score_alignment('CEELECANTH', '-PELICAN--', gap_open=-5,
    # gap_extend=-2, matrix='PAM250'))

    # test_needleman("Star-Wars-A-New-Hope.txt", "Star-Wars-A-New-HopeSubtitles.srt")
    # test_needleman("testmovie.txt", "testsubs.txt")


if __name__ == '__main__':
    main()
