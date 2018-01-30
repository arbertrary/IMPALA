import sys
import os
import functools
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates
from typing import List, Tuple
import xml.etree.ElementTree as ET
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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


def entire_script(path):
    sentiment = ImpalaSent()
    sentiment2 = ImpalaSent("NRC")
    sentences = get_all_sentences(path)

    sid = SentimentIntensityAnalyzer()

    text = ""
    for s in sentences:
        text += " " + s[1]

    print(path)
    score = sentiment.score(text)
    print("valence", score[0], "arousal", score[1])
    e = sentiment2.nrc_score(text)
    print("anger", e[0], "anticipation", e[1], "disgust", e[2], "fear", e[3], "joy", e[4], "negative", e[5], "positive",
          e[6], "sadness", e[7], "surprise", e[8], "trust", e[9])
    score = sid.polarity_scores(text)
    print(score)
    print("\n")

def sent_classes(path):
    sentiment = ImpalaSent()
    tree = ET.parse(path)
    sentences = get_all_sentences(path)

    sid = SentimentIntensityAnalyzer()
    high = 0
    neutral = 0
    low = 0
    x1 = []
    x2 = []
    x3 = []
    for s in sentences:
        # score = sentiment.score(s[1])
        # valence.append(score[0])
        # arousal.append(score[1])
        score = sid.polarity_scores(s[1])
        x1.append(score.get("neg"))
        x2.append(score.get("pos"))
        x3.append(score.get("compound"))

        # if score[1] < 2.7:
        #     low +=1
        # elif score[1] > 5.7:
        #     high +=1
        # else:
        #     neutral += 1

    n_bins = 5
    print(len(x1))
    print(len(x2))
    fig, axs = plt.subplots(1, 3, tight_layout=True)


    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(x1, bins=n_bins)
    axs[0].set_title("neg")
    axs[1].hist(x2, bins=n_bins)
    axs[1].set_title("pos")
    axs[2].hist(x3, bins=n_bins)
    axs[2].set_title("compound")


def test_hist():
    np.random.seed(19680801)
    N_points = 100000
    n_bins = 5

    # Generate a normal distribution, center at x=0 and y=5
    x = np.random.randn(N_points)
    y = .4 * x + np.random.randn(100000) + 5

    fig, axs = plt.subplots(1, 2, tight_layout=True)

    # We can set the number of bins with the `bins` kwarg
    axs[0].hist(x, bins=n_bins)
    axs[1].hist(y, bins=n_bins)
    plt.show()

def main():
    # print("Hello")
    path = os.path.join(BASE_DIR, "src/testfiles/")
    xml_path1 = os.path.join(path, "hellraiser_annotated.xml")
    xml_path2 = os.path.join(path, "star-wars-4_annotated.xml")
    xml_path3 = os.path.join(path, "cars-2.xml")

    # scenesentiment(xml_path)
    # weighted_scenesentiment(xml_path)
    # entire_script(xml_path1)
    # entire_script(xml_path2)
    # entire_script(xml_path3)

    # print(xml_path1)
    sent_classes(xml_path1)
    # print("\n")
    # print(xml_path2)
    sent_classes(xml_path2)
    # print("\n")
    # print(xml_path3)
    sent_classes(xml_path3)
    plt.show()
    # test_hist()



if __name__ == '__main__':
    main()
