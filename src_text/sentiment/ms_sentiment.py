import os
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates
from sentiment import ImpalaSent
from moviescript import get_full_scenes


PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"

def scenesentiment(xml_path: str):
    """Plan: sentiment für komplette szenen; plotten in zwei unterschiedlichen graphen. Valence and arousal"""

    sent = ImpalaSent()

    scenes = get_full_scenes(xml_path)

    valence_values = []
    arousal_values = []
    for scene in scenes:
        time = datetime.strptime(scene[0], "%H:%M:%S")

        # sentences = scenes[scene]
        sentences = scene[1]
        text = " ".join(sentences)
        score = sent.score(text)
        valence = score[0]
        arousal = score[1]

        valence_values.append((time, valence))
        arousal_values.append((time, arousal))


    # valence_values = sorted(valence_values, key= lambda tup: tup[0])
    valence_values.sort(key=lambda tup: tup[0])
    xv = [v[0] for v in valence_values]
    yv = [v[1] for v in valence_values]
    xv = dates.date2num(xv)

    # arousal_values = sorted(arousal_values, key= lambda tup: tup[0])
    arousal_values.sort(key= lambda tup: tup[0])
    xa = [a[0] for a in arousal_values]
    ya = [a[1] for a in arousal_values]
    xa = dates.date2num(xa)

    plt.figure().suptitle("Hellraiser Sentiment")
    plt.subplot(211)
    plt.plot_date(xv, yv, "b-")
    plt.xlim(xv[0], xv[-1])
    # plt.plot(xv, yv)
    plt.ylabel("Valence")
    plt.xlabel("time")

    plt.subplot(212)
    plt.ylabel("Arousal")
    plt.xlabel("time")
    # plt.plot(xa, ya)
    plt.plot_date(xa, ya, "b-")
    plt.xlim(xa[0], xa[-1])

    plt.show()


def main():
    # print("Hello")
    path = os.path.join(PAR_DIR, DATA_DIR)
    xml_path = os.path.join(path, "hellraiser_annotated.xml")
    # xml_path = os.path.join(path, "star-wars-4_annotated.xml")


    scenesentiment(xml_path)

if __name__ == '__main__':
    main()
