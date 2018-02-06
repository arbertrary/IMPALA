"""Combines sentiment analysis and audio analysis"""

import os
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates
from audio_analysis import get_energy
from subs_sentiment import get_subs_sentiment

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


def combine_subs(subtitle_scores, subtitle_times, energy, duration):
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

    plt.figure()
    plt.subplot(211)
    plt.title('Blade: Audio (RMS Energy)')
    # plt.title("Star Wars IV: Audio (RMS Energy)")
    plt.xlabel("seconds")

    plt.semilogy(en_times, intervals, color="b", label="RMS Energy")
    plt.legend(loc='best')

    plt.xlim(0, en_times[-1])

    plt.subplot(212)
    plt.title("Blade: Subtitle Sentiment (Valence Scores)")
    plt.ylabel("Arousal")
    plt.xlabel("seconds")

    # plt.plot_date(subtitle_times, subtitle_scores, fmt="-", color="b", label="Arousal")
    # plt.legend(loc='best')
    plt.plot(subtitle_times, subtitle_scores)
    plt.xlim(subtitle_times[0], subtitle_times[-1])
    # plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    # plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.tight_layout()
    plt.show()


def main():
    time = datetime.now()

    # scenes = get_full_scenes(os.path.join(BASE_DIR, "src/testfiles/" "blade_manually.xml"))
    energy = get_energy(os.path.join(BASE_DIR, "src/testfiles/" "blade.wav"))
    duration = sf.info(os.path.join(BASE_DIR, "src/testfiles/" "blade.wav")).duration
    # scenes = get_full_scenes(os.path.join(DATA_DIR, "star-wars-4_annotated.xml"))
    # energy = get_energy(os.path.join(DATA_DIR, "star-wars-4.wav"))
    # duration = sf.info(os.path.join(DATA_DIR, "star-wars-4.wav")).duration
    # energy = get_energy(os.path.join(DATA_DIR, "selfiefromhell.wav"))
    # # duration = sf.info(os.path.join(DATA_DIR, "selfiefromhell.wav")).duration
    #
    arousal, valence = get_subs_sentiment(os.path.join(BASE_DIR, "src/testfiles/" "blade_subs.xml"))
    times = [x[0] for x in arousal]
    # arousal_scores = [x[1] for x in arousal]
    valence_scores = [x[1] for x in valence]

    #
    time2 = datetime.now()
    diff = time2 - time

    print(diff)

    # combine(scenes, energy, duration)
    combine_subs(valence_scores, times, energy, duration)
    # for s in scenes:
    #     print(s)


if __name__ == '__main__':
    main()
