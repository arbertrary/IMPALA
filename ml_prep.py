import os
import csv
import numpy as np
import random
from datetime import datetime
from collections import Counter
from sentiment import ImpalaSent
from moviescript import get_all_sentences
from nltk.sentiment.vader import SentimentIntensityAnalyzer

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))


def write_vader_csv():
    directory = os.path.join(BASE_DIR, "data_xml")
    sid = SentimentIntensityAnalyzer()
    with open("allgenres2.txt") as file:
        films = file.read().splitlines(keepends=False)
        with open("test.csv", "w") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            filewriter.writerow(["Movie", "Vader Compound", "Vader Neg", "Vader Pos", "Vader Neu", "Genre"])

            for f in films:
                temp = f.split(":")
                name = temp[0]
                genres = temp[1]

                xml_path = os.path.join(directory, name + ".xml")
                sentences = get_all_sentences(xml_path)

                text = ""
                for s in sentences:
                    text += s[1] + " "
                score = sid.polarity_scores(text)

                filewriter.writerow(
                    [name, score.get("compound"), score.get("neg"), score.get("pos"), score.get("neu"), genres])


def write_nrc_csv():
    directory = os.path.join(BASE_DIR, "data_xml")
    sentiment = ImpalaSent("NRC")
    with open("allgenres2.txt") as file:
        films = file.read().splitlines(keepends=False)
        with open("nrc_genres.csv", "w") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            filewriter.writerow(["Movie", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Negative", "Positive",
                                 "Sadness", "Surprise", "Trust", "Genre"])

            for f in films:
                temp = f.split(":")
                name = temp[0]
                genres = temp[1].split(",")

                xml_path = os.path.join(directory, name + ".xml")
                sentences = get_all_sentences(xml_path)

                text = ""
                for s in sentences:
                    text += s[1] + " "
                score = sentiment.nrc_score(text)

                for g in genres:
                    filewriter.writerow(
                        [name, score[0], score[1], score[2], score[3], score[4], score[5], score[6], score[7], score[8],
                         score[9], g])


def write_warriner_csv():
    directory = os.path.join(BASE_DIR, "data_xml")
    sentiment = ImpalaSent()
    with open("allgenres2.txt") as file:
        films = file.read().splitlines(keepends=False)
        with open("warriner_genres.csv", "w") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            filewriter.writerow(["Movie", "Valence", "Arousal" "Genre"])

            for f in films:
                temp = f.split(":")
                name = temp[0]
                genres = temp[1].split(",")

                xml_path = os.path.join(directory, name + ".xml")
                sentences = get_all_sentences(xml_path)

                text = ""
                for s in sentences:
                    text += s[1] + " "
                scoreV, scoreA = sentiment.score(text)

                for g in genres:
                    filewriter.writerow(
                        [name, scoreV, scoreA, g])


def edit_csv():
    genre_dict = {'Drama': 500, 'Thriller': 323, 'Comedy': 281, 'Action': 245, 'Crime': 179, 'Romance': 154,
                  'Adventure': 135, 'Sci-Fi': 128, 'Horror': 120, 'Mystery': 88, 'Fantasy': 84, 'Family': 23,
                  'Animation': 22, 'War': 18, 'Musical': 15, 'Western': 11, 'Music': 5, 'Film-Noir': 3, 'History': 3,
                  'Short': 3, 'Biography': 3, 'Sport': 2, 'Genre': 1}

    film_main_genre = {}
    with open("allgenres2.txt") as all:
        films = all.read().splitlines(keepends=False)
        for f in films:
            temp = f.split(":")
            name = temp[0]
            genres = temp[1].split(",")
            genre = random.choice(genres)
            # genre_counts = [genre_dict[g] for g in genres]
            # i = np.argmax(genre_counts)
            # genre = genres[i]

            film_main_genre[name] = genre

    with open("nrc_genres.csv") as f:
        reader = csv.reader(f)
        genres = []
        current_film = ""

        with open("nrc_random_genres.csv", "w") as test2:
            filewriter = csv.writer(test2, delimiter=',', quoting=csv.QUOTE_ALL)
            # filewriter.writerow(["Movie", "Vader Compound", "Vader Neg", "Vader Pos", "Vader Neu", "Genre"])
            # filewriter.writerow(["Movie", "Valence", "Arousal" "Genre"])
            filewriter.writerow(["Movie", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Negative", "Positive",
                                 "Sadness", "Surprise", "Trust", "Genre"])
            done = []
            for row in reader:
                if row[0] != "Movie":
                    if row[0] not in done:
                        genre = film_main_genre.get(row[0])
                        # filewriter.writerow([row[0], row[1], row[2], row[3], row[4], genre])
                        # filewriter.writerow([row[0], row[1], row[2], genre])
                        filewriter.writerow(
                            [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                             genre])
                        done.append(row[0])
                    else:
                        continue


def main():
    genre_dict = {'Drama': 500, 'Thriller': 323, 'Comedy': 281, 'Action': 245, 'Crime': 179, 'Romance': 154,
                  'Adventure': 135, 'Sci-Fi': 128, 'Horror': 120, 'Mystery': 88, 'Fantasy': 84, 'Family': 23,
                  'Animation': 22, 'War': 18, 'Musical': 15, 'Western': 11, 'Music': 5, 'Film-Noir': 3, 'History': 3,
                  'Short': 3, 'Biography': 3, 'Sport': 2, 'Genre': 1}

    random_genre_dict = {'Drama': 256, 'Comedy': 122, 'Thriller': 104, 'Action': 93, 'Crime': 64, 'Romance': 59,
                         'Horror': 44, 'Sci-Fi': 44, 'Adventure': 31, 'Mystery': 23, 'Fantasy': 23, 'Animation': 7,
                         'Musical': 5, 'Family': 5, 'Western': 4, 'War': 4, 'Music': 4, 'Short': 2, 'Genre': 1,
                         'Biography': 1}

    most_frequent_genre_dict = {'Drama': 500, 'Thriller': 162, 'Comedy': 150, 'Action': 57, 'Horror': 12,
                                'Adventure': 6, 'Western': 2, 'Romance': 2, 'Genre': 1, 'Crime': 1, 'Short': 1,
                                'Family': 1, 'Sci-Fi': 1}

    # with open("test2.csv") as csvfile:
    #     test = []
    #     reader = csv.reader(csvfile)
    #     for row in reader:
    #         test.append(row[-1])
    #
    #     counter = Counter(test)
    #     print(counter)

    time = datetime.now()

    edit_csv()
    # write_warriner_csv()
    time2 = datetime.now()
    diff = time2 - time

    print(diff)


if __name__ == '__main__':
    main()
