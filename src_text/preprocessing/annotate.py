"""Comparing movie scripts and subtitle file.
Upcoming: annotating movie scripts with time codes from subtitles """

import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from subtitles import get_subtitles
from moviescript import get_moviedialogue
from typing import List, Tuple, Dict

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


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
                        scene_id = moviesent[1]

                        if scene_id in scene_times:
                            scene_times[scene_id].append(time)
                        else:
                            scene_times[scene_id] = [time]

                        sentence_times[sentence_id] = time

                        # print(i, j)
                        # print(moviesent[1])
                        # print(subsent[2])
                        # print(ratio)

                    else:
                        continue

    return scene_times, sentence_times


def get_avg_scene_times(movie_filename: str, subs_filename: str) -> List[Tuple[str, datetime]]:
    """Returns the average timecode for scenes with dialogue"""

    scene_times = match_sentences(movie_filename, subs_filename)[0]

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


# TODO: Zeiten der einzelnen SÄtze annotieren
def annotate_time(movie_filename: str, subs_filename: str):
    """Adds the timecode to the scenes in the movie script xml file"""
    scene_times = get_avg_scene_times(movie_filename, subs_filename)
    path = os.path.join(PAR_DIR, DATA_DIR, movie_filename)

    tree = ET.parse(path)

    scenes = tree.findall("scene")

    for scene_time in scene_times:
        for scene_xml in scenes:
            id = scene_time[0]
            time = scene_time[1]

            if scene_xml.attrib["id"] == id:
                scene_xml.set("time", time.strftime('%H:%M:%S'))
    tree.write("annotated.xml")


def add_time_inbetween_scenes(xml_filename: str):
    """Add timecode to scenes that originally had none. Based on timecodes before and after those scenes."""
    path = os.path.join(PAR_DIR, DATA_DIR, xml_filename)
    tree = ET.parse(path)

    scenes = tree.findall("scene")

    time_old = "00:00:00"

    scenes_without_time = []

    new_time_scenes = []
    for index, scene in enumerate(scenes):

        if scene.attrib.get("time"):
            time_new = scene.attrib.get("time")

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
                dt_old += timedelta(seconds=30)

                new_time_scenes.append((s, dt_old.strftime('%H:%M:%S')))

    for scene in new_time_scenes:
        for scene_xml in scenes:
            if scene_xml.attrib["id"] == scene[0]:
                scene_xml.set("time_interpolated", scene[1])

    annotated = os.path.join(PAR_DIR, DATA_DIR, "star-wars-4_alltimes.xml")
    tree.write(annotated)


def main():
    """main function"""

    path = os.path.join(PAR_DIR, DATA_DIR)

    time = datetime.now()
    #annotate_time("star-wars-4.xml", "star-wars-4_sub.xml")
    # annotate_time("testmovie.xml", "testsubs.xml")
    #test = match_sentences(os.path.join(path, "star-wars-4.xml"), os.path.join(path, "star-wars-4_sub.xml"))
    test = get_avg_scene_times(os.path.join(path, "star-wars-4.xml"), os.path.join(path, "star-wars-4_sub.xml"))
    time2 = datetime.now()
    diff = time2-time
    print(diff)

    for item in test:
        print(item)

    # add_time_inbetween_scenes("testmovie_annotated.xml")
    # add_time_inbetween_scenes("star-wars-4_annotated.xml")



if __name__ == '__main__':
    main()
