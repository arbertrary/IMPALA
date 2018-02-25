"""Preprocessing/parsing the subtitles in xml format"""

import os
import numpy as np
import xml.etree.ElementTree as ET
import string
from typing import List, Tuple
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def get_subtitles_for_annotating(path: str) -> List[Tuple[str, str, str]]:
    """Subtitles only for use in annotate
    :returns subtitles as list of Triples of (sentence_id, start-timecode, sentence)"""
    tree = ET.parse(path)
    root = tree.getroot()

    subdialogue = []
    time = "00:00:00,000"
    for sentence in root:
        dialogue = ""
        sentence_id = sentence.get("id")
        for child in sentence:

            if child.tag == "time" and str(child.get("id")).endswith("S"):
                time = child.get("value")

            elif child.tag == "time" and str(child.get("id")).endswith("E"):
                continue
            else:
                word = str(child.text)
                if word.endswith("'"):
                    dialogue += word
                else:
                    if word in string.punctuation:
                        dialogue = dialogue.strip() + word + " "
                    else:
                        dialogue = dialogue + word + " "

        sent_tuple = (sentence_id, time, dialogue.strip())
        subdialogue.append(sent_tuple)

    return subdialogue


def get_subtitles(path: str) -> List[Tuple[float, float, str]]:
    """Reads Subtitles from the xml files
    :returns List of Tuples of Strings as [starttime in s, endtime in s, text]"""
    tree = ET.parse(path)
    root = tree.getroot()

    beginning = datetime.strptime("00:00:00,000", '%H:%M:%S,%f')
    temp_dialogue = []
    start = 0
    end = 0
    dialogue = ""
    for sentence in root:
        for child in sentence:

            if child.tag == "time" and str(child.get("id")).endswith("S"):
                starttime_string = child.get("value")
                starttime = datetime.strptime(starttime_string, '%H:%M:%S,%f')
                start = (starttime - beginning).total_seconds()


            elif child.tag == "time" and str(child.get("id")).endswith("E"):
                endtime_string = child.get("value")
                endtime = datetime.strptime(endtime_string, '%H:%M:%S,%f')
                end = (endtime - beginning).total_seconds()
                if start == 0 or end == 0:
                    continue
                else:
                    sent_tuple = (start, end, dialogue.strip())
                    temp_dialogue.append(sent_tuple)
                    dialogue = ""
                    start = 0
                    end = 0
            else:
                word = str(child.text)
                if word.endswith("'"):
                    dialogue += word
                else:
                    if word in string.punctuation or word.startswith("'"):
                        dialogue = dialogue.strip() + word + " "
                    else:
                        dialogue = dialogue + word + " "

        # if starttime_string == "" or endtime_string == "":
        # if start == 0 or end == 0:
        #     continue
        # else:
        #     sent_tuple = (start, end, dialogue.strip())
        #     temp_dialogue.append(sent_tuple)
        #     # dialogue = ""
        #     start = 0
        #     end = 0

    subtitles = __same_time_dialogue(temp_dialogue)
    return subtitles


def __same_time_dialogue(subtitles: List) -> List:
    """Combines sentences with the same start time. Not necessary for subtitles from the opus.nl corpus
    but for subtitles parsed with srt_to_xml from parse_srt module"""
    start = subtitles[0][0]
    end = subtitles[0][1]
    dialogue = ""
    subdialogue = []
    for x in subtitles:
        if start == x[0]:
            dialogue = dialogue + " " + x[2]
        else:
            subdialogue.append((start, end, dialogue.strip()))

            start = x[0]
            end = x[1]
            dialogue = x[2]

    return subdialogue


def get_avg_duration(subtitles: List):
    """:returns average time on screen for subtitles"""
    temp = []
    for s in subtitles:
        start = s[0]
        end = s[1]
        temp.append(end - start)  # .total_seconds())
    return np.mean(temp)


def check_correctness(path: str):
    """Checks whether a file of xml subtitles is correctly numbered and the time codes are continuous"""

    tree = ET.parse(path)

    sub_id = 1
    root = tree.getroot()

    for sentence in root:
        if int(sentence.get("id")) != sub_id:
            raise ValueError("Error at sentence " + str(sub_id) + ": ID not continuous")
        sub_id += 1

    times = tree.iter("time")

    currenttime = datetime.strptime("00:00:00,000", '%H:%M:%S,%f')
    for time in times:
        if str(time.get("id")).endswith("S"):
            timestring = time.get("value")
            t = datetime.strptime(timestring, '%H:%M:%S,%f')

            if t < currenttime:
                raise ValueError("Time not continuous @" + time.get("id"))
            currenttime = t
        else:
            continue


def main():
    path = os.path.join(BASE_DIR, "src/testfiles", "star-wars-4_subs.xml")
    # path = os.path.join(BASE_DIR, "src/testfiles", "blade_subs.xml")

    # print(get_subtitles(path))

    check_correctness(path)
    test = get_subtitles(path)
    for t in test:
        print(t)


if __name__ == '__main__':
    main()
