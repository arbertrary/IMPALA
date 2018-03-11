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
import itertools
from scipy import stats

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

tuning1 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "blade_tuning.csv")
tuning2 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "hellboy_tuning.csv")
tuning3 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "predator_tuning.csv")
tuning4 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "scream_ger_tuning.csv")
tuning5 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "star-wars-4_tuning.csv")
tuning6 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "the-matrix_tuning.csv")

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


def correlation(csv_path: str, column: int, raw=True):
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)

        sentiment = []
        audio = []

        for row in reader:
            if row[0] != "Scene Start":
                if row[column] == "nan":
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
        # print(sentiment)
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


def main():
    # csvfile = "7mv_audiosent_Warriner.csv"
    # csvfile = "7mv_audiosent_normalized_Warriner.csv"
    # csvfile = "7mv_fountain_audiosent.csv"
    # csvfile = "7mv_audiosent_subs_Warriner.csv"
    csvfile = "7mv_audiosent_ohne_StarWars.csv"

    # csvfile = "7mv_audiosent_Vader.csv"
    # csvfile = "7mv_audiosent_normalized_Vader.csv"
    # csvfile = "7mv_audiosent_scenes_wo_time_Warriner.csv"
    # csvfile = "7mv_audiosent_tuning_Warriner.csv"
    # csvfile = "7mv_audiosent_centroid_Warriner.csv"
    test = []
    indices = [2, 3, 4]
    # indices = [0,1,2]
    # indices = [2,3,4,5]
    # csvfile = os.path.join(BASE_DIR, "data/audiosent_csv_raw", csvfile)
    for i in indices:
        test.append(correlation(csvfile, i, raw=True))
    # test.sort(key=lambda x: x[1])

    for i, t in enumerate(test):
        if i == 0:
            print("Valence")
            # print("neg")
        elif i == 1:
            print("Arousal")
            # print("neu")
        elif i ==2:
            # print("pos")
            print("Dominance")
        else:
            print("compound")

        print("spearman: ", t[0][0], "\np-value: ", t[0][1])
        # print("pearson: ", t[1][0], "\np-value: ", t[1][1])
        print("kendall's tau: ", t[2][0], "\np-value: ", t[2][1], "\n")

    # test = []
    # for file in os.listdir(os.path.join(BASE_DIR, "src/testfiles")):
    #     path = os.path.join(BASE_DIR, "src/testfiles", file)
    #     ind = [0, 1, 2]
    #     names = ["Valence", "Arousal", "Dominance"]
    #
    #     if ".csv" in path:
    #         for i in ind:
    #             corr = correlation(path, i, raw=True)
    #             test.append((corr, path, names[i]))
    #
    # for t in test:
    #     print("---", os.path.basename(t[1]), "---")
    #     print(t[2])
    #     # print("sample size: ", t[0][-1])
    #     print("spearman: ", t[0][0][0], "\np-value: ", t[0][0][1])
    #     # print("pearson: ", t[0][1][0], "\np-value: ", t[0][1][1])
    #     print("kendall's tau: ", t[0][2][0], "\np-value: ", t[0][2][1], "\n")


if __name__ == '__main__':
    main()
