import os
import matplotlib.pyplot as plt
import src.src_text.preprocessing.moviescript as ms
import src.src_text.preprocessing.subtitles as subs
import csv
import numpy as np
import src.utility as util
from wordcloud import WordCloud
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from src.src_text.sentiment.sentiment import ImpalaSent
from src.src_text.sentiment.ms_sentiment import plaintext_sentiment

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))

script1 = os.path.join(BASE_DIR, "data/manually_annotated", "blade_man.xml")
script2 = os.path.join(BASE_DIR, "data/manually_annotated", "hellboy_man.xml")
script3 = os.path.join(BASE_DIR, "data/manually_annotated", "predator_man.xml")
script4 = os.path.join(BASE_DIR, "data/manually_annotated", "scream_man.xml")
script5 = os.path.join(BASE_DIR, "data/manually_annotated", "star-wars-4_man.xml")
script6 = os.path.join(BASE_DIR, "data/manually_annotated", "the-matrix_man.xml")

subs1 = os.path.join(BASE_DIR, "data/data_subtitles/", "blade_subs.xml")
subs2 = os.path.join(BASE_DIR, "data/data_subtitles/", "hellboy_subs.xml")
subs3 = os.path.join(BASE_DIR, "data/data_subtitles/", "predator_subs.xml")
subs4 = os.path.join(BASE_DIR, "data/data_subtitles/", "scream_subs.xml")
subs5 = os.path.join(BASE_DIR, "data/data_subtitles/", "star-wars-4_subs.xml")
subs6 = os.path.join(BASE_DIR, "data/data_subtitles/", "the-matrix_subs.xml")

fountain1 = os.path.join(BASE_DIR, "data/all_moviescripts", "blade.txt")
fountain2 = os.path.join(BASE_DIR, "data/all_moviescripts", "hellboy.txt")
fountain3 = os.path.join(BASE_DIR, "data/all_moviescripts", "predator.txt")
fountain4 = os.path.join(BASE_DIR, "data/all_moviescripts", "scream.txt")
fountain5 = os.path.join(BASE_DIR, "data/all_moviescripts", "star-wars-4.txt")
fountain6 = os.path.join(BASE_DIR, "data/all_moviescripts", "the-matrix.txt")

audio1 = os.path.join(BASE_DIR, "data/audio_csvfiles", "blade.csv")
audio2 = os.path.join(BASE_DIR, "data/audio_csvfiles", "hellboy.csv")
audio3 = os.path.join(BASE_DIR, "data/audio_csvfiles", "predator.csv")
audio4 = os.path.join(BASE_DIR, "data/audio_csvfiles", "scream_ger.csv")
audio5 = os.path.join(BASE_DIR, "data/audio_csvfiles", "star-wars-4.csv")
audio6 = os.path.join(BASE_DIR, "data/audio_csvfiles", "the-matrix.csv")

data = [fountain1, fountain2, fountain3, fountain4, fountain5, fountain6]
data2 = [script1, script2, script3, script4, script5, script6]
data3 = [(subs1, script1), (subs2, script2), (subs3, script3), (subs4, script4), (subs5, script5), (subs6, script6)]


def audio_stufftemp(audio_path):
    with open(audio_path) as csvfile:
        reader = csv.reader(csvfile)

        audio = []
        for row in reader:
            audio.append(float(row[-1]))

        audio = len()


