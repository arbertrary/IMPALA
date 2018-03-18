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
        if sent_method == "Warriner":
            score = sentiment.score(s[2])
        elif sent_method == "NRC":
            score = sentiment.nrc_score(s[2])
        elif sent_method == "Vader":
            score = sid.polarity_scores(s[2])

        if all(score.get(x) == -1 for x in score):
            continue
        if score == {"valence": 5.06, "arousal": 4.21, "dominance": 5.18}:
            continue

        start = round(s[0])
        end = round(s[1])

        scores.append((start, end, score))

    return scores


def main():
    """main function"""
    path = os.path.join(BASE_DIR, "src/testfiles", "hellraiser_subs.xml")
    # subs = get_subtitles(path)
    # print(subs)
    # print(subtitle_sentiment(path, "NRC"))


if __name__ == '__main__':
    main()
