"""Combines sentiment analysis and audio analysis"""

import numpy as np
from datetime import datetime
import os
import csv
import matplotlib.pyplot as plt
import librosa
import src.utility as util
from src.src_text.sentiment.ms_sentiment import scenesentiment_for_man_annotated, sentence_sentiment, \
    plaintext_sentiment
from src.src_text.sentiment.subs_sentiment import subtitle_sentiment
from src.src_text.sentiment.sentiment import ImpalaSent
from src.src_text.preprocessing.moviescript import get_scenes_unannotated
from src import data_script, data_fountain, data_subs

"""Idee:
- scenes mit time codes aus moviescript get_full_scenes
- energy aus audio_analysis (noch nicht in Intervalle eingeteilt)
- nimm die time codes der Szenen um die energy aufzuteilen
- plotte beides über der gleichen Zeitachse
"""

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def audiosent_csv(script_path: str, audio_path: str, dest_csv_path: str, sent_method: str = "Warriner", **kwargs):
    if sent_method not in {"Warriner", "NRC", "Vader", "combined"}:
        raise ValueError("Incorrect sentiment method. Choose \"Warriner\" or \"NRC\"!")

    if sent_method == "combined":
        ts = scenesentiment_for_man_annotated(script_path, sent_method="Warriner")
        ts2 = scenesentiment_for_man_annotated(script_path, sent_method="Vader")
    else:
        # ts = subtitle_sentiment(script_path, sent_method)
        ts = scenesentiment_for_man_annotated(script_path, sent_method)
    print("warriner length", len(ts))
    partitions = []

    with open(audio_path) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            partitions.append((float(row[0]), float(row[1])))

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

    # print(len(ts), len(scene_sentiment))
    # print(len(ts2), len(scene_sentiment2))

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
                writer.writerow(["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", "Audio Level"])
            elif sent_method == "NRC":
                writer.writerow(
                    ["Scene Start", "Scene End", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Negative",
                     "Positive", "Sadness", "Surprise", "Trust", "Audio Level"])
            elif sent_method == "Vader":
                writer.writerow(["Scene Start", "Scene End", "neg", "neu", "pos", "compound", "Audio Level"])
            elif sent_method == "combined":
                writer.writerow(
                    ["Scene Start", "Scene End", "Valence", "Arousal", "Dominance", "Vader neg", "Vader neu",
                     "Vader pos", "Vader compound",
                     "Audio Level"])

        for i, t in enumerate(scene_audio):
            level = t
            start = scene_sentiment[i][0]
            end = scene_sentiment[i][1]
            score = scene_sentiment[i][2]
            if sent_method == "combined":
                score2 = scene_sentiment2[i][2]
            # score2 = None

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


def fountain_audiosent_csv(fountain_script: str, audio_path: str, n_sections: int, dest_path: str,
                           sent_method: str = "Warriner"):
    sent_sections = plaintext_sentiment(fountain_script, n_sections)

    audio = []
    with open(audio_path) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            audio.append(float(row[1]))

        la = len(audio)
        # audiosection_length = int(la / n_sections)
        # partitions = [np.mean(x) for x in util.part(audio, audiosection_length)]
        partitions = [np.mean(x) for x in util.split(audio, n_sections)]

    # sent = sent_sections[0:n_sections]
    # partitions = partitions[0:n_sections]

    with open(dest_path, "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        for index, item in enumerate(sent_sections):
            writer.writerow([item.get("valence"), item.get("arousal"), item.get("dominance"), partitions[index]])


def audiosent_scenes_wo_time(xml_path: str, audio_path: str, dest_path: str):
    sentiment = ImpalaSent()

    scenes = get_scenes_unannotated(xml_path)
    scenesentiment = [sentiment.score(" ".join(x)) for x in scenes]

    audio = []
    with open(audio_path) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            audio.append(float(row[1]))

        la = len(audio)
        # audiosection_length = int(la / len(scenes))
        partitions = [np.mean(x) for x in util.split(audio, len(scenes))]

    # scenesentiment = scenesentiment[0:len(scenes)]
    # partitions = partitions[0:len(scenes)]

    with open(dest_path, "a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)

        for index, item in enumerate(scenesentiment):
            writer.writerow([item.get("valence"), item.get("arousal"), item.get("dominance"), partitions[index]])

    # rho = stats.spearmanr(scenesentiment, partitions)
    # p = stats.pearsonr(scenesentiment, partitions)
    # tau = stats.kendalltau(scenesentiment, partitions)


def plot_audiosent(audio_csv: str, xml_path: str, scenelevel=True):
    if scenelevel:
        sentiment = scenesentiment_for_man_annotated(xml_path, "Warriner")
    else:
        sentiment = subtitle_sentiment(xml_path)

    sent_time = [s[0] for s in sentiment]
    arousal = [s[2].get("arousal") for s in sentiment]
    print(len(sent_time))

    audio_tuples = []
    with open(audio_csv) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            audio_tuples.append((float(row[0]), float(row[1])))

    audio_time = [a[0] for a in audio_tuples]
    audio = [a[1] for a in audio_tuples]
    print("Audio time: ", audio_time[-1])
    print("sentiment time: ", sent_time[-1])

    audio_windows = util.sliding_window(audio, 10)

    if scenelevel:
        sentiment_windows = arousal
    else:
        sentiment_windows = util.sliding_window(arousal, 10)

    fig, ax1 = plt.subplots()
    # fig.set_canvas(plt.gcf().canvas)
    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Audio Energy', color=color)
    ax1.semilogy(audio_time, audio_windows, color=color)
    # ax1.plot(audio_time, audio_windows, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Arousal', color=color)  # we already handled the x-label with ax1
    ax2.plot(sent_time, sentiment_windows, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    # fig.tight_layout()
    # plt.figure()
    # plt.subplot(311)
    # plt.title('Blade: Audio (RMS Energy)')
    # plt.xlabel("seconds")
    # plt.semilogy(times, audio)
    # # plt.plot(times, audio)
    # plt.xlim(0, times[-1])
    #
    # plt.subplot(312)
    # # plt.title('Blade: Audio (RMS Energy)')
    # plt.xlabel("seconds")
    # plt.semilogy(times, audio_windows)
    # # plt.plot(times, audio_windows)
    #
    # plt.xlim(0, times[-1])
    #
    # plt.subplot(313)
    # plt.xlabel("seconds")
    # plt.plot(time, sentiment_windows)
    # plt.xlim(0, time[-1])

    # plt.tight_layout()
    plt.show()
    # img_path = os.path.basename(xml_path).replace(".xml", ".png")
    # fig.savefig(img_path, dpi=300, format="png")


def main():
    time = datetime.now()

    for d in data_script:
        if "star" in d[0]:
            continue
        base = os.path.basename(d[1])
        # name = d[1].replace(base, "spectral_centroid/")+ base.replace(".csv", "_centroid.csv")
        # name = d[1].replace(base, "tuning/")+ base.replace(".csv", "_tuning.csv")
        name = d[1].replace(base, "energy/" + base)

        # audiosent_scenes_wo_time(d[0], d[1], "7mv_audiosent_scenes_wo_time_Warriner.csv")
        audiosent_csv(d[0], name, "7mv_audiosent_ohne_StarWars.csv", sent_method="Warriner")
        # fountain_audiosent_csv(d[0], d[1], 200, "7mv_fountain_audiosent.csv")

    time2 = datetime.now()
    diff = time2 - time

    print(diff)


if __name__ == '__main__':
    main()
