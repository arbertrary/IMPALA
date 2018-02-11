"""Helper Script for writing CSV files for Genre classification
The "write_xy_csv calculate sentiment for all movie scripts"""

import os
import operator
import csv
import random
from collections import Counter
from datetime import datetime
from sentiment import ImpalaSent
from moviescript import get_all_sentences
from nltk import word_tokenize

# from nltk.sentiment.vader import SentimentIntensityAnalyzer

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


def write_new_csv():
    directory = os.path.join(BASE_DIR, "all_moviescripts")
    sentiment = ImpalaSent()
    with open("allgenres2.txt") as file:
        films = file.read().splitlines(keepends=False)
        with open("new_genres.csv", "w") as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            filewriter.writerow(["Movie", "hv", "mv", "lv", "ha", "ma", "la", "hd", "md", "ld", "Genre"])

            for f in films:
                temp = f.split(":")
                title = temp[0]
                genre = random.choice(temp[1].split(","))

                path = os.path.join(directory, title + ".txt")
                with open(path) as movie:
                    text = movie.read()
                    words = word_tokenize(text)
                    wordcount = 0

                    hv, mv, lv, ha, ma, la, hd, md, ld = 0, 0, 0, 0, 0, 0, 0, 0, 0

                    for word in words:
                        score = sentiment.lexicon.get(word.lower())
                        if score:
                            wordcount += 1
                            v = float(score[0])
                            a = float(score[1])
                            d = float(score[2])

                            if a <= 2.54:
                                la += 1
                            elif 2.54 < a <= 5.88:
                                ma += 1
                            elif a > 5.88:
                                ha += 1

                            if v <= 3.73:
                                lv += 1
                            elif 3.73 < v <= 6.39:
                                mv += 1
                            elif v > 6.39:
                                hv += 1

                            if d <= 3.85:
                                ld += 1
                            elif 3.85 < d <= 6.51:
                                md += 1
                            elif d > 6.51:
                                hd += 1
                filewriter.writerow(
                    [title, hv / wordcount, mv / wordcount, lv / wordcount, ha / wordcount, ma / wordcount,
                     la / wordcount, hd / wordcount, md / wordcount, ld / wordcount, genre])


def write_test_csv():
    """Selber genres als "spannend" oder nicht benennen und dann filme anhand des genres als spannend klassifizieren?
    nur zum testen"""
    spannend = ["Drama", "Thriller", "Crime", "Horror", "Action"]
    medium = ["Mystery", "Adventure", "Sci-Fi", "Western", "Fantasy", "War"]
    lw = ["Romance", "Sport", "Biography", "Genre", "Short", "Family", "History", "Music", "Film-Noir", "Comedy", "Musical", "Animation"]



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


def read_csv():
    # genres = {'Biography', 'Fantasy', 'Comedy', 'Short', 'War', 'History', 'Romance', 'Drama', 'Crime', 'Sci-Fi',
    #         'Mystery', 'Thriller', 'Musical', 'Family', 'Action', 'Western', 'Music', 'Horror', 'Adventure',
    #         'Animation'}
    counter = {'Drama': 247, 'Comedy': 138, 'Thriller': 104, 'Action': 81, 'Crime': 70, 'Horror': 49, 'Romance': 44,
               'Sci-Fi': 40, 'Adventure': 32, 'Mystery': 26, 'Fantasy': 21}

    genre_dict = {'Crime': [0], 'Comedy': [0], 'Action': [0], 'Drama': [0], 'Fantasy': [0], 'Sci-Fi': [0],
                  'Romance': [0],
                  'Horror': [0], 'Adventure': [0], 'Thriller': [0], 'Mystery': [0]}

    with open("new_genres.csv") as csvfile:
        reader = csv.reader(csvfile)

        test = []
        for index, row in enumerate(reader):
            if index == 0:
                print(row)
                continue
            else:
                genre = row[-1]

                if genre_dict.get(genre):
                    temp = [float(x) for x in row[1:-1]]

                    if len(genre_dict.get(genre)) == 1:
                        genre_dict[genre] = temp
                    else:
                        asdf = genre_dict.get(genre)

                        qwer = [sum(x) for x in zip(asdf, temp)]
                        genre_dict[genre] = qwer

    for item in genre_dict:
        print(item)
        temp = []
        for n in genre_dict.get(item):
            c = counter.get(item)
            temp.append("%.3f" % (n / c))
        print(temp)


def main():
    genre_dict = {'Drama': 500, 'Thriller': 323, 'Comedy': 281, 'Action': 245, 'Crime': 179, 'Romance': 154,
                  'Adventure': 135, 'Sci-Fi': 128, 'Horror': 120, 'Mystery': 88, 'Fantasy': 84, 'Family': 23,
                  'Animation': 22, 'War': 18, 'Musical': 15, 'Western': 11, 'Music': 5, 'Film-Noir': 3, 'History': 3,
                  'Short': 3, 'Biography': 3, 'Sport': 2, 'Genre': 1}
    print(len(genre_dict))
    random_genre_dict = {'Drama': 256, 'Comedy': 122, 'Thriller': 104, 'Action': 93, 'Crime': 64, 'Romance': 59,
                         'Horror': 44, 'Sci-Fi': 44, 'Adventure': 31, 'Mystery': 23, 'Fantasy': 23, 'Animation': 7,
                         'Musical': 5, 'Family': 5, 'Western': 4, 'War': 4, 'Music': 4, 'Short': 2, 'Genre': 1,
                         'Biography': 1}

    # with open("new_genres.csv") as csvfile:
    #     test = []
    #     reader = csv.reader(csvfile)
    #     for row in reader:
    #         test.append(row[-1])
    #
    #     counter = Counter(test)
    #     # if counter > 11:
    #     print(counter)
    #
    time = datetime.now()
    # test = [1,2,3,4]
    # print(test[1:-1])

    # write_new_csv()
    # read_csv()
    # edit_csv()
    # write_warriner_csv()
    time2 = datetime.now()
    diff = time2 - time

    print(diff)


if __name__ == '__main__':
    main()
