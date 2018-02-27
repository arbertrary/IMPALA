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

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def create_audio_sent_csv(script_path: str, audio_path: str, dest_csv_path: str, sent_method: str = "Warriner"):
    if sent_method not in {"Warriner", "NRC", "Vader"}:
        raise ValueError("Incorrect sentiment method. Choose \"Warriner\" or \"NRC\"!")

    ts = scenesentiment_for_man_annotated(script_path, sent_method)
    print("warriner lengtht", len(ts))
    ts2 = scenesentiment_for_man_annotated(script_path, sent_method="Vader")
    print("vader length:", len(ts2))
    # ts = subtitle_sentiment(script_path, sent_method)
    partitions = []

    with open(audio_path) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            partitions.append((float(row[0]), float(row[1])))

    scene_audio = []
    scene_sentiment = []
    for t in ts:
        temp_audio = [x[1] for x in partitions if t[0] <= x[0] <= t[1]]

        if len(temp_audio) != 0:
            # Variante 1: avg über die gesamte szene
            scene_audio.append(np.mean(temp_audio))
            scene_sentiment.append(t)
            # variante 2: max der gesamten szene
            # scene_audio.append(np.max(temp_audio))

            # variante 3: average des 75% percentile
            # perc = np.percentile(temp_audio, 75)
            # temp = [x for x in temp_audio if x > perc]
            # scene_audio.append(np.mean(temp))

            # variante 4: min der gesamten szene
            # scene_audio.append(np.min(temp_audio))
    # scene_audio = librosa.util.normalize(np.array(scene_audio))
    # scene_audio = normalize(scene_audio)
    data = pd.DataFrame(scene_audio)
    # print(data.describe())

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
        for i, t in enumerate(scene_audio):

            level = t
            # level = "nan"
            # if t <= 1:
            #     level = "silent"
            # elif 1 < t <= 2:
            #     level = "medium"
            # elif 2 < t <= 3:
            #     level = "loud"
            # else:
            #     level = "loud"

            # if t <= 0.33:
            #     level = "silent"
            # elif 0.33 < t <= 0.66:
            #     level = "medium"
            # else:
            #     level = "loud"

            # if t <= 0.25:
            #     level = "silent"
            # elif 0.25 < t <= 0.5:
            #     level = "medium"
            # elif 0.5 < t <= 0.75:
            #     level = "loud"
            # else:
            #     level = "loudest"

            start = scene_sentiment[i][0]
            end = scene_sentiment[i][1]
            score = scene_sentiment[i][2]

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


