import os
import csv
from datetime import datetime

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
            filewriter.writerow(["Movie", "Vader Compound", "Vader Neg", "Vader Pos", "Vader Neu", "Genres"])

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

def read_csv():
    with open("test.csv") as f:
        reader = csv.reader(f)
        # for row in reader:
        #     genres = row[1].split(",")
        #     print(genres)

        with open("new.csv", "w") as new:
            writer = csv.writer(new, delimiter=",", quoting=csv.QUOTE_ALL)
            writer.writerow(["Movie", "Vader Compound", "Vader Neg", "Vader Pos", "Vader Neu", "Genre"])
            for row in reader:
                genres = row[1].split(",")
                for g in genres:
                    writer.writerow([row[0], row[2], row[3], row[4], row[5], g])


def main():
    time = datetime.now()

    # write_csv()
    # read_csv()
    write_warriner_csv()
    time2 = datetime.now()
    diff = time2 - time

    print(diff)


if __name__ == '__main__':
    main()
