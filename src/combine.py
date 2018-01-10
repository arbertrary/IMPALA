"""Combines sentiment analysis and audio analysis"""

import os
import soundfile as sf
import numpy as np
from datetime import datetime
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

#TODO: Pfade handlen! os.curdir macht Probleme. Für alle Module!!!
def combine(scenes):  # , energy, duration):

    s_count = len(scenes)
    print(s_count)
    # intervals = np.array_split(energy, len(energy) / s_count)

    arousal_values = get_arousal_values(scenes)

    #TODO: timestamp() funktioniert so nicht ganz
    times = [a[0].timestamp for a in arousal_values]
    print(times[0])
    scores = [a[1] for a in arousal_values]
    # times = dates.date2num(times)


def main():
    scenes = get_full_scenes(os.path.join(DATA_DIR, "hellraiser_annotated.xml"))
    # energy = get_energy(os.path.join(DATA_DIR, "selfiefromhell.wav"))
    duration = sf.info(os.path.join(DATA_DIR, "selfiefromhell.wav")).duration

    combine(scenes)
    print("asdfa")


if __name__ == '__main__':
    main()
