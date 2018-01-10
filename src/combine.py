"""Combines sentiment analysis and audio analysis"""

import os
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates
from moviescript import get_full_scenes
from audio_analysis import get_energy
from ms_sentiment import get_arousal_values

"""Idee:
- scenes mit time codes aus moviescript get_full_scenes
- energy aus audio_analysis (noch nicht in Intervalle eingeteilt)
- nimm die time codes der Szenen um die energy aufzuteilen
- plotte beides über der gleichen Zeitachse
"""

DATA_DIR = os.path.join(os.curdir, "testfiles")


# TODO: Pfade handlen! os.curdir macht Probleme. Für alle Module!!!
def combine(scenes, energy, duration):
    """
    :param scenes = list of scenes + their timecodes\n
    :param energy = np.array of RMS energy of the audio file\n
    :param duration = duration of the audio
    """
    scene_count = len(scenes)
    intervals = np.array_split(energy, scene_count)
    intervals = [np.mean(e) for e in intervals]

    # block_duration = np.divide(duration, len(intervals))
    # en_times = []
    # time = 0
    # i = 1
    # while i <= len(intervals):
    #     # hms = str(timedelta(seconds=time))
    #     # print(hms)
    #     m, s = divmod(time, 60)
    #     h, m = divmod(m, 60)
    #     hms = "%d:%02d:%02d" % (h, m, s)
    #
    #     en_times.append(hms)
    #     time += block_duration
    #     i += 1

    arousal_values = get_arousal_values(scenes)

    # TODO: timestamp() funktioniert so nicht ganz
    times = [a[0] for a in arousal_values]
    scores = [a[1] for a in arousal_values]
    times = dates.date2num(times)

    plt.figure()
    plt.subplot(211)
    plt.title('Hellraiser: Audio (RMS Energy)')
    plt.xlabel("time")

    plt.semilogy(times, intervals, color="b", label="RMS Energy")
    # plt.plot_date(times, intervals, "-")
    plt.legend(loc='best')

    # plt.xlim(0, len(intervals))
    plt.xlim(times[0], times[-1])

    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.subplot(212)
    plt.title("Hellraiser: Sentiment (Arousal Scores)")
    plt.ylabel("Arousal")
    plt.xlabel("time")
    plt.plot_date(times, scores, fmt="-", color="b", label="Arousal")
    plt.legend(loc='best')
    plt.xlim(times[0], times[-1])
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.tight_layout()

    plt.show()


def main():
    scenes = get_full_scenes(os.path.join(DATA_DIR, "hellraiser_annotated.xml"))
    energy = get_energy(os.path.join(DATA_DIR, "hellraiser.wav"))
    duration = sf.info(os.path.join(DATA_DIR, "hellraiser.wav")).duration
    # energy = get_energy(os.path.join(DATA_DIR, "selfiefromhell.wav"))
    # duration = sf.info(os.path.join(DATA_DIR, "selfiefromhell.wav")).duration

    combine(scenes, energy, duration)


if __name__ == '__main__':
    main()
