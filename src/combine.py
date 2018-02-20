"""Combines sentiment analysis and audio analysis"""

import csv
import os
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates
from src.src_audio.audio import get_energy
from src.src_text.sentiment.subs_sentiment import subtitle_sentiment
from src.src_text.sentiment.ms_sentiment import scenesentiment_for_man_annotated

"""Idee:
- scenes mit time codes aus moviescript get_full_scenes
- energy aus audio_analysis (noch nicht in Intervalle eingeteilt)
- nimm die time codes der Szenen um die energy aufzuteilen
- plotte beides über der gleichen Zeitachse
"""

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def sliding_window(inputlist: list, win_size: int):
    windows = []
    current_mean = []

    for index, score in enumerate(inputlist):
        if index + win_size <= len(inputlist):
            temp = inputlist[index:index + win_size]
            current_mean = np.mean(temp)
            windows.append(current_mean)
        else:
            temp = inputlist[index:]
            i = len(temp)
            while i < win_size:
                temp.append(current_mean)
                i += 1
            current_mean = np.mean(temp)
            windows.append(current_mean)

    return windows


def combine(audio_csv: str, xml_path: str, scenelevel=True):
    if scenelevel:
        sentiment = scenesentiment_for_man_annotated(xml_path, "Warriner")
    else:
        sentiment = subtitle_sentiment(xml_path)

    sent_time = [s[0] for s in sentiment]
    arousal = [s[2].get("arousal") for s in sentiment]
    print(len(sent_time))

    audio_tuples = []
    with open(audio_csv) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            audio_tuples.append((float(row[0]), float(row[1])))

    audio_time = [a[0] for a in audio_tuples]
    audio = [a[1] for a in audio_tuples]
    print("Audio time: ", audio_time[-1])
    print("sentiment time: ", sent_time[-1])

    audio_windows = sliding_window(audio, 10)

    if scenelevel:
        sentiment_windows = arousal
    else:
        sentiment_windows = sliding_window(arousal, 10)

    fig, ax1 = plt.subplots()
    # fig.set_canvas(plt.gcf().canvas)
    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Audio Energy', color=color)
    ax1.semilogy(audio_time, audio_windows, color=color)
    # ax1.plot(audio_time, audio_windows, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Arousal', color=color)  # we already handled the x-label with ax1
    ax2.plot(sent_time, sentiment_windows, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    # fig.tight_layout()
    # plt.figure()
    # plt.subplot(311)
    # plt.title('Blade: Audio (RMS Energy)')
    # plt.xlabel("seconds")
    # plt.semilogy(times, audio)
    # # plt.plot(times, audio)
    # plt.xlim(0, times[-1])
    #
    # plt.subplot(312)
    # # plt.title('Blade: Audio (RMS Energy)')
    # plt.xlabel("seconds")
    # plt.semilogy(times, audio_windows)
    # # plt.plot(times, audio_windows)
    #
    # plt.xlim(0, times[-1])
    #
    # plt.subplot(313)
    # plt.xlabel("seconds")
    # plt.plot(time, sentiment_windows)
    # plt.xlim(0, time[-1])

    # plt.tight_layout()
    plt.show()
    # img_path = os.path.basename(xml_path).replace(".xml", ".png")
    # fig.savefig(img_path, dpi=300, format="png")


def main():
    time = datetime.now()

    script1 = os.path.join(BASE_DIR, "manually_annotated", "blade_man.xml")
    script2 = os.path.join(BASE_DIR, "manually_annotated", "hellboy_man.xml")
    script3 = os.path.join(BASE_DIR, "manually_annotated", "predator_man.xml")
    script4 = os.path.join(BASE_DIR, "manually_annotated", "scream_man.xml")
    script5 = os.path.join(BASE_DIR, "manually_annotated", "star-wars-4_man.xml")

    subs1 = os.path.join(BASE_DIR, "data_subtitles/", "blade_subs.xml")
    subs2 = os.path.join(BASE_DIR, "data_subtitles/", "hellboy_subs.xml")
    subs3 = os.path.join(BASE_DIR, "data_subtitles/", "predator_subs.xml")
    subs4 = os.path.join(BASE_DIR, "data_subtitles/", "scream_subs.xml")
    subs5 = os.path.join(BASE_DIR, "data_subtitles/", "star-wars-4_subs.xml")

    audio1 = os.path.join(BASE_DIR, "audio_csvfiles", "blade.csv")
    audio2 = os.path.join(BASE_DIR, "audio_csvfiles", "hellboy.csv")
    audio3 = os.path.join(BASE_DIR, "audio_csvfiles", "predator.csv")
    audio4 = os.path.join(BASE_DIR, "audio_csvfiles", "scream_ger.csv")
    audio5 = os.path.join(BASE_DIR, "audio_csvfiles", "star-wars-4.csv")

    time2 = datetime.now()
    diff = time2 - time

    data = [(script1, audio1), (script2, audio2), (script3, audio3), (script4, audio4), (script5, audio5)]
    data2 = [(subs1, audio1), (subs2, audio2), (subs3, audio3), (subs4, audio4), (subs5, audio5)]

    for d in data:
        combine(d[1], d[0])

    for d in data2:
        combine(d[1], d[0], scenelevel=False)
    print(diff)


if __name__ == '__main__':
    main()
