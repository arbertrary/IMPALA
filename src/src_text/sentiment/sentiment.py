"""The main sentiment class"""
import csv
import os
import re
import numpy as np
from nltk import word_tokenize

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


class ImpalaSent:
    def __init__(self, method="default"):
        if method == ("default" or "Warriner"):
            self.method = "RatingsWarriner"
            self.lexicon = warriner_dict()
        elif method == "SentiWordNet":
            self.method = "SentiWordNet"
            self.lexicon = sentiwordnet_dict()
        elif method == "NRC":
            self.method = "NRC"
            self.lexicon = nrc_dict()
        else:
            raise ValueError("Not a valid method!")

    def score(self, text: str):
        words = word_tokenize(text)

        valence_scores = []
        arousal_scores = []
        dominance_scores = []
        for word in words:
            score = self.lexicon.get(word.lower())

            if score:
                v = float(score[0])
                a = float(score[1])
                d = float(score[2])

                valence_scores.append(v)
                arousal_scores.append(a)
                dominance_scores.append(d)

        lv = len(valence_scores)
        la = len(arousal_scores)
        ld = len(dominance_scores)
        if lv == 0 or la == 0 or ld == 0:
            return -1, -1, -1
        else:
            valence = np.mean(valence_scores)

            # Variante 1: avg über die gesamte szene
            # arousal = np.mean(arousal_scores)

            # Variante 2: max der gesamten Szene
            arousal = np.max(arousal_scores)

            # variante 3: average des 75% percentile
            # perc = np.percentile(arousal_scores, 75)
            # temp = [x for x in arousal_scores if x > perc]
            # arousal = np.mean(temp)


            dominance = np.mean(dominance_scores)
            return valence, arousal, dominance

    def nrc_score(self, text: str):
        if self.method != "NRC":
            raise ValueError("Lexicon is not NRC")

        words = word_tokenize(text)

        scores = []
        for word in words:
            score = self.lexicon.get(word.lower())

            if score:
                scores.append(score)

        anger = ant = disgust = fear = joy = negative = positive = sadness = surprise = trust = 0
        emotions = np.array([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
        # emo_dict = {"anger": -1, "anticipation": -1, "disgust": -1, "fear": -1, "joy": -1, "negative": -1,
        #             "positive": -1, "sadness": -1, "surprise": -1, "trust": -1}
        word_count = len(scores)
        for dict in scores:
            if emotions[0] == -1:
                emotions[0] = dict.get("anger")
                emotions[1] = dict.get("anticipation")
                emotions[2] = dict.get("disgust")
                emotions[3] = dict.get("fear")
                emotions[4] = dict.get("joy")
                emotions[5] = dict.get("negative")
                emotions[6] = dict.get("positive")
                emotions[7] = dict.get("sadness")
                emotions[8] = dict.get("surprise")
                emotions[9] = dict.get("trust")
            else:
                emotions[0] += dict.get("anger")
                emotions[1] += dict.get("anticipation")
                emotions[2] += dict.get("disgust")
                emotions[3] += dict.get("fear")
                emotions[4] += dict.get("joy")
                emotions[5] += dict.get("negative")
                emotions[6] += dict.get("positive")
                emotions[7] += dict.get("sadness")
                emotions[8] += dict.get("surprise")
                emotions[9] += dict.get("trust")

        # print(emotions)
        emotions = [x / word_count if x != -1 else x for x in emotions]
        # print(emotions)
        # if emotions[0] == -1:
        #     return []
        # else:
        return emotions


def warriner_dict():
    path = os.path.join(BASE_DIR, "src/src_text/lexicons/", "WarrinerRatings.csv")

    lexicon = {}
    with open(path, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=",")

        for index, row in enumerate(data):
            if index == 0:
                continue
            else:
                word = row[1]
                valence = row[2]
                arousal = row[5]
                dominance = row[8]
                # temp = {"valence": valence, "arousal": arousal, "dominance": dominance}
                score = (valence, arousal, dominance)
                lexicon[word] = score

    return lexicon


def nrc_dict():
    path = os.path.join(BASE_DIR, "src/src_text/lexicons/", "NRC_EmoLex.txt")

    lexicon = {}
    with open(path, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter='\t')

        temp_dict = {}
        for index, line in enumerate(data):
            word = line[0]
            key = line[1]
            value = line[2]
            if index % 10 < 9:
                temp_dict[key] = int(value)
            else:
                temp_dict[key] = int(value)
                lexicon[word] = temp_dict
                temp_dict = {}

    return lexicon


def sentiwordnet_dict():
    path = os.path.join(BASE_DIR, "src/src_text/lexicons/", "SentiWordNet.txt")

    lexicon = {}
    with open(path, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter='\t')

        i = 1
        for index, line in enumerate(data):
            if line[0].startswith("#"):
                continue
            else:
                pos = float(line[2])
                neg = float(line[3])
                synset = re.sub(r"#\d", "", line[4]).split(" ")
                temp_dict = {"pos": pos, "neg": neg}

                for word in synset:
                    lexicon[word] = temp_dict
    return lexicon


def main():
    # test = ImpalaSent()
    # test = ImpalaSent("SentiWordNet")
    # test = ImpalaSent()
    # print(test.score("Hey, this really is a shit fucking sentence!"))

    # test2 = ImpalaSent("SentiWordNet")
    # print(test2.score("happy"))

    test3 = ImpalaSent("NRC")
    # print(test3.lexicon.get("happy"))
    # print(test3.lexicon.get("death"))
    print(test3.nrc_score('Take her away!'))
    # PAR_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))
    # DATA_DIR = os.path.join(PAR_DIR, "lexicons")
    # print(DATA_DIR)


if __name__ == '__main__':
    main()
