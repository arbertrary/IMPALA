"""Comparing movie scripts and subtitle file.
Upcoming: annotating movie scripts with time codes from subtitles """

import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from subtitles import get_subtitles
from moviescript_temp import get_moviedialogue
from typing import List, Tuple, Dict

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


def annotate(movie_path: str, subs_path: str, dest_path: str):
    scene_times, sentence_times = match_sentences(movie_path, subs_path)

    avg_scene_times = get_avg_scene_times(scene_times)

    tree = annotate_time(movie_path, avg_scene_times, sentence_times)

    add_time_inbetween_scenes(tree, dest_path)


# TODO: Zeiten der einzelnen Sätze annotieren
def annotate_time(movie_path: str, avg_scene_times: List, sentence_times: Dict):
    """Adds the timecode to the scenes in the movie script xml file"""
    tree = ET.parse(movie_path)

    scenes = tree.findall("scene")

    for scene_time in avg_scene_times:
        for scene_xml in scenes:
            scene_id = scene_time[0]
            time = scene_time[1]
            if scene_xml.attrib["id"] == scene_id:
                scene_xml.set("time_avg", time.strftime('%H:%M:%S'))

    for sentence_time in sentence_times:
        for s in tree.iter("s"):
            sent_id = sentence_time
            time = sentence_times[sentence_time]
            if s.attrib["id"] == sent_id:
                s.set("time", time.strftime('%H:%M:%S'))

    return tree


def match_sentences(movie_filename: str, subs_filename: str) -> Tuple[Dict[str, List[datetime]], Dict[str, datetime]]:
    """Find closest matching sentences; Assign timecodes to scenes; get average timecode of a scene"""
    subs_dialogue = get_subtitles(subs_filename)
    # [(sentence_id, timecode, sentence), (sentence_id, timecode, sentence) ...]

    movie_dialogue = get_moviedialogue(movie_filename)
    # [(sentence_id, scene_id, sentence), (sentence_id, scene_id, sentence) ...]

    scene_times = {"s1": []}
    sentence_times = {}
    done1 = []
    done2 = []
    count = 0
    for i, subsent in enumerate(subs_dialogue):
        for j, moviesent in enumerate(movie_dialogue):
            if j < (i - 200):
                continue
            elif j > (i + 200):
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
                        sentence_times[sentence_id] = time

                        scene_id = moviesent[1]

                        if scene_id in scene_times:
                            scene_times[scene_id].append(time)
                        else:
                            scene_times[scene_id] = [time]
                    else:
                        continue

    return scene_times, sentence_times


def get_avg_scene_times(scene_timecodes: Dict[str, List[datetime]]) -> List[Tuple[str, datetime]]:
    """Returns the average timecode for scenes with dialogue"""

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


def add_time_inbetween_scenes(tree, dest_path):
    """Add timecode to scenes that originally had none. Based on timecodes before and after those scenes."""

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

    annotate(os.path.join(path, "star-wars-4.xml"), os.path.join(path, "star-wars-4_sub.xml"), "annotated.xml")

    time2 = datetime.now()
    diff = time2 - time
    print(diff)


if __name__ == '__main__':
    main()
