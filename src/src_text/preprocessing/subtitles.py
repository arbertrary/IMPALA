"""Preprocessing/parsing the subtitles in xml format"""

import os
import xml.etree.ElementTree as ET
import string
from typing import List, Tuple
from datetime import datetime, timedelta

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


# class Subtitles:


def get_subtitles(movie_filename: str) -> List[Tuple[str, str, str]]:
    """returns subtitles as list of Triples of (sentence_id, start-timecode, sentence)"""
    path = os.path.join(PAR_DIR, DATA_DIR, movie_filename)
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


def get_sub_sentences(path: str) -> List[Tuple[str, str]]:
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

        sent_tuple = (time, dialogue.strip())
        subdialogue.append(sent_tuple)

    return subdialogue



def check_correctness(path: str):
    """Checks whether a file of xml subtitles is correctly numbered and the time codes are continuous"""

    tree = ET.parse(path)

    id = 1
    root = tree.getroot()

    for sentence in root:
        if int(sentence.get("id")) != id:
            raise ValueError("Error at sentence "+ str(id)+ ": ID not continuous")
        id += 1

    times = tree.iter("time")

    currenttime = datetime.strptime("00:00:00,000", '%H:%M:%S,%f')
    for time in times:
        if str(time.get("id")).endswith("S"):
            timestring = time.get("value")
            t = datetime.strptime(timestring, '%H:%M:%S,%f')

            if t < currenttime:
                raise ValueError("Time not continuous @"+time.get("id"))
            currenttime = t
        else:
            continue

def main():
    # print(get_subtitles("star-wars-4_sub.xml"))
    # path = os.path.join(PAR_DIR, DATA_DIR, "blade-trinity_subs.xml")
    path = os.path.join(PAR_DIR, DATA_DIR, "hellraiser_subs.xml")

    # check_correctness(path)

    test = get_sub_sentences(path)
    for s in test:
        print(s)

if __name__ == '__main__':
    main()
