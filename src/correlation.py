import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
from scipy import stats

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))

fountain1 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "blade.txt")
fountain2 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "hellboy.txt")
fountain3 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "predator.txt")
fountain4 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "scream.txt")
fountain5 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "star-wars-4.txt")
fountain6 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "the-matrix.txt")

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

script1 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "blade_man.xml")
script2 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "hellboy_man.xml")
script3 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "predator_man.xml")
script4 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "scream_man.xml")
script5 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "star-wars-4_man.xml")
script6 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "the-matrix_man.xml")

subs1 = os.path.join(BASE_DIR, "data/data_subtitles/", "blade_subs.xml")
subs2 = os.path.join(BASE_DIR, "data/data_subtitles/", "hellboy_subs.xml")
subs3 = os.path.join(BASE_DIR, "data/data_subtitles/", "predator_subs.xml")
subs4 = os.path.join(BASE_DIR, "data/data_subtitles/", "scream_subs.xml")
subs5 = os.path.join(BASE_DIR, "data/data_subtitles/", "star-wars-4_subs.xml")
subs6 = os.path.join(BASE_DIR, "data/data_subtitles/", "the-matrix_subs.xml")


def correlation(csv_path: str, x_variable: str, y_variable: str, raw=True):
    dataframe = pd.read_csv(csv_path)
    x = dataframe.get(x_variable).values
    y = dataframe.get(y_variable).values
    rho = stats.spearmanr(x, y)
    p = stats.pearsonr(x, y)
    tau = stats.kendalltau(x, y)

    return rho, p, tau, len(x)


def permutationtest(a, b, n_perm):
    rho = stats.spearmanr(a, b)
    print(rho)

    greater = 0
    less = 0
    i = 0
    while i < n_perm:
        if i > n_perm:
            break
        i += 1
        np.random.shuffle(a)
        test = stats.spearmanr(a, b)
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
    directory = os.path.join(BASE_DIR, "data/audiosentiment_csvfiles/single movies")

    # csvfile = os.path.join(directory, "7mv_audiosent_all.csv")
    # df = pd.read_csv(csvfile)
    # energy = df.get("Audio Energy").values
    # arousal = df.get("Arousal").values
    # valence = df.get("Valence").values
    # dominance = df.get("Dominance").values



    for file in os.listdir(directory):
        if file =="Warriner":
            continue
        csvfile = os.path.join(directory, file)
        print("\n",r"\textbf{"+file.replace("_audiosent_all.csv","")+"}","\n")
        indices = ["Valence", "Arousal", "Dominance"]#, "Vader neg", "Vader pos", "Vader compound"]
        # csvfile = os.path.join(BASE_DIR, "data/audiosent_csv_raw", csvfile)

        for i in indices:
            print(r"\textit{"+i+"}",r"\\")
            t = correlation(csvfile, i, "Audio Energy", raw=True)
            print("spearman: ", "%.3f" %t[0][0], r"\\","\np-value: ",t[0][1],r"\\")
            # print("pearson: ", t[1][0], "\np-value: ", t[1][1])
            print("kendall's tau: ", "%.3f" %t[2][0],r"\\", "\np-value: ", t[2][1],r"\\")
            print(r"\\")




if __name__ == '__main__':
    main()