def section_sentiment(fountain_path):
    fountain_dir = os.path.join(BASE_DIR, "data/all_moviescripts")
    last_v_smallest = 0
    last_v_not_smallest = 0

    last_d_smallest = 0
    last_d_not_smallest = 0

    aro_greatest = 0
    aro_not = 0

    for script in os.listdir(fountain_dir):
        path = os.path.join(fountain_dir, script)
        print(path)
        test = plaintext_sentiment(path, 5)
        arousal = [x.get("arousal") for x in test]
        valence = [x.get("valence") for x in test]
        dominance = [x.get("dominance") for x in test]

        if arousal[-1] > arousal[0]:
            aro_greatest += 1
        elif arousal[-1] != np.max(arousal):
            aro_not += 1

        if valence[-1] < valence[0]:
            last_v_smallest += 1
        elif valence[-1] != np.min(valence):
            last_v_not_smallest += 1

        if dominance[-1] < dominance[0]:
            last_d_smallest += 1
        elif dominance[-1] != np.min(dominance):
            last_d_not_smallest += 1

    print("ende mehr arousal als erste section:", aro_greatest, "filme")
    print("ende nicht mehr arousal:", aro_not, "filme")

    print("ende weniger valence als erste section:", last_v_smallest, "filme")
    print("ende nicht weniger valence:", last_v_not_smallest, "filme")

    print("ende weniger dominance als erste section:", last_d_smallest, "filme")
    print("ende nicht weniger dominance als erste section:", last_d_not_smallest, "filme")

    # test = plaintext_sentiment(fountain_path, 10)
    # print(len(test))
    #
    # arousal = [x.get("arousal") for x in test]
    # plt.plot(arousal)
    # plt.show()


def word_count(xml_path):
    sentiment = ImpalaSent()

    stop = stopwords.words("english")
    chars = ms.get_characters(xml_path)
    # sentences = ms.get_all_sentences(xml_path)
    # text = " ".join(sentences)

    sentences = subs.get_subtitles(subs6)
    text = " ".join([x[-1] for x in sentences])

    test = []
    for word in word_tokenize(text):
        score = sentiment.lexicon.get(word.lower())
        if score and word.lower() not in stop and word.lower() not in chars:
            # test.append(word.lower())
            test.append((word.lower(), score.get("arousal")))
    c = Counter(test)

    print(c)
    test = set(test)

    temp = [(x[0], c.get(x), x[1]) for x in test]
    test = sorted(temp, key=lambda x: (-x[1], -x[2]))
    print(test)


def warriner_wordcloud(xml_path):
    sentiment = ImpalaSent()

    stop = stopwords.words("english")
    chars = ms.get_characters(xml_path)
    sentences = ms.get_all_sentences(xml_path)
    text = " ".join(sentences)

    words = []
    for word in word_tokenize(text):
        score = sentiment.lexicon.get(word.lower())
        if score and word.lower() not in stop and word.lower() not in chars:
            words.append(word)

    wordcloud = WordCloud().generate(" ".join(words))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def histograms():
    path = os.path.join(BASE_DIR, "data/audiosent_csv_raw/6mv_raw_mean_audio_normalized_Warriner.csv")
    # path = os.path.join(BASE_DIR, "data/audiosent_csv_raw/6mv_raw_mean_audio_Vader.csv")

    with open(path) as csvfile:
        reader = csv.reader(csvfile)

        valence = []
        arousal = []
        dominance = []
        audio = []

        for row in reader:
            if row[0] == "Scene Start":
                continue
            valence.append(float(row[2]))
            arousal.append(float(row[3]))
            dominance.append(float(row[4]))
            audio.append(float(row[-1]))

    plt.suptitle("Histograms for Sentiment and Audio of 6 movies (1027 scenes)")
    plt.subplot(221)
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.title("Valence")
    plt.hist(valence)
    plt.subplot(222)
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.title("Arousal")
    plt.hist(arousal)
    plt.subplot(223)
    plt.hist(dominance)
    plt.xlabel("Score")
    plt.ylabel("Count")
    plt.title("Dominance")
    plt.subplot(224)
    plt.xlabel("Audio Energy")
    plt.ylabel("Count")
    plt.title("Audio")
    plt.hist(audio)

    plt.show()


def main():
    # word_count(script1)
    # word_count(script2)
    # word_count(script3)
    # word_count(script4)
    # word_count(script5)
    # word_count(script6)
    # histograms()

    # for d in data:
    #     section_sentiment(d)
    section_sentiment(fountain1)


if __name__ == '__main__':
    main()
