"""Several functions to visualize sentiment and audio.
Mostly single-use functions"""

import os
import matplotlib.pyplot as plt
import src.src_text.preprocessing.moviescript as ms
import csv
import numpy as np
import pandas as pd
import src.utility as util
from wordcloud import WordCloud
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from src.src_text.sentiment.sentiment import SentimentClass
from src.src_text.sentiment.ms_sentiment import plaintext_sentiment, scenesentiment_man_annotated
from src.src_text.sentiment.subs_sentiment import subtitle_sentiment

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def section_sentiment():
    """
    single use function and not really reusable for other things
    Analyzes all fountain movie scripts split into (currently) 5 sections
    whether the sentiment in the first section is higher/lower than in the last section.
    prints the number of movies where either of this is tru
    and prints a "Counter" Dict of the genres for each case.
    """
    fountain_dir = os.path.join(BASE_DIR, "data/moviescripts_fountain")
    last_v_smallest = 0
    last_v_not_smallest = 0

    last_d_smallest = 0
    last_d_not_smallest = 0

    aro_greatest = 0
    aro_not = 0
    genre_dict = {}

    with open(os.path.join(BASE_DIR, "data/allgenres.txt")) as genrefile:
        genres = genrefile.read().splitlines(keepends=False)
        for g in genres:
            temp = g.split(":")
            genre_dict[temp[0]] = temp[1].split(",")

    aro_good_genres = []
    aro_bad_genres = []

    val_good_genres = []
    val_bad_genres = []

    dom_good_genres = []
    dom_bad_genres = []
    for script in os.listdir(fountain_dir):
        path = os.path.join(fountain_dir, script)
        print(path)
        test = plaintext_sentiment(path, 5)
        arousal = [x.get("arousal") for x in test]
        valence = [x.get("valence") for x in test]
        dominance = [x.get("dominance") for x in test]

        name = script.replace(".txt", "")

        if arousal[-1] > arousal[0]:
            aro_greatest += 1
            for g in genre_dict.get(name):
                aro_bad_genres.append(g)

        elif arousal[-1] <= arousal[0]:
            for g in genre_dict.get(name):
                aro_good_genres.append(g)
            aro_not += 1

        if valence[-1] < valence[0]:
            last_v_smallest += 1
            for g in genre_dict.get(name):
                val_bad_genres.append(g)
        elif valence[-1] >= valence[0]:
            last_v_not_smallest += 1
            for g in genre_dict.get(name):
                val_good_genres.append(g)

        if dominance[-1] < dominance[0]:
            last_d_smallest += 1
            for g in genre_dict.get(name):
                dom_bad_genres.append(g)
        elif dominance[-1] >= dominance[0]:
            last_d_not_smallest += 1
            for g in genre_dict.get(name):
                dom_good_genres.append(g)

    print("Last section higher arousal than first section:", aro_greatest, "filme")
    print("Genres:", Counter(aro_bad_genres))
    print("\n")
    print("Last section lower arousal than first section:", aro_not, "filme")
    print("Genres:", Counter(aro_good_genres))
    print("\n")
    print("Last section lower valence than first section:", last_v_smallest, "filme")
    print("Genres:", Counter(val_bad_genres))
    print("\n")
    print("Last section higher valence than first section:", last_v_not_smallest, "filme")
    print("Genres:", Counter(val_good_genres))
    print("\n")
    print("Last section lower dominance than first section:", last_d_smallest, "filme")
    print("Genres:", Counter(dom_bad_genres))
    print("\n")
    print("Last section higher dominance than first section:", last_d_not_smallest, "filme")
    print("Genres:", Counter(dom_good_genres))


def section_audio():
    """Analyzes audio csvfiles (split into 5 sections)
    whether the audio energy in the last section is higher than in the first section"""
    newdir = os.path.join(BASE_DIR, "data/audio_csvfiles")
    yes = 0
    no = 0

    for file in os.listdir(newdir):
        path = os.path.join(newdir, file)

        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            audio = []
            for row in reader:
                audio.append(float(row[-1]))
        audio = [np.mean(x) for x in util.split(audio, 5)]

        if audio[-1] > audio[0]:
            yes += 1
        else:
            no += 1

    print("audio in last section louder than in first section: ", yes, "filme")
    print("audio in last section more silent than in first section: ", no, "filme")


