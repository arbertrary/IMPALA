"""Annotating xml movie scripts with time codes found in subtitle files"""

import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from subtitles import get_subtitles_for_annotating
from typing import List, Tuple, Dict

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


def annotate(movie_path: str, subs_path: str, dest_path: str):
    """ Input: xml movie script without times and xml subtitle file
        Output: annotated xml movie script with average time and interpolated time codes @ scenes and
        time codes @ matched sentences
    """
    scene_times, sentence_times = __match_sentences(movie_path, subs_path)

    avg_scene_times = __get_avg_scene_times(scene_times)

    tree = __write_time(movie_path, avg_scene_times, sentence_times)

    __interpolate_timecodes(tree, dest_path)


def __write_time(movie_path: str, avg_scene_times: List, sentence_times: Dict) -> ET.ElementTree:
    """Adds the timecode to the scenes and sentences in the movie script xml file"""
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
    """Find closest matching sentences; Return two Dicts
    a) {scene_id : [timecode sentence1, timecode sentence2 ...]}
    b) {sentence_id : (timecode, sentence id from subtitle file)}
    """
    subs_dialogue = get_subtitles_for_annotating(subs_path)
    # [(sentence_id, timecode, sentence), (sentence_id, timecode, sentence) ...]

    movie_dialogue = __get_moviedialogue(movie_path)
    # [(sentence_id, scene_id, sentence), (sentence_id, scene_id, sentence) ...]

    diff = abs(len(movie_dialogue) - len(subs_dialogue))

    # scene_times = {"s1": []}
    scene_times = {}
    sentence_times = {}
    done1 = []
    done2 = []
    count = 0
    for i, subsent in enumerate(subs_dialogue):
        for j, moviesent in enumerate(movie_dialogue):
            if j < (i - diff):
                continue
            elif j > (i + diff):
                break
            else:
                if moviesent[2] not in done2 and subsent[2] not in done1:
                    ratio = fuzz.ratio(subsent[2].lower(), moviesent[2].lower())
                    if ratio > 80:
                        done1.append(subsent[2])
                        done2.append(moviesent[2])
                        count += 1

                        # print(subsent[2])
                        # print(moviesent[2])
                        # print(ratio)

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


def __get_avg_scene_times(scene_timecodes: Dict[str, List[datetime]]) -> List[Tuple[str, datetime]]:
    """Returns the average timecode for scenes
    (averaged over the timecodes of dialogue-sentences, that were found in __match_sentences)
    """

    scene_times_tuples = []
    for scene in scene_timecodes:
        times = scene_timecodes[scene]

        temp = []

        for t in times:
            # asdf = datetime.strptime(t, '%H:%M:%S,%f')
            millis = t.timestamp() * 1000
            temp.append(millis)

        avg = sum(temp) / len(temp)

        dt = datetime.fromtimestamp(avg / 1000)
        scene_times_tuples.append((scene, dt.time()))

    return scene_times_tuples


def __get_moviedialogue(movie_path) -> List[Tuple[str, str, str]]:
    """Return List of Triples of (sentence_id, scene_id, sentence)"""

    tree = ET.parse(movie_path)
    dialogue_triples = []

    for scene in tree.findall("scene"):
        scene_id = scene.get("id")

        dialogue = scene.findall("dialogue")

        for d in dialogue:
            dialogue_triples += [(sent.get("id"), scene_id, sent.text) for sent in d.findall("s")]

    return dialogue_triples


def __interpolate_timecodes(tree: ET.ElementTree, dest_path: str):
    """Add interpolated time codes to scenes that previously had no annotated time code"""

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


def main():
    """main function"""

    path = os.path.join(PAR_DIR, DATA_DIR)

    time = datetime.now()

    annotate(os.path.join(path, "hellraiser.xml"), os.path.join(path, "hellraiser_sub.xml"),
             os.path.join(path, "hellraiser_annotated.xml"))

    # test1, test2 = match_sentences(os.path.join(path, "hellraiser.xml"), os.path.join(path, "hellraiser_sub.xml"))
    #
    # for t in test1:
    #     print(t, test1[t])
    #
    # for t in test2:
    #     print(t, test2[t])

    time2 = datetime.now()
    diff = time2 - time
    print(diff)


if __name__ == '__main__':
    main()
