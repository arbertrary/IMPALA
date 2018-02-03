import os
import csv
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from audio_analysis import partition_audiofeature
from subs_sentiment import get_subs_sentiment

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def sentiment_and_energy(audio_path: str, subtitle_path: str):
    # separate audio energy in partitions of 1 s
    energy = partition_audiofeature(audio_path, 1.0)
    arousal, valence = get_subs_sentiment(subtitle_path)

    energy_plot = []
    arousal_plot = []
    valence_plot = []

    for index, s in enumerate(arousal):
        if energy.get(str(s[0])):
            audio = energy.get(str(s[0]))
            energy_plot.append(audio)
            arousal_plot.append(s[1])
            valence_plot.append(valence[index][1])

    plt.figure()
    plt.subplot(211)
    plt.scatter(arousal_plot, energy_plot)
    plt.xlabel("Arousal")
    plt.ylabel("Audio Energy")
    # plt.show()
    plt.subplot(212)
    plt.scatter(valence_plot, energy_plot)
    plt.xlabel("Valence")
    plt.ylabel("Audio Energy")


def plot_from_csv():

    with open("audio_sent.csv") as csvfile:
        reader = csv.reader(csvfile)

        x1 = []
        x2 = []
        y =[]
        for row in reader:
            if row[0] != "Scene Start":
                x1.append(float(row[2]))
                x2.append(float(row[3]))

                if row[4] == "silent":
                    y.append(1)
                elif row[4] == "medium":
                    y.append(2)
                elif row[4] == "louder":
                    y.append(3)
                else:
                    y.append(4)

    plt.figure()
    plt.subplot(211)
    plt.scatter(x1, y)
    plt.xlim(4.5,)
    plt.xlabel("Valence")
    plt.ylabel("Audio level")

    plt.subplot(212)
    plt.scatter(x2, y)
    plt.xlim(3.10,)
    plt.xlabel("Arousal")
    plt.ylabel("Audio level")




def main():
    subs = os.path.join(BASE_DIR, "src/testfiles/", "blade_subs.xml")
    audio = os.path.join(BASE_DIR, "src/testfiles/" "blade.wav")
    # selfie_audio = os.path.join(BASE_DIR, "src/testfiles/" "selfiefromhell.wav")
    # subs = os.path.join(BASE_DIR, "src/testfiles", "blade-trinity_subs.xml")
    time = datetime.now()

    # sentiment_and_energy(audio, subs)
    plot_from_csv()
    time2 = datetime.now()
    diff = time2 - time

    print(diff)
    plt.show()


if __name__ == '__main__':
    main()
