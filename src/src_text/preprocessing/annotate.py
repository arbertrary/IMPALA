"""Annotating xml movie scripts with time codes found in subtitle files"""

import xml.etree.ElementTree as ET
import os
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from typing import List, Tuple, Dict
from src.src_text.preprocessing.subtitles import get_subtitles_for_annotating

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def annotate(movie_path: str, subs_path: str, dest_path: str, interpolate: bool = False):
    """Walks through all the steps for automatically annotating a movie script with time codes from subtitles.
    :param movie_path: xml movie script
    :param subs_path: xml subtitle file
    :param dest_path: the destination path
    :param interpolate: if True the scenes in the movie script where no subtitle dialogue was found
     are annotated with interpolated time codes. Defaults to False

     :returns Writes annotated xml movie script
    """
    scene_times, sentence_times = __match_sentences2(movie_path, subs_path)

    avg_scene_times = __get_avg_scene_times(scene_times)

    tree = __write_time(movie_path, avg_scene_times, sentence_times)

    if interpolate:
        __interpolate_timecodes(tree, dest_path)
    else:
        tree.write(dest_path)


def __write_time(movie_path: str, avg_scene_times: List, sentence_times: Dict) -> ET.ElementTree:
    """Adds the timecode to the scenes and sentences in the movie script xml file.
    :param movie_path: xml movie script
    :param avg_scene_times: list of scene time codes (averaged over all sentences with time in the scene)
    :param sentence_times: list of time codes of matched sentences
    :returns xml ElementTree"""
    tree = ET.parse(movie_path)

    for scene_time in avg_scene_times:
        for scene_xml in tree.iter("scene"):
            scene_id = scene_time[0]
            time = scene_time[1]
            if scene_xml.attrib["id"] == scene_id:
                scene_xml.set("time_avg", time.strftime('%H:%M:%S'))

    for sentence_time in sentence_times:
        for s in tree.iter("s"):
            sent_id = sentence_time
            time = sentence_times.get(sentence_time)[0]
            sub_sentence_id = sentence_times.get(sentence_time)[1]
            if s.attrib["id"] == sent_id:
                s.set("time", time.strftime('%H:%M:%S'))
                s.set("subtitle_id", sub_sentence_id)

    return tree


def __match_sentences(movie_path: str, subs_path: str) -> Tuple[
    Dict[str, List[datetime]], Dict[str, Tuple[datetime, str]]]:
    """Find closest matching sentences in movie script and subtitles
    :param movie_path: xml movie script file
    :param subs_path: xml subtitle file
    :returns Dict of key= scene_id and value=time codes per scene
    {scene_id : [timecode sentence1, timecode sentence2 ...]}
    :returns Dict of key= sentence_id (from xml movie script) and time code
    {sentence_id : (timecode, sentence id from subtitle file)}
    """
    subs_dialogue = get_subtitles_for_annotating(subs_path)

    movie_dialogue = __get_moviedialogue(movie_path)

    # Only sentences with indices +/- diff are compared
    # e.g. subtitles from the first 10% of the movie script
    # are only compared to
    # diff = 0.05 * len(movie_dialogue)
    diff = 0.05
    scene_times = {}
    sentence_times = {}
    done1 = []
    done2 = []
    count = 0
    for i, subsent in enumerate(subs_dialogue):
        perc_i = i / len(subs_dialogue)
        for j, moviesent in enumerate(movie_dialogue):
            perc_j = j / len(movie_dialogue)
            # if j < (i - diff):
            #     continue
            # elif j > (i + diff):
            #     break
            if perc_j < (perc_i - diff):
                continue
            elif perc_j > (perc_i + diff):
                break
            else:
                if moviesent[2] not in done2 and subsent[2] not in done1:
                    ratio = fuzz.ratio(subsent[2].lower(), moviesent[2].lower())
                    if ratio > 80:
                        done1.append(subsent[2])
                        done2.append(moviesent[2])
                        count += 1

                        time = datetime.strptime(subsent[1], '%H:%M:%S,%f')

                        sentence_id = moviesent[0]
                        sentence_times[sentence_id] = (time, subsent[0])

                        scene_id = moviesent[1]

                        if scene_id in scene_times:
                            scene_times[scene_id].append(time)
                        else:
                            scene_times[scene_id] = [time]
                    else:
                        continue

    return scene_times, sentence_times


