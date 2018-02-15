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


def combine(scenes, energy, duration):
    """
    :param scenes = list of scenes + their timecodes\n
    :param energy = np.array of RMS energy of the audio file\n
    :param duration = duration of the audio
    """
    intervals = np.array_split(energy, len(energy) / 100)
    intervals = [np.mean(e) for e in intervals]

    block_duration = np.divide(duration, len(intervals))
    en_times = []
    time = 0
    i = 1
    while i <= len(intervals):
        en_times.append(time)
        time += block_duration
        i += 1

    arousal_values = get_arousal_values(scenes)
    x = []
    i = 0
    for s in scenes:
        l = len(s[1])
        i += l
        x.append(i)

    times = [a[0] for a in arousal_values]
    scores = [a[1] for a in arousal_values]
    times = dates.date2num(times)

    plt.figure()
    plt.subplot(211)
    plt.title("Blade: Audio (RMS Energy)")
    plt.xlabel("seconds")

    plt.semilogy(en_times, intervals, color="b", label="RMS Energy")
    plt.legend(loc='best')

    plt.xlim(0, en_times[-1])

    plt.subplot(212)
    # plt.title("Hellraiser: Sentiment (Arousal Scores)")
    plt.title("Blade: Sentiment (Arousal Scores)")
    plt.ylabel("Arousal")
    plt.xlabel("time")
    plt.plot_date(times, scores, fmt="-", color="b", label="Arousal")
    plt.legend(loc='best')
    plt.xlim(times[0], times[-1])
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    # plt.subplot(313)
    # plt.plot(x, arousal_values_wo_time)
    # plt.ylabel("Arousal")
    # plt.xlabel("Scenes in Abh. ihrer Länge")
    # plt.xlim(x[0], x[-1])

    plt.tight_layout()

    plt.show()


def sliding_window(inputlist: list, win_size: int):
    windows = []
    for index, score in enumerate(inputlist):
        if index + win_size <= len(inputlist):
            temp = inputlist[index:index + win_size]
            windows.append(np.mean(temp))
        else:
            temp = inputlist[index:]
            windows.append(np.mean(temp))

    return windows


def combine_subs(audio_csv: str, subs_path: str):
    # sentiment = subtitle_sentiment(subs_path)
    sentiment = scenesentiment_for_man_annotated(subs_path, "Warriner")

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
    # sentiment_windows = sliding_window(arousal, 20)
    sentiment_windows = arousal
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Audio Energy', color=color)
    # ax1.semilogy(times, audio_windows, color=color)
    ax1.plot(audio_time, audio_windows, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Arousal', color=color)  # we already handled the x-label with ax1
    ax2.plot(sent_time, sentiment_windows, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
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


def main():
    time = datetime.now()

    script1 = os.path.join(BASE_DIR, "manually_annotated", "blade_man.xml")
    script2 = os.path.join(BASE_DIR, "manually_annotated", "star-wars-4_man.xml")
    script3 = os.path.join(BASE_DIR, "manually_annotated", "scream_man.xml")
    script4 = os.path.join(BASE_DIR, "manually_annotated", "hellboy_man.xml")
    script5 = os.path.join(BASE_DIR, "manually_annotated", "predator_man.xml")

    subs1 = os.path.join(BASE_DIR, "data_subtitles/", "hellboy_subs.xml")
    subs2 = os.path.join(BASE_DIR, "data_subtitles/", "blade_subs.xml")
    subs3 = os.path.join(BASE_DIR, "data_subtitles/", "star-wars-4_subs.xml")
    subs4 = os.path.join(BASE_DIR, "data_subtitles/", "scream_subs.xml")
    subs5 = os.path.join(BASE_DIR, "data_subtitles/", "predator_subs.xml")

    audio1 = os.path.join(BASE_DIR, "audio_csvfiles", "blade.csv")
    audio2 = os.path.join(BASE_DIR, "audio_csvfiles", "star-wars-4.csv")
    audio3 = os.path.join(BASE_DIR, "audio_csvfiles", "scream_ger.csv")
    audio4 = os.path.join(BASE_DIR, "audio_csvfiles", "hellboy.csv")
    audio5 = os.path.join(BASE_DIR, "audio_csvfiles", "predator.csv")


    time2 = datetime.now()
    diff = time2 - time

    combine_subs(audio2, script2)
    print(diff)


if __name__ == '__main__':
    main()
