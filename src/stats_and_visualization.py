import os
import matplotlib.pyplot as plt
import src.src_text.preprocessing.moviescript as ms
import src.src_text.preprocessing.subtitles as subs
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import src.utility as util
from wordcloud import WordCloud
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from src.src_text.sentiment.sentiment import ImpalaSent
from src.src_text.sentiment.ms_sentiment import plaintext_sentiment
from src import data_script, data_fountain, data_subs

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def audio_stufftemp(audio_path):
    with open(audio_path) as csvfile:
        reader = csv.reader(csvfile)

        audio = []
        for row in reader:
            audio.append(float(row[-1]))

        audio = [np.mean(a) for a in util.split(audio, 5)]
        # print(audio)
        # print(audio)
        plt.plot(audio)
        plt.show()


def section_sentiment(fountain_path):
    fountain_dir = os.path.join(BASE_DIR, "data/moviescripts_fountain")
    last_v_smallest = 0
    last_v_not_smallest = 0

    last_d_smallest = 0
    last_d_not_smallest = 0

    aro_greatest = 0
    aro_not = 0
    genre_dict = {}

    with open(os.path.join(BASE_DIR, "allgenres2.txt")) as genrefile:
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
    # i = 1
    for script in os.listdir(fountain_dir):
        # if i == 10:
        #     break
        # i+=1
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

    print("ende mehr arousal als erste section:", aro_greatest, "filme")
    print("Genres:", Counter(aro_bad_genres))
    print("\n")
    print("ende nicht mehr arousal:", aro_not, "filme")
    print("Genres:", Counter(aro_good_genres))
    print("\n")
    print("ende weniger valence als erste section:", last_v_smallest, "filme")
    print("Genres:", Counter(val_bad_genres))
    print("\n")
    print("ende nicht weniger valence:", last_v_not_smallest, "filme")
    print("Genres:", Counter(val_good_genres))
    print("\n")
    print("ende weniger dominance als erste section:", last_d_smallest, "filme")
    print("Genres:", Counter(dom_bad_genres))
    print("\n")
    print("ende nicht weniger dominance als erste section:", last_d_not_smallest, "filme")
    print("Genres:", Counter(dom_good_genres))

    # test = plaintext_sentiment(fountain_path, 10)
    # print(len(test))
    #
    # arousal = [x.get("arousal") for x in test]
    # plt.plot(arousal)
    # plt.show()


def section_audio():
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


def word_count(xml_path):
    sentiment = ImpalaSent()

    stop = stopwords.words("english")
    chars = ms.get_characters(xml_path)
    # sentences = ms.get_all_sentences(xml_path)
    # text = " ".join(sentences)

    sentences = subs.get_subtitles(data_subs[5][0])
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


def warriner_wordcloud(xml_path):  # , subs_path):
    sentiment = ImpalaSent()

    stop = stopwords.words("english")
    high = []
    medium = []
    low = []
    # directory = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually")
    # directory = os.path.join(BASE_DIR, "data/moviescripts_xml_time")
    directory = os.path.join(BASE_DIR, "data/moviescripts_xml")

    for file in os.listdir(directory):
        xml_path = os.path.join(directory, file)
        chars = ms.get_characters(xml_path)
        sentences = ms.get_all_sentences(xml_path)
        text = " ".join(sentences)

        # sentences = subs.get_subtitles(subs_path)
        # text = " ".join([x[-1] for x in sentences])


        words = []
        sent = "dominance"
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
    wc1 = WordCloud(background_color="white",width=800, height=450,collocations=False).generate(" ".join(high))
    wc2 = WordCloud(background_color="white",width=800, height=450,collocations=False).generate(" ".join(medium))
    wc3 = WordCloud(background_color="white",width=800, height=450,collocations=False).generate(" ".join(low))

    wc1.to_file("high_"+sent+".png")
    wc2.to_file("medium_"+sent+".png")
    wc3.to_file("low_"+sent+".png")

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
    path = os.path.join(BASE_DIR, "data/audiosent_csv_raw/7mv_audiosent_normalized_Warriner.csv")
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

    plt.suptitle("Histograms for Sentiment and Audio of 7 movies (1162 scenes)")
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
    # img_path = "histogram.png"
    # plt.savefig(img_path, dpi=300)


def regression_plot(csvfile, x):
    """In the simplest invocation, both functions draw a scatterplot of two variables, x and y,
    and then fit the regression model y ~ x
    and plot the resulting regression line and a 95% confidence interval for that regression:"""
    dataframe = pd.read_csv(csvfile)
    # print(dataframe)
    plt.figure()
    sns.regplot(y="Audio Energy", x=x, data=dataframe)
    plt.title("Scatter Plot with Regression line for 1162 scenes from 7 movies")
    plt.tight_layout()
    plt.show()


def main():
    # histograms()
    # warriner_wordcloud("/home/armin/Studium/Bachelor/CodeBachelorarbeit/IMPALA/src/testfiles/blade_manually.xml")
    regression_plot(os.path.join(BASE_DIR, "data/audiosent_csv_raw/single movies/indiana-jones-3_ger_audiosent_Warriner.csv"), "Arousal")


if __name__ == '__main__':
    main()
