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
from audio import partition_audiofeature, normalize

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def audio_scenes(audio_path, ts):
    partitions = partition_audiofeature(audio_path)

    scene_audio = []
    for t in ts:
        temp_audio = [x[1] for x in partitions if t[0] <= x[0] <= t[4]]
        if len(temp_audio) != 0:
            scene_audio.append(np.mean(temp_audio))

    print(len(scene_audio))
    # scene_audio = librosa.util.normalize(np.array(scene_audio))
    scene_audio = normalize(scene_audio)
    max_audio = np.max(scene_audio)
    data = pd.DataFrame(scene_audio)
    # print(data.describe(percentiles=[.33,.66]))

    with open("test.csv", "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        # writer.writerow(["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", "Audio Level"])
        for i, t in enumerate(scene_audio):
            level = "nan"
            # if t <= 0.25*max_audio:
            #     level = "silent"
            # elif 0.25*max_audio < t <= 0.50*max_audio:
            #     level = "medium"
            # elif 0.5*max_audio < t <= 0.75*max_audio:
            #     level = "loud"
            # else:
            #     level = "loudest"

            if t <= 1:
                level = "silent"
            elif 1 < t <= 2:
                level = "medium"
            elif 2 < t <= 3:
                level = "loud"
            else:
                level = "loudest"

            start = ts[i][0]
            end = ts[i][4]
            valence = ts[i][1]
            arousal = ts[i][2]
            dominance = ts[i][3]

            writer.writerow([start, end, valence, arousal, dominance, level])


def plot_from_csv():
    with open("5mv_audioclasses_abs(kleiner1, kleiner2...).csv") as csvfile:
        reader = csv.reader(csvfile)

        x1 = []
        x2 = []
        x3 = []
        y = []

        aro_silent = []
        aro_med = []
        aro_loud = []
        aro_loudest = []

        for row in reader:
            if row[0] != "Start":
                x1.append(float(row[2]))
                x2.append(float(row[3]))
                x3.append(float(row[4]))

                if row[-1] == "silent":
                    y.append(1)
                    aro_silent.append(float(row[3]))
                elif row[-1] == "medium":
                    aro_med.append(float(row[3]))
                    y.append(2)
                elif row[-1] == "loud":
                    aro_loud.append(float(row[3]))
                    y.append(3)
                else:
                    y.append(4)
                    aro_loudest.append(float(row[3]))

    print("silent median: ", np.median(aro_silent), len(aro_silent))
    print("medium median: ", np.median(aro_med), len(aro_med))
    print("loud median: ", np.median(aro_loud), len(aro_loud))
    print("loudest median: ", np.median(aro_loudest), len(aro_loudest))
    x = [aro_silent, aro_med, aro_loud, aro_loudest]

    plt.suptitle("Audiolevels and Arousal for 5 movies.")
    plt.boxplot(x, sym="", vert=False, showmeans=True, meanline=True)
    # plt.scatter(x2,y)
    plt.ylabel("Audio Level (4 = highest)")
    plt.xlabel("Arousal")
    plt.tight_layout()
    # plt.figure()
    # plt.subplot(311)
    # plt.scatter(x1, y)
    # plt.xlabel("Valence")
    # plt.ylabel("Audio level")
    #
    # plt.subplot(312)
    # # plt.scatter(x2, y)
    # plt.boxplot(x2)
    # plt.xlabel("Arousal")
    # plt.ylabel("Audio level")
    #
    # plt.subplot(313)
    # plt.scatter(x3, y)
    # plt.xlabel("Dominance")
    # plt.ylabel("Audio level")
    plt.show()



def main():
    script1 = os.path.join(BASE_DIR, "manually_annotated", "blade_man.xml")
    audio1 = os.path.join(BASE_DIR, "data_audio", "blade.wav")
    script2 = os.path.join(BASE_DIR, "manually_annotated", "star-wars-4_man.xml")
    audio2 = os.path.join(BASE_DIR, "data_audio", "star-wars-4.wav")
    script3 = os.path.join(BASE_DIR, "manually_annotated", "scream_man.xml")
    audio3 = os.path.join(BASE_DIR, "data_audio", "scream_ger.wav")
    script4 = os.path.join(BASE_DIR, "manually_annotated", "hellboy_man.xml")
    audio4 = os.path.join(BASE_DIR, "data_audio", "hellboy.wav")
    script5 = os.path.join(BASE_DIR, "manually_annotated", "predator_man.xml")
    audio5 = os.path.join(BASE_DIR, "data_audio", "predator.wav")

    data = [(script1, audio1),(script2, audio2),(script3, audio3),(script4, audio4),(script5, audio5),]

    # for d in data:
    #     ts = scenesentiment_for_manually_annotated(d[0])
    #     audio_scenes(d[1], ts)
    # ts = scenesentiment_for_manually_annotated(script)
    # print(ts)
    # audio_scenes(audio, ts)
    plot_from_csv()

if __name__ == '__main__':
    main()