def warriner_wordcloud(sentiment_dimension: str):
    """Prints word clouds for chosen sentiment dimension
    and the text of xml movie scripts.
    Currently hard coded for the seven manually annotated movie scripts"""
    sentiment = SentimentClass()

    stop = stopwords.words("english")
    high = []
    medium = []
    low = []
    directory = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually")
    # directory = os.path.join(BASE_DIR, "data/moviescripts_xml_time")
    # directory = os.path.join(BASE_DIR, "data/moviescripts_xml")

    for file in os.listdir(directory):
        xml_path = os.path.join(directory, file)
        chars = ms.get_characters(xml_path)
        sentences = ms.get_all_sentences(xml_path)
        text = " ".join(sentences)

        words = []
        sent = sentiment_dimension
        for w in word_tokenize(text):
            word = w.lower()
            score = sentiment.lexicon.get(word)
            if score and word not in stop and word not in chars:
                if score.get(sent) < 3.67:
                    low.append(word)
                elif 3.67 <= score.get(sent) < 6.33:
                    medium.append(word)
                else:
                    high.append(word)

                words.append(word)

    c = Counter(high)
    print(c)
    wc1 = WordCloud(colormap="ocean", background_color="white", width=800, height=450, collocations=False).generate(
        " ".join(high))
    wc2 = WordCloud(colormap="ocean", background_color="white", width=800, height=450, collocations=False).generate(
        " ".join(medium))
    wc3 = WordCloud(colormap="ocean", background_color="white", width=800, height=450, collocations=False).generate(
        " ".join(low))

    # wc1.to_file("high_" + sent + ".png")
    # wc2.to_file("medium_" + sent + ".png")
    # wc3.to_file("low_" + sent + ".png")

    plt.figure()
    plt.subplot(311)
    plt.imshow(wc1, interpolation="bilinear")
    plt.axis("off")
    plt.subplot(312)
    plt.imshow(wc2, interpolation="bilinear")
    plt.axis("off")
    plt.subplot(313)
    plt.imshow(wc3, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def histograms():
    """Shows histograms of Valence, Arousal, Dominance and Audio Energy.
    Currently hardcoded to one csv file containing sentiment and audio information
    from 7 movies/1160 scenes"""
    path = os.path.join(BASE_DIR, "data/audiosentiment_csvfiles/7mv_audiosent_all.csv")

    df = pd.read_csv(path)
    valence = df.get("Valence").values
    arousal = df.get("Arousal").values
    dominance = df.get("Dominance").values
    audio = df.get("Audio Energy").values

    plt.suptitle("Histograms for Sentiment and Audio of 7 movies (1160 scenes)")
    plt.subplot(221)
    plt.xlabel("Score")
    plt.ylabel("# of data points")
    plt.title("Valence")
    plt.hist(valence)
    plt.subplot(222)
    plt.xlabel("Score")
    plt.ylabel("# of data points")
    plt.title("Arousal")
    plt.hist(arousal)
    plt.subplot(223)
    plt.hist(dominance)
    plt.xlabel("Score")
    plt.ylabel("# of data points")
    plt.title("Dominance")
    plt.subplot(224)
    plt.xlabel("Audio Energy")
    plt.ylabel("# of data points")
    plt.title("Audio")
    plt.hist(audio)

    plt.tight_layout()
    plt.show()


def plot_audiosent(audio_csv: str, xml_path: str, sentiment_dimension: str = "arousal", scenelevel=True):
    """Plots the audio energy from a audio csv file
    and a sentiment dimension from a xml file (either subtitles or movie script)
    and plots it in the same figure"""
    if scenelevel:
        sentiment = scenesentiment_man_annotated(xml_path, "Warriner")
    else:
        sentiment = subtitle_sentiment(xml_path)

    sent_time = [s[0] for s in sentiment]
    arousal = [s[2].get(sentiment_dimension) for s in sentiment]
    print(len(sent_time))

    audio_tuples = []
    with open(audio_csv) as audio_csv:
        reader = csv.reader(audio_csv)
        for row in reader:
            if row[0] == "Time":
                continue
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
    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Audio Energy', color=color)
    ax1.semilogy(audio_time, audio_windows, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Arousal', color=color)  # we already handled the x-label with ax1
    ax2.plot(sent_time, sentiment_windows, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.show()
