import os
import matplotlib.pyplot as plt
import src.utility as util
from datetime import datetime
from typing import List, Tuple, Dict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from src.src_text.sentiment.sentiment import ImpalaSent
from src.src_text.preprocessing.moviescript import get_full_scenes, get_scenes_man_annotated, get_all_sentences

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def sentence_sentiment(xml_path: str):
    sentiment = ImpalaSent()
    sentences = get_all_sentences(xml_path)
    scores = []
    for s in sentences:
        score = sentiment.score(s)
        scores.append(score)

    return scores


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

        valence = score.get("valence")
        arousal = score.get("arousal")
        dominance = score.get("dominance")
        if valence != -1:
            sentiment_tuples.append((time_sec, score))

    sentiment_tuples.sort(key=lambda tup: tup[0])

    return sentiment_tuples


def scenesentiment_for_man_annotated(xml_path: str, sent_method: str = "Warriner") -> List[Tuple[float, float, Dict]]:
    """:returns List of Tuples of [scene-starttime in seconds, scene-endtime in seconds, sentiment scores:Dict"""
    if sent_method not in {"Warriner", "NRC", "Vader"}:
        raise ValueError("Incorrect sentiment method. Choose \"Warriner\" or \"NRC\"!")
    elif sent_method == "Vader":
        sid = SentimentIntensityAnalyzer()
    else:
        sentiment = ImpalaSent(sent_method)

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
        if sent_method == "Warriner":
            score = sentiment.score(text)
        elif sent_method == "NRC":
            score = sentiment.nrc_score(text)
        elif sent_method == "Vader":
            score = sid.polarity_scores(text)

        if all(score.get(x) == -1 for x in score):
            continue
        else:
            sentiment_tuples.append((start, end, score))

    sentiment_tuples.sort(key=lambda tup: tup[0])

    return sentiment_tuples


def plaintext_sentiment(fountain_path: os.path, n_parts: int, sent_method: str = "Warriner"):
    sentiment = ImpalaSent()

    with open(fountain_path) as textfile:
        text = textfile.read()

        section_length = int(len(text) / n_parts)
        sections = util.part(text, section_length)

    sections = [sentiment.score(x) for x in sections]

    return sections


def plot_scenesentiment(sentiment_values: List):
    x = [s[0] for s in sentiment_values]
    # x = dates.date2num(x)
    yv = [v[2].get("anger") for v in sentiment_values]
    ya = [a[2].get("joy") for a in sentiment_values]
    yd = [d[2].get("negative") for d in sentiment_values]

    plt.subplot(311)
    plt.plot(x, yv)
    plt.xlim(x[0], x[-1])
    plt.ylabel("anger")
    plt.xlabel("time")

    plt.subplot(312)
    plt.ylabel("joy")
    plt.xlabel("time")
    plt.plot(x, ya)
    plt.xlim(x[0], x[-1])

    plt.subplot(313)
    plt.ylabel("negative")
    plt.xlabel("time")
    plt.plot(x, yd)
    plt.xlim(x[0], x[-1])

    # nur mal zum Merken, damit ich nicht wieder googlen muss
    # plt.plot_date(x, yd, "-")
    # plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    # plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.tight_layout()
    plt.show()


def main():
    # print("Hello")
    path = os.path.join(BASE_DIR, "src/testfiles/")
    sw = os.path.join(path, "star-wars-4_annotated.xml")
    sw_man = os.path.join(path, "star-wars-4_man.xml")

    a = scenesentiment_for_man_annotated(sw_man, "NRC")
    plot_scenesentiment(a)
    print(a)


if __name__ == '__main__':
    main()
