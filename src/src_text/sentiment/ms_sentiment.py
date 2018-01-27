import sys
import os
import functools
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates
from typing import List, Tuple

from sentiment import ImpalaSent
from moviescript import get_full_scenes, get_all_sentences

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


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


def weighted_scenesentiment(xml_path: str):
    scenes = get_full_scenes(xml_path)
    y = get_arousal_values_wo_time(scenes)

    # total = functools.reduce(lambda x, y: x + len(y[1]), scenes, 0)

    x = []
    i = 0
    for s in scenes:
        l = len(s[1])
        i += l
        x.append(i)

    print(len(x))
    print(len(y))

    test = get_arousal_values(scenes)
    x2 = [a[0] for a in test]
    y2 = [a[1] for a in test]
    x2 = dates.date2num(x2)

    plt.figure().suptitle("Hellraiser Scene Sentiment")

    plt.subplot(311)
    plt.ylabel("Arousal")
    plt.xlabel("scenes")
    plt.plot(y)
    plt.xlim(0, len(y))

    plt.subplot(312)
    plt.plot(x, y)
    plt.ylabel("Arousal")
    plt.xlabel("Scenes in Abh. ihrer Länge")
    plt.xlim(x[0], x[-1])

    plt.subplot(313)
    plt.ylabel("Arousal")
    plt.xlabel("time")
    plt.plot_date(x2, y2, "-")
    plt.xlim(x2[0], x2[-1])
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.tight_layout()
    plt.show()


def get_arousal_weights(scenes: List[Tuple[str, List[str]]]):
    sentiment = ImpalaSent()

    arousal_values = []
    for scene in scenes:
        sentences = scene[1]
        text = " ".join(sentences)
        score = sentiment.arousal_weights(text)

        arousal = score[0]
        # if arousal != 0:
        # arousal_values.append((arousal, score[1]))
        arousal_values.append(score[1])

        # else:
        #     arousal_values.append((4.21)

    # arousal_values.sort(key=lambda tup: tup[0])

    return arousal_values


def get_arousal_values_wo_time(scenes: List[Tuple[str, List[str]]]):
    sentiment = ImpalaSent()

    arousal_values = []
    for scene in scenes:

        sentences = scene[1]
        text = " ".join(sentences)
        score = sentiment.score(text)

        arousal = score[1]
        if arousal != 0:
            arousal_values.append(arousal)
        else:
            arousal_values.append(4.21)

    # arousal_values.sort(key=lambda tup: tup[0])

    return arousal_values


def get_arousal_values(scenes: List[Tuple[str, List[str]]]):
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
        else:
            arousal_values.append((time, 4.21))

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
    path = os.path.join(BASE_DIR, "src/testfiles/")
    xml_path = os.path.join(path, "hellraiser_annotated.xml")
    # xml_path = os.path.join(path, "star-wars-4_annotated.xml")

    # scenesentiment(xml_path)
    weighted_scenesentiment(xml_path)

    # scenes = get_scenes_wo_time(xml_path)
    # test = get_arousal_weights(scenes)
    #
    # x = []
    # i = 0
    # for s in scenes:
    #     l = len(s[1])
    #     # i += l
    #     x.append(l)
    #
    # # print("found words: \n", test)
    # # print("# of sentences: \n", x)
    #
    # j = 0
    # while j <len(test):
    #     print("sentences: ", x[j], "\t", "found words: ", test[j])
    #     j+=1


if __name__ == '__main__':
    main()