def correlation_plaintext(fountain_script: str, audio_path: str, n_sections: int, sent_method: str = "Warriner"):
    sent_sections = plaintext_sentiment(fountain_script, n_sections)

    audio = []
    with open(audio_path) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            audio.append(float(row[1]))

        la = len(audio)
        audiosection_length = int(la / n_sections)
        partitions = [np.mean(x) for x in util.part(audio, audiosection_length)]

    sent = sent_sections[0:n_sections]
    partitions = partitions[0:n_sections]

    with open("test.csv", "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        for index, item in enumerate(sent):
            writer.writerow([item.get("valence"), item.get("arousal"), item.get("dominance"), partitions[index]])

    # rho = stats.spearmanr(sent, partitions)
    # tau = stats.kendalltau(sent, partitions)

    # i = 0
    # n = 10000
    # greater = 0
    # less = 0
    # for index, p in enumerate(itertools.permutations(sent)):
    #     if index > n:
    #         break
    #
    #     # shuffled = np.random.shuffle(sent)
    #     # test = stats.spearmanr(shuffled, partitions)
    #     test = stats.spearmanr(p, partitions)
    #     if test[0] >= rho[0]:
    #         greater += 1
    #     else:
    #         less += 1
    #
    # print("korrelation größer gleich rho: ", greater/n)
    # print("korrelation kleiner rho: ", less/n)

    # print("Arousal")
    # print("spearman: ", rho[0])
    # print("p-value: ", rho[1])
    # print("kendall's tau: ", tau[0])
    # print("p-value: ", tau[1])


def correlation(csv_path: str, column: int, raw=False):
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)

        sentiment = []
        audio = []

        for row in reader:
            if row[0] != "Scene Start":
                if row[2] == "nan":
                    continue

                # sentiment.append(float("%.3f"%(float(row[3]))))
                sentiment.append(float(row[column]))

                if raw:
                    # audio.append(float("%.3f"%(float(row[-1]))))
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

        # plt.suptitle("Histogram: Distribution of Arousal and Audio Energy of 5 movies")
        # plt.subplot(211)
        # plt.hist(sentiment)
        # plt.ylabel("Number of Data Points")
        # plt.xlabel("Arousal")
        # plt.subplot(212)
        # plt.hist(audio)
        # plt.ylabel("Number of Data Points")
        # plt.xlabel("Audio Energy")
        # plt.show()
        # random.shuffle(sentiment)
        # random.shuffle(audio)

        # print(csv_path)
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
        # n = 10000
        #
        # greater = 0
        # less = 0
        # for index, p in enumerate(itertools.permutations(sentiment)):
        #     if index > n:
        #         break
        #
        #     # shuffled = np.random.shuffle(sent)
        #     # test = stats.spearmanr(shuffled, partitions)
        #     test = stats.spearmanr(p, audio)
        #     if test[0] >= rho[0]:
        #         greater += 1
        #     else:
        #         less += 1
        # print("korrelation größer gleich rho: ", greater / n)
        # print("korrelation kleiner rho: ", less / n)
        return rho, p, tau, len(sentiment)


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
    script1 = os.path.join(BASE_DIR, "data/all_moviescripts", "blade.txt")
    script2 = os.path.join(BASE_DIR, "data/all_moviescripts", "hellboy.txt")
    script3 = os.path.join(BASE_DIR, "data/all_moviescripts", "predator.txt")
    script4 = os.path.join(BASE_DIR, "data/all_moviescripts", "scream.txt")
    script5 = os.path.join(BASE_DIR, "data/all_moviescripts", "star-wars-4.txt")
    script6 = os.path.join(BASE_DIR, "data/all_moviescripts", "the-matrix.txt")

    audio1 = os.path.join(BASE_DIR, "data/audio_csvfiles", "blade.csv")
    audio2 = os.path.join(BASE_DIR, "data/audio_csvfiles", "hellboy.csv")
    audio3 = os.path.join(BASE_DIR, "data/audio_csvfiles", "predator.csv")
    audio4 = os.path.join(BASE_DIR, "data/audio_csvfiles", "scream_ger.csv")
    audio5 = os.path.join(BASE_DIR, "data/audio_csvfiles", "star-wars-4.csv")
    audio6 = os.path.join(BASE_DIR, "data/audio_csvfiles", "the-matrix.csv")

    data = [(script1, audio1), (script2, audio2), (script3, audio3), (script4, audio4), (script5, audio5),
            (script6, audio6)]

    # for d in data:
    #     correlation_plaintext(d[0], d[1], 170, "Warriner")

    test = []
    test.append(correlation("test.csv", 2, raw=True))
    test.sort(key=lambda x: x[1])
    for t in test:
        print("spearman: ", t[0][0], "\np-value: ", t[0][1])
        print("pearson: ", t[1][0], "\np-value: ", t[1][1])
        print("kendall's tau: ", t[2][0], "\np-value: ", t[2][1], "\n")


def main():
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

    audio1 = os.path.join(BASE_DIR, "data/audio_csvfiles", "blade.csv")
    audio2 = os.path.join(BASE_DIR, "data/audio_csvfiles", "hellboy.csv")
    audio3 = os.path.join(BASE_DIR, "data/audio_csvfiles", "predator.csv")
    audio4 = os.path.join(BASE_DIR, "data/audio_csvfiles", "scream_ger.csv")
    audio5 = os.path.join(BASE_DIR, "data/audio_csvfiles", "star-wars-4.csv")
    audio6 = os.path.join(BASE_DIR, "data/audio_csvfiles", "the-matrix.csv")

    data = [(script1, audio1), (script2, audio2), (script3, audio3), (script4, audio4), (script5, audio5),
            (script6, audio6)]
    data2 = [(subs1, audio1), (subs2, audio2), (subs3, audio3), (subs4, audio4), (subs5, audio5), (subs6, audio6)]

    name = "6mv_raw_Warriner_unnorm.csv"
    # for d in data:
    # name = os.path.basename(d[1]).replace(".csv", "_raw_mean_audio_Warriner.csv")
    # create_audio_sent_csv(d[0], d[1], name, sent_method="Warriner")
    # path = d[1].replace(".csv", "_test.csv")
    # create_audio_sent_csv(d[1], d[0], dest_csv_path=path, sent_method="Warriner")

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

    test = []
    test.append(correlation(name, 2, raw=True))
    test.sort(key=lambda x: x[1])
    for t in test:
        print("spearman: ", t[0][0], "\np-value: ", t[0][1])
        print("pearson: ", t[1][0], "\np-value: ", t[1][1])
        print("kendall's tau: ", t[2][0], "\np-value: ", t[2][1], "\n")


if __name__ == '__main__':
    main2()
