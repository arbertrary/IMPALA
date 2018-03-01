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
import random
import soundfile as sf
import itertools
import librosa
import src.utility as util
from scipy import stats
from src.src_audio.audio import normalize, partition_audiofeature
from src.src_text.sentiment.ms_sentiment import scenesentiment_for_man_annotated, sentence_sentiment, \
    plaintext_sentiment
from src.src_text.sentiment.subs_sentiment import subtitle_sentiment
from src.src_text.sentiment.sentiment import ImpalaSent
from src.src_text.preprocessing.moviescript import get_scenes_unannotated

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))

fountain1 = os.path.join(BASE_DIR, "data/all_moviescripts", "blade.txt")
fountain2 = os.path.join(BASE_DIR, "data/all_moviescripts", "hellboy.txt")
fountain3 = os.path.join(BASE_DIR, "data/all_moviescripts", "predator.txt")
fountain4 = os.path.join(BASE_DIR, "data/all_moviescripts", "scream.txt")
fountain5 = os.path.join(BASE_DIR, "data/all_moviescripts", "star-wars-4.txt")
fountain6 = os.path.join(BASE_DIR, "data/all_moviescripts", "the-matrix.txt")

audio1 = os.path.join(BASE_DIR, "data/audio_csvfiles", "blade.csv")
audio2 = os.path.join(BASE_DIR, "data/audio_csvfiles", "hellboy.csv")
audio3 = os.path.join(BASE_DIR, "data/audio_csvfiles", "predator.csv")
audio4 = os.path.join(BASE_DIR, "data/audio_csvfiles", "scream_ger.csv")
audio5 = os.path.join(BASE_DIR, "data/audio_csvfiles", "star-wars-4.csv")
audio6 = os.path.join(BASE_DIR, "data/audio_csvfiles", "the-matrix.csv")

script1 = os.path.join(BASE_DIR, "data/manually_annotated", "blade_man.xml")
script2 = os.path.join(BASE_DIR, "data/manually_annotated", "hellboy_man.xml")
script3 = os.path.join(BASE_DIR, "data/manually_annotated", "predator_man.xml")
script4 = os.path.join(BASE_DIR, "data/manually_annotated", "scream_man.xml")
script5 = os.path.join(BASE_DIR, "data/manually_annotated", "star-wars-4_man.xml")
script6 = os.path.join(BASE_DIR, "data/manually_annotated", "the-matrix_man.xml")

subs1 = os.path.join(BASE_DIR, "data/data_subtitles/", "blade_subs.xml")
subs2 = os.path.join(BASE_DIR, "data/data_subtitles/", "hellboy_subs.xml")
subs3 = os.path.join(BASE_DIR, "data/data_subtitles/", "predator_subs.xml")
subs4 = os.path.join(BASE_DIR, "data/data_subtitles/", "scream_subs.xml")
subs5 = os.path.join(BASE_DIR, "data/data_subtitles/", "star-wars-4_subs.xml")
subs6 = os.path.join(BASE_DIR, "data/data_subtitles/", "the-matrix_subs.xml")


def audiosent_csv(script_path: str, audio_path: str, dest_csv_path: str, sent_method: str = "Warriner", **kwargs):
    if sent_method not in {"Warriner", "NRC", "Vader", "combined"}:
        raise ValueError("Incorrect sentiment method. Choose \"Warriner\" or \"NRC\"!")

    # ts = scenesentiment_for_man_annotated(script_path)
    # ts2 = scenesentiment_for_man_annotated(script_path, sent_method="Vader")
    ts = subtitle_sentiment(script_path, sent_method)
    print("warriner length", len(ts))
    partitions = []

    with open(audio_path) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            partitions.append((float(row[0]), float(row[1])))

    scene_audio = []
    scene_sentiment = []
    scene_sentiment2 = []
    for index, t in enumerate(ts):
        temp_audio = [x[1] for x in partitions if t[0] <= x[0] <= t[1]]

        if len(temp_audio) != 0:
            scene_audio.append(np.mean(temp_audio))
            scene_sentiment.append(t)
            # scene_sentiment2.append(ts2[index])

    print(len(ts), len(scene_sentiment))
    # print(len(ts2), len(scene_sentiment2))

    if kwargs.get("normalized"):
        scene_audio = librosa.util.normalize(np.array(scene_audio))

    if not os.path.isfile(dest_csv_path):
        mode = "w"
    elif os.stat(dest_csv_path).st_size == 0:
        mode = "w"
    else:
        mode = "a"

    with open(dest_csv_path, mode) as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        if mode == "w":
            if sent_method == "Warriner":
                writer.writerow(["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", "Audio Level"])
            elif sent_method == "NRC":
                writer.writerow(
                    ["Scene Start", "Scene End", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Negative",
                     "Positive", "Sadness", "Surprise", "Trust", "Audio Level"])
            elif sent_method == "Vader":
                writer.writerow(["Scene Start", "Scene End", "neg", "neu", "pos", "compound", "Audio Level"])
            elif sent_method == "combined":
                writer.writerow(
                    ["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", "Vader neg", "Vader neu",
                     "Vader pos", "Vader compound",
                     "Audio Level"])

        for i, t in enumerate(scene_audio):
            level = t
            start = scene_sentiment[i][0]
            end = scene_sentiment[i][1]
            score = scene_sentiment[i][2]
            # score2 = scene_sentiment2[i][2]
            score2 = None

            if sent_method == "Warriner":
                writer.writerow([start, end, score.get("valence"), score.get("arousal"), score.get("dominance"), level])
            elif sent_method == "NRC":
                writer.writerow(
                    [start, end, score.get("anger"), score.get("anticipation"), score.get("disgust"), score.get("fear"),
                     score.get("joy"),
                     score.get("negative"), score.get("positive"), score.get("sadness"), score.get("surprise"),
                     score.get("trust"), level])
            elif sent_method == "Vader":
                writer.writerow(
                    [start, end, score.get("neg"), score.get("neu"), score.get("pos"), score.get("compound"), level])
            elif sent_method == "combined":
                writer.writerow(
                    [start, end, score.get("valence"), score.get("arousal"), score.get("dominance"), score2.get("neg"),
                     score2.get("neu"), score2.get("pos"), score2.get("compound"), level])


