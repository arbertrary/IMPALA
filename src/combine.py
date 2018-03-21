"""Combines sentiment analysis and audio analysis into csv files"""

import numpy as np
import os
import pandas as pd
import csv
import librosa
import src.utility as util
from src.src_text.sentiment.ms_sentiment import scenesentiment_man_annotated, plaintext_sentiment
from src.src_text.sentiment.subs_sentiment import subtitle_sentiment
from src.src_text.sentiment.sentiment import SentimentClass
from src.src_text.preprocessing.moviescript import get_scenes

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def audiosent_csv(xml_path: str, audio_csv: str, dest_csv_path: str, feature_column: str,
                  sent_method: str = "Warriner", subtitles: bool = False, **kwargs):
    """
    Creates csv files combining audio and sentiment
    :param xml_path: the xml file (either subtitles or xml movie script)
    :param audio_csv: the audio csv file
    :param dest_csv_path: destination path of the resulting file
    :param feature_column: which audio feature to write
    :param sent_method: which sentiment method to use (Warriner, NRC, Vader or combined.
    "combined" is Vader and Warriner
    :param subtitles: boolean whether the xml_path input is a subtitle file. defaults to false
    :param kwargs: currently only "normalized" if normalized is True then the audio feature values will be normalized
    :return: writes data to csv file
    """

    if sent_method not in {"Warriner", "NRC", "Vader", "combined"}:
        raise ValueError(
            "Incorrect sentiment method. Choose 'Warriner', 'Vader', 'NRC' or 'combined' (Warriner+Vader)!")

    if sent_method == "combined":
        if subtitles:
            raise ValueError("Sorry, not yet implemented for subtitles!")
        ts = scenesentiment_man_annotated(xml_path, sent_method="Warriner")
        ts2 = scenesentiment_man_annotated(xml_path, sent_method="Vader")
        temp = []
        for s in ts:
            for t in ts2:
                if s[-1] == t[-1] and s[0] == t[0] and s[1] == t[1]:
                    temp.append(t)
        ts2 = temp

    else:
        if subtitles:
            ts = subtitle_sentiment(xml_path, sent_method)
        else:
            ts = scenesentiment_man_annotated(xml_path, sent_method)

    df = pd.read_csv(audio_csv)
    time = df.get("Time").values
    try:
        feature = df.get(feature_column).values
    except AttributeError as error:
        raise ValueError(
            """Incorrect audio feature. 
            Choose 'Audio Energy', 'Spectral Centroid' 
            or 'mfccN' with N for the n-th mel-frequency cepstral coefficient!""") from error

    partitions = list(zip(time, feature))

    scene_audio = []
    scene_sentiment = []
    scene_sentiment2 = []
    for index, t in enumerate(ts):
        temp_audio = [x[1] for x in partitions if t[0] <= x[0] <= t[1]]

        if len(temp_audio) != 0:
            scene_audio.append(np.mean(temp_audio))
            scene_sentiment.append(t)
            if sent_method == "combined":
                scene_sentiment2.append(ts2[index])

    if kwargs.get("normalized"):
        scene_audio = librosa.util.normalize(np.array(scene_audio))

    if not os.path.isfile(dest_csv_path):
        mode = "w"
    elif os.stat(dest_csv_path).st_size == 0:
        mode = "w"
    else:
        mode = "a"

    with open(dest_csv_path, mode) as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        if mode == "w":
            if sent_method == "Warriner":
                writer.writerow(["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", feature_column])
            elif sent_method == "NRC":
                writer.writerow(
                    ["Scene Start", "Scene End", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Negative",
                     "Positive", "Sadness", "Surprise", "Trust", feature_column])
            elif sent_method == "Vader":
                writer.writerow(["Scene Start", "Scene End", "neg", "neu", "pos", "compound", feature_column])
            elif sent_method == "combined":
                writer.writerow(
                    ["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", "Vader neg", "Vader neu",
                     "Vader pos", "Vader compound",
                     feature_column])

        for i, t in enumerate(scene_audio):
            level = t
            start = scene_sentiment[i][0]
            end = scene_sentiment[i][1]
            score = scene_sentiment[i][2]
            if sent_method == "combined":
                score2 = scene_sentiment2[i][2]

            if sent_method == "Warriner":
                writer.writerow([start, end, score.get("valence"), score.get("arousal"), score.get("dominance"), level])
            elif sent_method == "NRC":
                writer.writerow(
                    [start, end, score.get("anger"), score.get("anticipation"), score.get("disgust"), score.get("fear"),
                     score.get("joy"),
                     score.get("negative"), score.get("positive"), score.get("sadness"), score.get("surprise"),
                     score.get("trust"), level])
            elif sent_method == "Vader":
                writer.writerow(
                    [start, end, score.get("neg"), score.get("neu"), score.get("pos"), score.get("compound"), level])
            elif sent_method == "combined":
                writer.writerow(
                    [start, end, score.get("valence"), score.get("arousal"), score.get("dominance"), score2.get("neg"),
                     score2.get("neu"), score2.get("pos"), score2.get("compound"), level])


def fountain_audiosent_csv(fountain_script: str, audio_csv: str, n_sections: int, dest_path: str,
                           feature_column: str, sent_method: str = "Warriner"):
    """Creates audiosentiment csv file for plain text fountain movie scripts
    :param fountain_script: the file path
    :param audio_csv: the audio csv file path
    :param n_sections: the number of secitons the movie script will be split into
    :param dest_path: the destination of the resulting csv file
    :param feature_column: which audio feature to use
    :param sent_method: which sentiment method to use
    :return:
    """
    sent_sections = plaintext_sentiment(fountain_script, n_sections, sent_method)

    df = pd.read_csv(audio_csv)
    try:
        audio = df.get(feature_column).values
    except AttributeError as error:
        raise ValueError(
            """Incorrect audio feature. 
            Choose 'Audio Energy', 'Spectral Centroid' 
            or 'mfccN' with N for the n-th mel-frequency cepstral coefficient!""") from error

    partitions = [np.mean(x) for x in util.split(audio, n_sections)]

    with open(dest_path, "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        for index, item in enumerate(sent_sections):
            writer.writerow([item.get("valence"), item.get("arousal"), item.get("dominance"), partitions[index]])


def audiosent_scenes_wo_time(xml_path: str, audio_csv: str, dest_path: str, feature_column: str):
    """
       Creates csv files combining audio and sentiment without information of the time codes
       :param xml_path: the xml file (either subtitles or xml movie script)
       :param audio_csv: the audio csv file
       :param dest_path: destination path of the resulting file
       :param feature_column: which audio feature to write
       :return: writes data to csv file
       """
    sentiment = SentimentClass()

    scenes = get_scenes(xml_path)
    scene_sentiment = [sentiment.score(" ".join(x)) for x in scenes]

    df = pd.read_csv(audio_csv)
    try:
        audio = df.get(feature_column).values
    except AttributeError as error:
        raise ValueError(
            """Incorrect audio feature. 
            Choose 'Audio Energy', 'Spectral Centroid' 
            or 'mfccN' with N for the n-th mel-frequency cepstral coefficient!""") from error

    partitions = [np.mean(x) for x in util.split(audio, len(scenes))]

    with open(dest_path, "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        for index, item in enumerate(scene_sentiment):
            writer.writerow([item.get("valence"), item.get("arousal"), item.get("dominance"), partitions[index]])
