"""Module for calculating sentiment for movie scripts.
Contains functions for f"""
import os
import src.utility as util
from datetime import datetime
from typing import List, Tuple, Dict
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from src.src_text.sentiment.sentiment import SentimentClass
import src.src_text.preprocessing.moviescript as ms

# BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


def scenesentiment_auto_annotated(xml_path: str) -> List[Tuple[float, float, float, float]]:
    """Plan: sentiment für komplette szenen; plotten in zwei unterschiedlichen graphen. Valence and arousal"""

    sentiment = SentimentClass()

    scenes = ms.get_scenes_auto_annotated(xml_path)
    characters = ms.get_characters(xml_path)
    beginning = datetime.strptime("00:00:00", '%H:%M:%S')

    sentiment_tuples = []
    for scene in scenes:
        time = datetime.strptime(scene[0], "%H:%M:%S")
        time_sec = (time - beginning).total_seconds()

        sentences = scene[1]
        text = " ".join(sentences)
        score = sentiment.score(text, stopwords=characters)

        if all(score.get(x) == -1 for x in score):
            continue
        else:
            sentiment_tuples.append((time_sec, score))

    sentiment_tuples.sort(key=lambda tup: tup[0])

    return sentiment_tuples


def scenesentiment_man_annotated(xml_path: str, sent_method: str = "Warriner") -> List[Tuple[float, float, Dict]]:
    """Returns sentiment for manually annotated xml movie scripts
    :returns List of Tuples of [scene-starttime in seconds, scene-endtime in seconds, sentiment scores:Dict"""
    if sent_method not in {"Warriner", "NRC", "Vader"}:
        raise ValueError("Incorrect sentiment method. Choose \"Warriner\" or \"NRC\"!")
    elif sent_method == "Vader":
        sid = SentimentIntensityAnalyzer()
    else:
        sentiment = SentimentClass(sent_method)

    scenes = ms.get_scenes_man_annotated(xml_path)
    characters = ms.get_characters(xml_path)
    beginning = datetime.strptime("00:00:00", '%H:%M:%S')

    sentiment_tuples = []
    for scene in scenes:
        scene_id = scene[-1]
        starttime_string = scene[0]
        starttime = datetime.strptime(starttime_string, '%H:%M:%S')
        start = (starttime - beginning).total_seconds()

        endtime_string = scene[1]
        endtime = datetime.strptime(endtime_string, '%H:%M:%S')
        end = (endtime - beginning).total_seconds()

        sentences = scene[2]
        text = " ".join(sentences)
        if sent_method == "Warriner":
            score = sentiment.score(text, stopwords=characters)
        elif sent_method == "NRC":
            score = sentiment.nrc_score(text)
        elif sent_method == "Vader":
            score = sid.polarity_scores(text)

        if all(score.get(x) == -1 for x in score):
            continue
        else:
            sentiment_tuples.append((start, end, score, scene_id))

    sentiment_tuples.sort(key=lambda tup: tup[0])

    return sentiment_tuples


def plaintext_sentiment(fountain_path: str, n_parts: int, sent_method: str = "Warriner"):
    """Sentiment for plain text fountain movie scripts.
    Separates plain text into n_parts sections of same length.
    :param fountain_path: plain text fountain movie script path
    :param n_parts: The number of sections the script will be split into
    :param sent_method: Which sentiment method to use
    """
    if fountain_path.endswith(".xml"):
        raise ValueError("Not a plain text movie script!")

    sentiment = SentimentClass(sent_method)

    with open(fountain_path) as textfile:
        text = textfile.read()

        sections = util.split(text, n_parts)

    sections = [sentiment.score(x) for x in sections]

    return sections
