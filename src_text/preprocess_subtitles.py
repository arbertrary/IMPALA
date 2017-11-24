#!/usr/bin/env python

"""
- Preprocesses subtitle files
- Checks correctness of format of subtitles (downloaded as .srt files from subscene.com)
"""


import re
import os
import string

from datetime import datetime, timedelta
from nltk import word_tokenize
from nltk.corpus import stopwords

CUR_DIR = os.path.dirname(__file__)
PAR_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
DATA_DIR = 'testfiles'


def clean_subtitle_file(subs_filename):
    """encode/decode, strip every line, remove formatting tags, overwrite file"""
    textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    subs_path = os.path.join(textdata_dir, subs_filename)

    with open(subs_path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        data = [line.strip() for line in data]

        text = '\n'.join(data)
        text = re.sub('<[^<]+?>', '', text)
        # text = re.sub('-\s', '', text)
        # text = re.sub('–\s', '', text)
        text = text.strip()

    # with open(subs_path, 'w', encoding='utf-8') as f:
    #     f.write(text)


# TODO: extract timecodes
def check_subtitle_file(subs_filename):
    """
    check file for correct .srt format
    check if linecounter is continuous
    check if timecode has correct format
    """
    textdata_dir = os.path.join(PAR_DIR, DATA_DIR)
    subs_path = os.path.join(textdata_dir, subs_filename)

    clean_subtitle_file(subs_filename)

    countpattern = re.compile(r'\d+')
    timepattern = re.compile(
        r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")

    linecounter = 1
    with open(subs_path) as f:
        text = f.read()

        subtitlelist = text.split(os.linesep + os.linesep)

        for paragraph in subtitlelist:
            sub = paragraph.split(os.linesep)
            if countpattern.fullmatch(sub[0]):
                if int(sub[0]) == linecounter:
                    linecounter += 1
                else:
                    print(paragraph)
                    raise ValueError(
                        "Inputfile not in correct format!\n Subtitle counter not continuous!")
            else:
                print(paragraph)
                raise ValueError(
                    "Inputfile not in correct format!\n Subtitle counter contains error!")

            if not timepattern.fullmatch(sub[1]):
                print(sub[1])
                raise ValueError(
                    "Inputfile not in correct format!\n Timepattern contains error!")

    return subtitlelist

# sollte ich dialog als list der lines extrahieren oder als string?
# ich wandle ja eh wieder in strings um fürs tokenizen

# TODO: Beim Extrahieren die timecodes mitnehmen zum wiederverwenden
def extract_subdialogue(subs_filename):
    """Extracts only dialogue from subtitle files"""
    # subs_path = os.path.join(dirpath, subs_filename)
    # with open(subs_path) as f:
    #     text = f.read()
    #
    #     paragraphs = text.split(os.linesep + os.linesep)
    subtitlelist = check_subtitle_file(subs_filename)
    dialogue = []

    for paragraph in subtitlelist:
        sub = paragraph.split(os.linesep)

        for i in sub[2:]:
            dialogue.append(i.lower())

        # dialogue += s[2:]

    return dialogue


def get_dialogue_with_time(subs_filename):
    """Extracts dialogue with timecode as tuple of (timecode, text)"""

    subtitlelist = check_subtitle_file(subs_filename)
    subtitles = []
    timepattern = re.compile(
        r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")

    for paragraph in subtitlelist:

        dialogue = []
        sub = paragraph.split(os.linesep)
        m = timepattern.match(sub[1])

        starttime = datetime.strptime(m.group(1), '%H:%M:%S,%f')#.time()

        for i in sub[2:]:
            # irgendwie ist das ja mega dumm, das erst von str in list und dann
            # wieder in einen string umzuwandeln, aber wie bekomme ich sonst das
            # leerzeichen zwischen die Sätze?
            dialogue.append(i)

        sub_tuple = (starttime, " ".join(dialogue))
        subtitles.append(sub_tuple)
    return subtitles

def separate_subs_by_time(subs_filename, duration):
    """Separates subtitles into periods based on timecodes/duration"""
    # scenelength = timedelta(minutes=duration)

    timepattern = re.compile(
        r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")

    subtitlelist = check_subtitle_file(subs_filename)

    end = subtitlelist[-1]
    m = timepattern.match(end.split(os.linesep)[1])
    pseudomovielength = datetime.strptime(m.group(2), '%H:%M:%S,%f').time()

    print(end)
    print(pseudomovielength)

# Der Ansatz mit scenelength und temp runterzählen macht ja an sich wenig Sinn,
# weil's ja nicht durchgehend Dialog im Film ist
    # temp = scenelength
    # timesep_list = []
    # dialogue = ''
    # for p in subtitlelist:
    #     sub = p.split(os.linesep)
    #
    #     m = timepattern.match(sub[1])
    #
    #     starttime = datetime.strptime(m.group(1), '%H:%M:%S,%f')
    #     endtime = datetime.strptime(m.group(2), '%H:%M:%S,%f')
    #
    #     d = endtime-starttime
    #     s = ' '.join(sub[2:])
    #     temp = temp -d
    #     if(temp > timedelta(microseconds=0)):
    #         dialogue +=s
    #     else:
    #         temp = scenelength
    #         timesep_list.append(dialogue)
    #         dialogue = ''
    #
    # print(len(timesep_list))


def tokenize_dialogue(subs_filename):
    """Tokenize dialogue for frequency analysis/comparison with dialogue from moviescript"""
    dialogue = extract_subdialogue(subs_filename)
    dialogue = '\n'.join(dialogue)

    dialogue = dialogue.translate(str.maketrans('', '', string.punctuation))

    stop = stopwords.words('english')
    dialogue_tokens = word_tokenize(dialogue)
    dialogue_tokens = [i for i in dialogue_tokens if i not in stop]

    return dialogue_tokens


def main():
    """Die main halt"""
    # print(extract_subdialogue("testsubs.txt"))
    #separate_subs_by_time("Star-Wars-A-New-HopeSubtitles.srt", 2)
    print(get_dialogue_with_time("testsubs.txt"))

    # check_subtitle_file('BladeRunnerSubtitles.srt')
    # check_subtitle_file('Star-Wars-A-New-HopeSubtitles.srt')#, 'Star-Wars-A-New-Hope.txt')
    # check_subtitle_file('AmericanPsychoSubtitles.srt')

if __name__ == '__main__':
    main()
