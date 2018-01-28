"""Sentiment analysis of subtitle files"""

import os
import matplotlib.pyplot as plt
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from matplotlib import dates
from datetime import datetime, timedelta
from sentiment import ImpalaSent
from subtitles import get_subtitles

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def get_subs_sentiment(subs_filename: str):
    """Analyse dialogue from subtitles"""

    sentiment = ImpalaSent()

    sentences = get_subtitles(subs_filename)
    print(len(sentences))
    scores = []
    scores2 = []
    times = []

    for s in sentences:
        # diese Zeile ist erstmal nur temporär da und nimmt den String (s[1]) und den arousal wert score[1]
        # valence wäre score[0]
        arousal = sentiment.score(s[2])[1]
        valence = sentiment.score(s[2])[0]
        # if arousal == 0:
        #     continue
        # else:
        time = datetime.strptime(s[0], "%H:%M:%S,%f")
        scores.append(arousal)
        scores2.append(valence)
        times.append(time)

    # scores = scores[::3]
    # print(len(scores))
    # times = times[::3]
    #
    # times = dates.date2num(times)
    #
    # plt.subplot(212)
    # plt.ylabel("Arousal")
    # plt.xlabel("time")
    #
    # plt.plot_date(times, scores, fmt="-", color="b", label="Arousal")
    # plt.xlim(times[0], times[-1])
    # plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    # plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
    #
    # plt.tight_layout()
    # plt.show()

    return scores, scores2


def get_nrc_sentiment(subs_filename: str):
    sentiment = ImpalaSent(method="NRC")

    sentences = get_subtitles(subs_filename)

    scores = []
    for s in sentences:
        emotions = sentiment.nrc_score(s[2])
        scores.append((s[0], emotions))
        # print(s)
        # print(emotions)
    return scores


def get_vader_sentiment(subs_filename: str):
    sentences = get_subtitles(subs_filename)
    sid = SentimentIntensityAnalyzer()

    scores = []
    times = []
    for s in sentences:
        scores.append(sid.polarity_scores(s[2]).get("compound"))
        # print(sid.polarity_scores(s[1]))
        time = datetime.strptime(s[0], "%H:%M:%S,%f")

        times.append(time)

    return scores, times


def plot_stuff(path):
    scores1, times1 = get_vader_sentiment(path)
    scores2, times2 = get_subs_sentiment(path)

    # scores1 = scores1[::3]
    # print(len(scores1))
    # times1 = times1[::3]
    #
    # scores2 = scores2[::3]
    # print(len(scores2))
    # times2 = times2[::3]

    times1 = dates.date2num(times1)
    times2 = dates.date2num(times2)

    plt.subplot(211)
    plt.ylabel("Vader Compound score")
    plt.xlabel("time")

    plt.plot_date(times1, scores1, fmt="-", color="b", label="compound")
    plt.xlim(times1[0], times1[-1])
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.subplot(212)
    plt.ylabel("Warriner Arousal")
    plt.xlabel("time")

    plt.plot_date(times2, scores2, fmt="-", color="b", label="Arousal")
    plt.xlim(times2[0], times2[-1])
    plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))

    plt.tight_layout()
    plt.show()


def main():
    """main function"""
    path = os.path.join(BASE_DIR, "src/testfiles", "american-psycho_subs.xml")
    # path = "/home/armin/Studium/Bachelor/CodeBachelorarbeit/IMPALA/src/testfiles/american-psycho_subs.xml"
    # path = "/home/armin/Studium/Bachelor/CodeBachelorarbeit/IMPALA/src/testfiles/star-wars-4_subs.xml"
    # test= get_nrc_sentiment(path)
    # test, test2 = get_subs_sentiment(path)
    # test, times = get_vader_sentiment(path)

    # c1 = 0
    # c2 = 0
    # for t in test:
    #     if np.max(t[1]) == 0:
    #     # if t == 0:
    #         c1 += 1
    #     else:
    #         c2 += 1
    # print("sätze ohne wert: ", c1)
    # print("sätze mit: ", c2)


if __name__ == '__main__':
    main()
