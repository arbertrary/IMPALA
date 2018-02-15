"""Sentiment analysis of subtitle files"""

import os
import matplotlib.pyplot as plt
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from matplotlib import dates
from typing import List, Tuple, Dict
from datetime import datetime, timedelta
from src.src_text.sentiment.sentiment import ImpalaSent
from src.src_text.preprocessing.subtitles import get_subtitles

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def subtitle_sentiment(xml_path: str, sent_method: str = "Warriner") -> List[Tuple[float, float, Dict]]:
    """:returns List of Tuples of [scene-starttime in seconds, scene-endtime in seconds, sentiment scores:Dict"""
    if sent_method not in {"Warriner", "NRC", "Vader"}:
        raise ValueError("Incorrect sentiment method. Choose \"Warriner\" or \"NRC\"!")
    elif sent_method == "Vader":
        sid = SentimentIntensityAnalyzer()
    else:
        sentiment = ImpalaSent(sent_method)

    sentences = get_subtitles(xml_path)
    scores = []

    for s in sentences:
        score = sentiment.score(s[2])
        if all(score.get(x) == -1 for x in score):
            continue

        arousal = sentiment.score(s[2]).get("arousal")
        valence = sentiment.score(s[2]).get("valence")

        start = round(s[0])
        end = round(s[1])
        scores.append((start, end, score))
        # scores2.append(valence)
        # scores2.append((time, valence))

    return scores


def plot_stuff(path):
    sentiment = subtitle_sentiment(path)

    arousal = [score[2].get("arousal") for score in sentiment]

    windows = []

    for index, score in enumerate(arousal):
        if index+4 <= len(arousal):
            temp = arousal[index:index+4]
            if index== 0:
                print(len(temp))
            windows.append(np.mean(temp))
        else:
            temp = arousal[index:]
            windows.append(np.mean(temp))

    print(len(windows), len(arousal))

    plt.subplot(211)
    plt.plot(arousal)
    plt.subplot(212)
    plt.plot(windows)
    plt.tight_layout()
    plt.show()




def main():
    """main function"""
    path = os.path.join(BASE_DIR, "src/testfiles", "hellraiser_subs.xml")
    # subs = get_subtitles(path)
    # print(subs)
    print(subtitle_sentiment(path, "Warriner"))
    # plot_stuff(path)


if __name__ == '__main__':
    main()
