#!/usr/bin/env python

"""
- Preprocesses subtitle files
- Checks correctness of format of subtitles (downloaded as .srt files from subscene.com)
"""


import re
import os
from nltk import word_tokenize
from nltk.corpus import stopwords

import string

from datetime import datetime

dirpath = 'testfiles'

# encode/decode
# strip every line
# remove formatting tags
# overwrite file

def clean_subtitle_file(subs_filename):
    subs_path = os.path.join(dirpath, subs_filename)
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


# check file for correct .srt format
# check if linecounter is continuous
# check if timecode has correct format

# TODO: extract timecodes and dialogues
def check_subtitle_file(subs_filename):
    subs_path = os.path.join(dirpath, subs_filename)
    clean_subtitle_file(subs_filename)

    countpattern = re.compile("\d+")
    timepattern = re.compile(
        "(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")

    linecounter = 1
    with open(subs_path) as f:
        text = f.read()

        paragraphs = text.split(os.linesep + os.linesep)
        dialogue = ''

        for p in paragraphs:
            s = p.split(os.linesep)
            if(countpattern.fullmatch(s[0])):
                if(int(s[0]) == linecounter):
                    linecounter += 1
                else:
                    print(p)
                    raise ValueError(
                        "Inputfile not in correct format!\n Subtitle counter not continuous!")
            else:
                print(p)
                raise ValueError(
                    "Inputfile not in correct format!\n Subtitle counter contains error!")

            if(not timepattern.fullmatch(s[1])):
                print(s[1])
                raise ValueError(
                    "Inputfile not in correct format!\n Timepattern contains error!")
            else:
# Format timecodes to datetime objects
# Calculate timedelta between beginning and end of subtitle
                m = timepattern.match(s[1])
                #
                # dt1 = datetime.strptime(m.group(1), '%H:%M:%S,%f')
                # dt2 = datetime.strptime(m.group(2), '%H:%M:%S,%f')
                #
                # print(dt1.time())
                # print(dt2.time())
                # print('Duration: ' + str(dt2 - dt1))

def extract_subdialogue(subs_filename):
    subs_path = os.path.join(dirpath, subs_filename)
    with open(subs_path) as f:
        text = f.read()

        paragraphs = text.split(os.linesep + os.linesep)
        dialogue = []

        for p in paragraphs:
            s = p.split(os.linesep)
            i = 2
            while(i < len(s)):
                dialogue.append(s[i])
                i += 1

    return dialogue

# Tokenize dialogue for frequency analysis/comparison with dialogue from
# moviescript
def tokenize_dialogue(subs_filename):
    dialogue = extract_dialogue(subs_filename)
    dialogue = '\n'.join(dialogue)

    dialogue = dialogue.translate(str.maketrans('', '', string.punctuation))

    stop = set(stopwords.words('english'))
    dialogue_tokens = word_tokenize(dialogue)
    dialogue_tokens = set([i for i in dialogue_tokens if i not in stop])

    return dialogue_tokens


# def main():
#     # check_subtitle_file('BladeRunnerSubtitles.srt')
#     #check_subtitle_file('testfile.txt')
#     #check_subtitle_file('Star-Wars-A-New-HopeSubtitles.srt')#, 'Star-Wars-A-New-Hope.txt')
#     # check_subtitle_file('AmericanPsychoSubtitles.srt')
#
#     print(tokenize_dialogue("AmericanPsychoSubtitles.srt"))
# if __name__ == '__main__':
#     main()