def fountain_audiosent_csv(fountain_script: str, audio_path: str, n_sections: int, dest_path: str,
                           sent_method: str = "Warriner"):
    sent_sections = plaintext_sentiment(fountain_script, n_sections)

    audio = []
    with open(audio_path) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            audio.append(float(row[1]))

        la = len(audio)
        # audiosection_length = int(la / n_sections)
        # partitions = [np.mean(x) for x in util.part(audio, audiosection_length)]
        partitions = [np.mean(x) for x in util.split(audio, n_sections)]

    # sent = sent_sections[0:n_sections]
    # partitions = partitions[0:n_sections]

    with open(dest_path, "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        for index, item in enumerate(sent_sections):
            writer.writerow([item.get("valence"), item.get("arousal"), item.get("dominance"), partitions[index]])


def audiosent_scenes_wo_time(xml_path: str, audio_path: str, dest_path: str):
    sentiment = ImpalaSent()

    scenes = get_scenes_unannotated(xml_path)
    scenesentiment = [sentiment.score(" ".join(x)) for x in scenes]

    audio = []
    with open(audio_path) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            audio.append(float(row[1]))

        la = len(audio)
        # audiosection_length = int(la / len(scenes))
        partitions = [np.mean(x) for x in util.split(audio, len(scenes))]

    # scenesentiment = scenesentiment[0:len(scenes)]
    # partitions = partitions[0:len(scenes)]

    with open(dest_path, "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        for index, item in enumerate(scenesentiment):
            writer.writerow([item.get("valence"), item.get("arousal"), item.get("dominance"), partitions[index]])

    # rho = stats.spearmanr(scenesentiment, partitions)
    # p = stats.pearsonr(scenesentiment, partitions)
    # tau = stats.kendalltau(scenesentiment, partitions)


def correlation(csv_path: str, column: int, raw=True):
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)

        sentiment = []
        audio = []

        for row in reader:
            if row[0] != "Scene Start":
                if row[2] == "nan":
                    continue

                sentiment.append(float(row[column]))

                if raw:
                    audio.append(float(row[-1]))
                else:
                    if row[-1] == "silent":
                        audio.append(1)
                    elif row[-1] == "medium":
                        audio.append(2)
                    elif row[-1] == "loud":
                        audio.append(3)
                    else:
                        audio.append(4)

        # rho = stats.mstats.spearmanr(sentiment, audio)
        rho = stats.spearmanr(sentiment, audio)
        # p = stats.mstats.pearsonr(sentiment, audio)
        p = stats.pearsonr(sentiment, audio)
        # print(p)
        # tau = stats.mstats.kendalltau(sentiment, audio)
        tau = stats.kendalltau(sentiment, audio)
        # print("spearman: ", rho)
        # print("pearson: ", p)
        # print("kendall's tau: ", tau, "\n")

        # permutationtest(sentiment, audio, 100000)

        return rho, p, tau, len(sentiment)


def permutationtest(a, b, n_perm):
    rho = stats.spearmanr(a, b)

    greater = 0
    less = 0
    i = 0
    # while i < n_perm:
    for perm in itertools.permutations(a):
        if i > n_perm:
            break
        i += 1
        # np.random.shuffle(a)
        test = stats.spearmanr(perm, b)
        if test[0] >= rho[0]:
            greater += 1
        else:
            less += 1
    print("korrelation größer gleich tau: ", greater / n_perm)
    print("korrelation kleiner tau: ", less / n_perm)


def plot_from_csv(csv_path: str, classes: int):
    with open(csv_path) as csvfile:

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
            if row[0] != "Scene Start":
                if row[3] == "nan":
                    continue
                x1.append(float(row[2]))
                x2.append(float(row[3]))
                x3.append(float(row[4]))

                i = 2

                if row[-1] == "silent":
                    y.append(1)
                    aro_silent.append(float(row[i]))
                elif row[-1] == "medium":
                    aro_med.append(float(row[i]))
                    y.append(2)
                elif row[-1] == "loud":
                    aro_loud.append(float(row[i]))
                    y.append(3)
                else:
                    y.append(4)
                    aro_loudest.append(float(row[i]))

    print("silent median: ", np.median(aro_silent), len(aro_silent))
    print("medium median: ", np.median(aro_med), len(aro_med))
    print("loud median: ", np.median(aro_loud), len(aro_loud))
    print("loudest median: ", np.median(aro_loudest), len(aro_loudest))

    if classes == 3:
        x = [aro_silent, aro_med, aro_loud]
    else:
        x = [aro_silent, aro_med, aro_loud, aro_loudest]

    name = os.path.basename(csv_path).split("_")[0]
    plt.suptitle("Max arousal, Max audio energy of " + name)
    plt.boxplot(x, vert=False, showmeans=True, meanline=True)
    # plt.scatter(x2,y)
    plt.ylabel("Audio Level (" + str(classes) + " = highest)")
    plt.xlabel("Arousal")
    # plt.tight_layout()
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
    # img_path = csv_path.replace(".csv", ".png")
    # plt.savefig(img_path, dpi=300)


def main2():
    data = [(fountain1, audio1), (fountain2, audio2), (fountain3, audio3), (fountain4, audio4), (fountain5, audio5),
            (fountain6, audio6)]
    data2 = [(script1, audio1), (script2, audio2), (script3, audio3), (script4, audio4), (script5, audio5),
             (script6, audio6)]

    data3 = [(subs1, audio1), (subs2, audio2), (subs3, audio3), (subs4, audio4), (subs5, audio5), (subs6, audio6)]

    for d in data:
        fountain_audiosent_csv(d[0], d[1], 200, "test2.csv")
    # audiosent_scenes_wo_time(d[0], d[1])
    # audiosent_csv(d[0], d[1], "test4.csv")

    indices = [0, 1, 2]
    for i in indices:
        test = []
        if i == 0:
            print("Valence")
        elif i == 1:
            print("Arousal")
        else:
            print("Dominance")

        test.append(correlation("test2.csv", i, raw=True))
        test.sort(key=lambda x: x[1])

        for t in test:
            print("spearman: ", t[0][0], "\np-value: ", t[0][1])
            # print("pearson: ", t[1][0], "\np-value: ", t[1][1])
            print("kendall's tau: ", t[2][0], "\np-value: ", t[2][1], "\n")


def main():
    data = [(script1, audio1), (script2, audio2), (script3, audio3), (script4, audio4), (script5, audio5),
            (script6, audio6)]
    data2 = [(subs1, audio1), (subs2, audio2), (subs3, audio3), (subs4, audio4), (subs5, audio5), (subs6, audio6)]

    name = "test3.csv"
    # for d in data2:
    #     audiosent_csv(d[0], d[1], name, normalized=True)
    #     audiosent_scenes_wo_time(d[0], d[1], name)

    # csvfile = os.path.join(BASE_DIR, "data/audiosent_csv_raw/6mv_mean_audio_raw_combined_sent.csv")
    test = []
    test.append(correlation(name, 3, raw=True))
    test.sort(key=lambda x: x[1])
    for t in test:
        print("spearman: ", t[0][0], "\np-value: ", t[0][1])
        # print("pearson: ", t[1][0], "\np-value: ", t[1][1])
        print("kendall's tau: ", t[2][0], "\np-value: ", t[2][1], "\n")

    test = []

    # for file in os.listdir(os.path.join(BASE_DIR, "data/audiosent_csv_raw/single_movies")):
    #     path = os.path.join(BASE_DIR, "data/audiosent_csv_raw/single_movies", file)

    # if "6mv" in path:
    # if "Vader" in path:
    #     if "Vader" in path:
    #         ind = [2, 3, 4, 5]
    #         names = ["Scene Start", "Scene End", "neg", "neu", "pos", "compound", "Audio Level"]
    #     else:
    #         ind = [2, 3, 4]
    #         names = ["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", "Audio Level"]
    #
    #     for i in ind:
    #         corr = correlation(path, i, raw=True)
    #         test.append((corr, path, names[i]))

    # if "Warriner" in path:
    #     print(file)
    #     corr = correlation(path, 3, raw=True)

    # for t in test:
    #     print("---", os.path.basename(t[1]), "---")
    #     print(t[2])
    #     # print("sample size: ", t[0][-1])
    #     print("spearman: ", t[0][0][0], "\np-value: ", t[0][0][1])
    #     # print("pearson: ", t[0][1][0], "\np-value: ", t[0][1][1])
    #     print("kendall's tau: ", t[0][2][0], "\np-value: ", t[0][2][1], "\n")


if __name__ == '__main__':
    main()
