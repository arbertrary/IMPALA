"""TODO:
- alle annotierten szenen mit start-end + deren Sentiment scores
- die audio pro sekunde um dann die audio auf die szenen aufzuteilen
- dann den average nehmen und den average einer klasse zuweisen
- das ganze dann in eine csv datei mit ["Arousal", "Valence", "Energy"]

GILT ERSTMAL NUR FÜR BLADE:
silent = x <= 0.586673
medium =  0.58663 < x <= 1.830190
louder = 1.830190 < x <= 5.919347
else ...

min        0.003770
25%        0.586673
50%        1.830190
75%        5.919347
max       35.207653
"""

import os
import csv
import numpy as np
import librosa
import matplotlib.pyplot as plt
from datetime import datetime
from sentiment import ImpalaSent
from moviescript import get_full_scenes
from audio_analysis import partition_audiofeature

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))


def get_time_sentiment(xml_path):
    sentiment = ImpalaSent()
    scenes = get_full_scenes(xml_path)
    beginning = datetime.strptime("00:00:00", '%H:%M:%S')

    time_sentiment = []
    for s in scenes:
        text = " ".join(s[2])

        starttime_string = s[0]
        starttime = datetime.strptime(starttime_string, '%H:%M:%S')
        start = (starttime - beginning).total_seconds()

        endtime_string = s[1]
        endtime = datetime.strptime(endtime_string, '%H:%M:%S')
        end = (endtime - beginning).total_seconds()
        score = sentiment.score(text)
        time_sentiment.append((start, end, score[0], score[1]))

    time_sentiment.sort(key=lambda tup: tup[0])
    print(time_sentiment[0])
    valence_array = librosa.util.normalize(np.array([x[2] for x in time_sentiment]))
    arousal_array = librosa.util.normalize(np.array([x[3] for x in time_sentiment]))
    time_sentiment2 = [(x[0], x[1], y, z) for x in time_sentiment for y in valence_array for z in arousal_array]
    print(time_sentiment2[0])

    return time_sentiment


def audio_scenes(audio_path, ts):
    partitions = partition_audiofeature(audio_path, 1)
    # test = get_time_sentiment(blade_script, blade_audio)

    scene_audio = []
    for t in ts:
        temp_audio = [x[1] for x in partitions if t[0] <= x[0] <= t[1]]
        scene_audio.append(np.mean(temp_audio))

    print(len(scene_audio))

    with open("audio_sent.csv", "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerow(["Scene Start", "Scene End", "Valence", "Arousal", "Audio Level"])
        for i, t in enumerate(scene_audio):
            level = "nan"
            if t <= 0.586673:
                level = "silent"
            elif 0.58663 < t <= 1.830190:
                level = "medium"
            elif 1.830190 < t <= 5.919347:
                level = "louder"
            elif t <= 35.207653:
                level = "loudest"
            else:
                continue

            start = ts[i][0]
            end = ts[i][1]
            valence = ts[i][2]
            arousal = ts[i][3]

            writer.writerow([start, end, valence, arousal, level])


def main():
    blade_script = os.path.join(BASE_DIR, "testfiles", "blade_manually.xml")
    blade_audio = os.path.join(BASE_DIR, "testfiles", "blade.wav")
    selfie_audio = os.path.join(BASE_DIR, "testfiles", "selfiefromhell.wav")

    ts = get_time_sentiment(blade_script)
    audio_scenes(blade_audio, ts)


if __name__ == '__main__':
    main()
