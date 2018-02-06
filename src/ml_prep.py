"""TODO:
- alle annotierten szenen mit start-end + deren Sentiment scores
- die audio pro sekunde um dann die audio auf die szenen aufzuteilen
- dann den average nehmen und den average einer klasse zuweisen
- das ganze dann in eine csv datei mit ["Arousal", "Valence", "Energy"]
"""

import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import librosa
from ms_sentiment import scenesentiment_for_manually_annotated
from audio_analysis import partition_audiofeature

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))


def audio_scenes(audio_path, ts):
    partitions = partition_audiofeature(audio_path)

    scene_audio = []
    for t in ts:
        temp_audio = [x[1] for x in partitions if t[0] <= x[0] <= t[4]]
        if len(temp_audio) != 0:
            print(len(temp_audio))

            scene_audio.append(np.mean(temp_audio))

    print(len(scene_audio))
    scene_audio = librosa.util.normalize(np.array(scene_audio))
    data = pd.DataFrame(scene_audio)
    print(data.describe())

    with open("test.csv", "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        # writer.writerow(["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", "Audio Level"])
        for i, t in enumerate(scene_audio):
            level = "nan"
            if t <= 0.25:
                level = "silent"
            elif 0.25 < t <= 0.5:
                level = "medium"
            elif 0.5 < t <= 0.75:
                level = "louder"
            elif t <= 1:
                level = "loudest"
            else:
                continue

            start = ts[i][0]
            end = ts[i][4]
            valence = ts[i][1]
            arousal = ts[i][2]
            dominance = ts[i][3]

            writer.writerow([start, end, valence, arousal, dominance, level])


def plot_from_csv():
    with open("audio_sent_blade_norm.csv") as csvfile:
        reader = csv.reader(csvfile)

        x1 = []
        x2 = []
        x3 = []
        y = []

        aro_silent = []
        aro_med = []
        aro_louder = []
        aro_loudest = []

        for row in reader:
            if row[0] != "Scene Start":
                x1.append(float(row[2]))
                x2.append(float(row[3]))
                x3.append(float(row[4]))

                if row[-1] == "silent":
                    y.append(1)
                    aro_silent.append(float(row[3]))
                elif row[-1] == "medium":
                    aro_med.append(float(row[3]))
                    y.append(2)
                elif row[-1] == "louder":
                    aro_louder.append(float(row[3]))
                    y.append(3)
                else:
                    y.append(4)
                    aro_loudest.append(float(row[3]))

    print("silent median: ", np.median(aro_silent))
    print("medium median: ", np.median(aro_med))
    print("louder median: ", np.median(aro_louder))
    print("loudest median: ", np.median(aro_loudest))

    plt.figure()
    plt.subplot(311)
    plt.scatter(x1, y)
    plt.xlabel("Valence")
    plt.ylabel("Audio level")

    plt.subplot(312)
    plt.scatter(x2, y)
    plt.xlabel("Arousal")
    plt.ylabel("Audio level")

    plt.subplot(313)
    plt.scatter(x3, y)
    plt.xlabel("Dominance")
    plt.ylabel("Audio level")
    plt.show()



def main():
    # script = os.path.join(BASE_DIR, "testfiles", "blade_manually.xml")
    # audio = os.path.join(BASE_DIR, "testfiles", "blade.wav")
    script = os.path.join(BASE_DIR, "testfiles", "star-wars-4_man.xml")
    audio = os.path.join(BASE_DIR, "testfiles", "star-wars-4.wav")
    # selfie_audio = os.path.join(BASE_DIR, "testfiles", "selfiefromhell.wav")

    # ts = scenesentiment_for_manually_annotated(script)
    # print(ts)
    # audio_scenes(audio, ts)
    plot_from_csv()

if __name__ == '__main__':
    main()