def __match_sentences2(movie_path: str, subs_path: str) -> Tuple[
    Dict[str, List[datetime]], Dict[str, Tuple[datetime, str]]]:
    subs_dialogue = get_subtitles_for_annotating(subs_path)

    movie_dialogue = __get_moviedialogue(movie_path)

    # Only sentences with indices +/- diff are compared
    # e.g. subtitles from the first 10% of the movie script
    # are only compared to
    # diff = 0.05 * len(movie_dialogue)
    diff = 0.05
    scene_times = {}
    sentence_times = {}
    done1 = []
    done2 = []
    count = 0
    for i, subsent in enumerate(subs_dialogue):
        perc_i = i / len(subs_dialogue)
        temp = []
        for j, moviesent in enumerate(movie_dialogue):
            perc_j = j / len(movie_dialogue)

            if perc_j < (perc_i - diff):
                continue
            elif perc_j > (perc_i + diff):
                if len(temp) == 0:
                    break
                s = max(temp, key=lambda x: x[0])[1]
                print(s)
                done1.append(s[2])
                done2.append(moviesent[2])
                count += 1

                time = datetime.strptime(s[1], '%H:%M:%S,%f')

                sentence_id = moviesent[0]
                sentence_times[sentence_id] = (time, s[0])

                scene_id = moviesent[1]

                if scene_id in scene_times:
                    scene_times[scene_id].append(time)
                else:
                    scene_times[scene_id] = [time]

                break

            else:
                if moviesent[2] not in done2 and subsent[2] not in done1:
                    ratio = fuzz.ratio(subsent[2].lower(), moviesent[2].lower())
                    if ratio > 80:
                        temp.append((ratio, subsent))
                    else:
                        continue

    return scene_times, sentence_times


def __get_avg_scene_times(scene_timecodes: Dict[str, List[datetime]]) -> List[Tuple[str, datetime]]:
    """Calculates average time for each scene from all the matched time codes in the scene
    :param scene_timecodes from __match_sentences
    :returns the average timecode for scenes
    (averaged over the timecodes of dialogue-sentences, that were found in __match_sentences)
    """

    scene_times_tuples = []
    for scene in scene_timecodes:
        times = scene_timecodes[scene]

        temp = []

        for t in times:
            millis = t.timestamp() * 1000
            temp.append(millis)

        avg = sum(temp) / len(temp)

        dt = datetime.fromtimestamp(avg / 1000)
        scene_times_tuples.append((scene, dt.time()))

    return scene_times_tuples


def __get_moviedialogue(movie_path) -> List[Tuple[str, str, str]]:
    """:returns List of Triples of (sentence_id, scene_id, sentence)"""

    tree = ET.parse(movie_path)
    dialogue_triples = []

    for scene in tree.findall("scene"):
        scene_id = scene.get("id")

        dialogue = scene.findall("dialogue")

        for d in dialogue:
            dialogue_triples += [(sent.get("id"), scene_id, sent.text) for sent in d.findall("s")]

    return dialogue_triples


def __interpolate_timecodes(tree: ET.ElementTree, dest_path: str):
    """Adds interpolated time codes to scenes that previously had no annotated time code"""

    scenes = tree.findall("scene")

    time_old = "00:00:00"

    scenes_without_time = []

    new_time_scenes = []
    for index, scene in enumerate(scenes):

        if scene.attrib.get("time_avg"):
            time_new = scene.attrib.get("time_avg")

            dt_new = datetime.strptime(time_new, '%H:%M:%S')
            dt_old = datetime.strptime(time_old, '%H:%M:%S')
            diff = dt_new - dt_old

            if len(scenes_without_time) != 0:

                step = diff.total_seconds() / (len(scenes_without_time) + 1)

                for s in scenes_without_time:
                    dt_old += timedelta(seconds=step)

                    new_time_scenes.append((s, dt_old.strftime('%H:%M:%S')))

            scenes_without_time = []
            time_old = time_new

        else:
            scenes_without_time.append(scene.attrib["id"])

        if index == len(scenes) - 1 and len(scenes_without_time) != 0:
            dt_old = datetime.strptime(time_old, '%H:%M:%S')

            for s in scenes_without_time:
                dt_old += timedelta(seconds=60)

                new_time_scenes.append((s, dt_old.strftime('%H:%M:%S')))

    for scene in new_time_scenes:
        for scene_xml in scenes:
            if scene_xml.attrib["id"] == scene[0]:
                scene_xml.set("time_interpolated", scene[1])

    tree.write(dest_path)


if __name__ == '__main__':
    annotate("star-wars-4.xml", "star-wars-4_subs.xml", "star_wars_annotated.xml")
    # file = os.path.join(BASE_DIR, "data/movies_with_subs_and_script.txt")
    # with open(file) as mv_file:
    #     movies = mv_file.read().splitlines(keepends=False)
    #
    #     for m in movies[1:]:
    #         print(m)
    #         script = os.path.join(BASE_DIR, "data/moviescripts_xml", m+".xml")
    #         subs = os.path.join(BASE_DIR, "data/subtitles_xml", m+"_subs.xml")
    #
    #         dest = os.path.join(BASE_DIR, "data/moviescripts_xml_time/10perc80ratio_new",m+"_annotated.xml")
    #
    #         # if not(os.path.isfile(script) and os.path.isfile(subs)):
    #         #     print(m)
    #
    #         annotate(script,subs,dest)
