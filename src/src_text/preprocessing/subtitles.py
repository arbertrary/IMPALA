"""Preprocessing/parsing the subtitles in xml format"""

import os
import numpy as np
import xml.etree.ElementTree as ET
import string
from typing import List, Tuple
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def get_subtitles_for_annotating(path: str) -> List[Tuple[str, str, str]]:
    """returns subtitles as list of Triples of (sentence_id, start-timecode, sentence)"""
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

    # i=1
    # for d in subdialogue:
    #     if i<20:
    #         print(time, d[1].strip())
    #         i += 1
    #     else:
    #         break
    return subdialogue


def get_subtitles(path: str) -> List[Tuple[str, str]]:
    tree = ET.parse(path)
    root = tree.getroot()

    temp_dialogue = []
    time = "00:00:00,000"
    for sentence in root:
        dialogue = ""
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
                    if word in string.punctuation or word.startswith("'"):
                        dialogue = dialogue.strip() + word + " "
                    else:
                        dialogue = dialogue + word + " "

        sent_tuple = (time, dialogue.strip())
        temp_dialogue.append(sent_tuple)

    time = temp_dialogue[0][0]
    dialogue = ""
    subdialogue = []
    for x in temp_dialogue:
        if time == x[0]:
            dialogue = dialogue + " " + x[1]
        else:
            subdialogue.append((time, dialogue.strip()))

            time = x[0]
            dialogue = x[1]

    return subdialogue


def get_avg_timediff(path: str):
    tree = ET.parse(path)
    root = tree.getroot()

    start = ""
    end = ""
    times = list(tree.iter("time"))
    test = []
    i = 0
    while i + 1 < len(times):
        start = datetime.strptime(str(times[i].get("value")), '%H:%M:%S,%f')
        end = datetime.strptime(str(times[i + 1].get("value")), '%H:%M:%S,%f')

        test.append((end - start).total_seconds())
        i += 2
    return np.mean(test)


def check_correctness(path: str):
    """Checks whether a file of xml subtitles is correctly numbered and the time codes are continuous"""

    tree = ET.parse(path)

    id = 1
    root = tree.getroot()

    for sentence in root:
        if int(sentence.get("id")) != id:
            raise ValueError("Error at sentence " + str(id) + ": ID not continuous")
        id += 1

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
    # print(get_subtitles_for_annotating("star-wars-4_subs.xml"))
    # path = os.path.join(PAR_DIR, DATA_DIR, "blade-trinity_subs.xml")
    # path = os.path.join(PAR_DIR, DATA_DIR, "american-psycho_subs.xml")
    path = os.path.join(BASE_DIR, "testfiles", "gladiator_subs.xml")
    print(BASE_DIR)

    check_correctness(path)
    print(get_avg_timediff(path))
    # test = get_subtitles(path)
    # for s in test:
    #     print(s)


if __name__ == '__main__':
    main()
