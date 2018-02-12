import os
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates
from typing import List, Tuple
from src.src_text.sentiment.sentiment import ImpalaSent
from src.src_text.preprocessing.moviescript import get_full_scenes, get_scenes_man_annotated

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def scenesentiment(xml_path: str) -> List[Tuple[float, float, float, float]]:
    """Plan: sentiment für komplette szenen; plotten in zwei unterschiedlichen graphen. Valence and arousal"""

    sentiment = ImpalaSent()

    scenes = get_full_scenes(xml_path)
    beginning = datetime.strptime("00:00:00", '%H:%M:%S')

    sentiment_tuples = []
    for scene in scenes:
        time = datetime.strptime(scene[0], "%H:%M:%S")
        time_sec = (time - beginning).total_seconds()

        sentences = scene[1]
        text = " ".join(sentences)
        score = sentiment.score(text)

        valence = score[0]
        arousal = score[1]
        dominance = score[2]
        if valence != -1:
            sentiment_tuples.append((time_sec, valence, arousal, dominance))

    sentiment_tuples.sort(key=lambda tup: tup[0])

    return sentiment_tuples


def scenesentiment_for_manually_annotated(xml_path: str) -> List[Tuple[float, float, float, float, float]]:
    """:returns list of Tuples of [starttime, valence, arousal, dominance, endtime]
    not having start and end with indices 0 and 1 is stupid but currently necessary because it's easier to deal with
    for functions that need to take both this and normal scenesentiment (only one time code)"""
    sentiment = ImpalaSent()

    scenes = get_scenes_man_annotated(xml_path)
    beginning = datetime.strptime("00:00:00", '%H:%M:%S')

    sentiment_tuples = []
    for scene in scenes:
        starttime_string = scene[0]
        starttime = datetime.strptime(starttime_string, '%H:%M:%S')
        start = (starttime - beginning).total_seconds()

        endtime_string = scene[1]
        endtime = datetime.strptime(endtime_string, '%H:%M:%S')
        end = (endtime - beginning).total_seconds()

        sentences = scene[2]
        text = " ".join(sentences)
        score = sentiment.score(text)

        valence = score[0]
        arousal = score[1]
        dominance = score[2]
        if valence != -1:
            sentiment_tuples.append((start, valence, arousal, dominance, end))

    sentiment_tuples.sort(key=lambda tup: tup[0])

    return sentiment_tuples


def plot_scenesentiment(sentiment_values: List):
    x = [s[0] for s in sentiment_values]
    # x = dates.date2num(x)
    yv = [v[1] for v in sentiment_values]
    ya = [a[2] for a in sentiment_values]
    yd = [a[3] for a in sentiment_values]

    plt.subplot(311)
    # plt.plot_date(x, yv, fmt="-")
    plt.plot(x, yv)
    plt.xlim(x[0], x[-1])
    plt.ylabel("Valence")
    plt.xlabel("time")
    # plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    # plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.subplot(312)
    plt.ylabel("Arousal")
    plt.xlabel("time")
    # plt.plot_date(x, ya, "-")
    plt.plot(x, ya)
    plt.xlim(x[0], x[-1])
    # plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    # plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.subplot(313)
    plt.ylabel("Dominace")
    plt.xlabel("time")
    # plt.plot_date(x, yd, "-")
    plt.plot(x, yd)
    plt.xlim(x[0], x[-1])
    # plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    # plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.tight_layout()
    plt.show()


def main():
    # print("Hello")
    path = os.path.join(BASE_DIR, "src/testfiles/")
    sw = os.path.join(path, "star-wars-4_annotated.xml")
    sw_man = os.path.join(path, "star-wars-4_man.xml")

    a = scenesentiment(sw)
    b = scenesentiment_for_manually_annotated(sw_man)
    plot_scenesentiment(a)
    plot_scenesentiment(b)


if __name__ == '__main__':
    main()
