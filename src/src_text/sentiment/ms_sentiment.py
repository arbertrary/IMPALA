import os
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates
from sentiment import ImpalaSent
from moviescript import get_full_scenes, get_all_sentences
from typing import List, Tuple

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir, os.pardir))
DATA_DIR = "testfiles"


def scenesentiment(xml_path: str):
    """Plan: sentiment für komplette szenen; plotten in zwei unterschiedlichen graphen. Valence and arousal"""

    sentiment = ImpalaSent()

    scenes = get_full_scenes(xml_path)

    valence_values = []
    arousal_values = []
    for scene in scenes:
        time = datetime.strptime(scene[0], "%H:%M:%S")

        # sentences = scenes[scene]
        sentences = scene[1]
        text = " ".join(sentences)
        score = sentiment.score(text)

        valence = score[0]
        arousal = score[1]
        if valence != 0:
            valence_values.append((time, valence))
        if arousal != 0:
            arousal_values.append((time, arousal))

    # valence_values = sorted(valence_values, key= lambda tup: tup[0])
    valence_values.sort(key=lambda tup: tup[0])
    xv = [v[0] for v in valence_values]
    yv = [v[1] for v in valence_values]
    xv = dates.date2num(xv)

    # arousal_values = sorted(arousal_values, key= lambda tup: tup[0])
    arousal_values.sort(key=lambda tup: tup[0])
    xa = [a[0] for a in arousal_values]
    ya = [a[1] for a in arousal_values]
    xa = dates.date2num(xa)

    plt.figure().suptitle("Hellraiser Scene Sentiment")

    plt.subplot(211)
    plt.plot_date(xv, yv, fmt="-")
    # plt.fill(xv, yv)
    plt.xlim(xv[0], xv[-1])
    # plt.plot(xv, yv)
    plt.ylabel("Valence")
    plt.xlabel("time")
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.subplot(212)
    plt.ylabel("Arousal")
    plt.xlabel("time")
    # plt.plot(xa, ya)
    plt.plot_date(xa, ya, "-")
    # plt.fill(xa, ya)
    plt.xlim(xa[0], xa[-1])
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.tight_layout()
    plt.show()


def get_arousal_values(scenes:  List[Tuple[str, List[str]]]):
    """Plan: sentiment für komplette szenen; plotten in zwei unterschiedlichen graphen. Valence and arousal"""

    sentiment = ImpalaSent()

    # scenes = get_full_scenes(xml_path)

    arousal_values = []
    for scene in scenes:
        time = datetime.strptime(scene[0], "%H:%M:%S")

        # sentences = scenes[scene]
        sentences = scene[1]
        text = " ".join(sentences)
        score = sentiment.score(text)

        arousal = score[1]
        if arousal != 0:
            arousal_values.append((time, arousal))

    arousal_values.sort(key=lambda tup: tup[0])
    xa = [a[0] for a in arousal_values]
    # ya = [a[1] for a in arousal_values]
    # xa = dates.date2num(xa)

    return arousal_values


def sentence_sentiment(xml_path):
    sentiment = ImpalaSent()

    sentences = get_all_sentences(xml_path)

    valence_values = []
    arousal_values = []
    for sent in sentences:
        time = datetime.strptime(sent[0], "%H:%M:%S")

        # sentences = scenes[scene]
        sentence = sent[1]
        # text = " ".join(sentences)
        score = sentiment.score(sentence)

        valence = score[0]
        arousal = score[1]
        if valence != 0:
            valence_values.append((time, valence))
        if arousal != 0:
            arousal_values.append((time, arousal))

    arousal_values.sort(key=lambda tup: tup[0])

    ##############################
    # from sentences with the same time take only the one with the maximum arousal
    done = []
    ar_temp = []
    i = 1

    for v in arousal_values:
        if v[0] in done:
            continue

        sametime = [x for x in arousal_values if x[0] == v[0]]
        done.append(v[0])

        max_arousal = max(sametime, key=lambda x: x[1])[1]
        ar_temp.append((v[0], max_arousal))

    xa = [a[0] for a in ar_temp]
    ya = [a[1] for a in ar_temp]
    ##################################

    # xa = [a[0] for a in arousal_values]
    # ya = [a[1] for a in arousal_values]
    xa = dates.date2num(xa)

    valence_values.sort(key=lambda tup: tup[0])
    xv = [v[0] for v in valence_values]
    yv = [v[1] for v in valence_values]
    xv = dates.date2num(xv)

    plt.figure().suptitle("Hellraiser Sentence Sentiment")

    plt.subplot(211)
    plt.ylabel("Arousal")
    plt.xlabel("time")
    # plt.plot(xa, ya)
    plt.plot_date(xa, ya, "b-")
    plt.xlim(xa[0], xa[-1])
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.subplot(212)
    plt.plot_date(xv, yv, "b-")
    # plt.xlim(xv[0], xv[-1])
    plt.plot(xv, yv)
    plt.ylabel("Valence")
    plt.xlabel("time")
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
    plt.show()


def main():
    # print("Hello")
    path = os.path.join(PAR_DIR, DATA_DIR)
    xml_path = os.path.join(path, "hellraiser_annotated.xml")
    # xml_path = os.path.join(path, "star-wars-4_annotated.xml")

    scenesentiment(xml_path)
    # sentence_sentiment(xml_path)


if __name__ == '__main__':
    main()
