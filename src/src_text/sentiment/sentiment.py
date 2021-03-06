"""The main sentiment module"""
import csv
import os
import re
import numpy as np
from nltk import word_tokenize

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir, os.pardir))


class SentimentClass:
    """The main Sentiment Class. Instantiated with a sentiment method and a lexicon.
    :param method: The sentiment method. Either Warriner, NRC or SentiWordNet.
    """

    def __init__(self, method="Warriner"):
        if method == "Warriner":
            self.method = "Warriner"
            self.lexicon = warriner_dict()
        elif method == "SentiWordNet":
            self.method = "SentiWordNet"
            self.lexicon = sentiwordnet_dict()
        elif method == "NRC":
            self.method = "NRC"
            self.lexicon = nrc_dict()
        else:
            raise ValueError("Not a valid method!")

    def score(self, text: str, **kwargs):
        """:returns Dict with key= valence, arousal or dominance and value= avg of all values in text
                if no word in text is found in the Warriner lexicon, return -1 for each value
            :raises ValueError if used with an SentimentClass instance with a sentiment lexicon other than Warriner"""
        if self.method != "Warriner":
            raise ValueError(
                "Tried getting the Warriner score from an instance of SentimentClass with a different lexicon")
        words = word_tokenize(text)

        valence_scores = []
        arousal_scores = []
        dominance_scores = []
        for word in words:
            if kwargs.get("stopwords") and word.lower() in kwargs.get("stopwords"):
                continue

            score = self.lexicon.get(word.lower())
            if score:
                v = score.get("valence")
                a = score.get("arousal")
                d = score.get("dominance")

                valence_scores.append(v)
                arousal_scores.append(a)
                dominance_scores.append(d)

        lv = len(valence_scores)
        la = len(arousal_scores)
        ld = len(dominance_scores)
        if lv == 0 or la == 0 or ld == 0:
            return {"valence": -1, "arousal": -1, "dominance": -1}
        else:
            valence = np.mean(valence_scores)
            arousal = np.mean(arousal_scores)
            dominance = np.mean(dominance_scores)
            sent_dict = {"valence": valence, "arousal": arousal, "dominance": dominance}
            return sent_dict

    def nrc_score(self, text: str):
        """:returns Dict with key= NRC emotion and value= avg of all emotion values in text
        if no word in text is found in NRC lexicon, return -1 for each value
           :raises ValueError if used with an SentimentClass instance with a sentiment lexicon other than NRC"""

        if self.method != "NRC":
            raise ValueError("Tried to get the NRC score from an instance of SentimentClass with a different lexicon")

        words = word_tokenize(text)

        scores = []
        for word in words:
            score = self.lexicon.get(word.lower())

            if score:
                scores.append(score)

        emo_dict = {"anger": -1, "anticipation": -1, "disgust": -1, "fear": -1, "joy": -1, "negative": -1,
                    "positive": -1, "sadness": -1, "surprise": -1, "trust": -1}
        word_count = len(scores)
        if word_count == 0:
            return emo_dict
        else:
            for d in scores:
                for emo in emo_dict:
                    if emo_dict.get(emo) == -1:
                        emo_dict[emo] = d.get(emo)
                    else:
                        emo_dict[emo] += d.get(emo)

            for emo in emo_dict:
                value = emo_dict.get(emo)
                emo_dict[emo] = value / word_count

            return emo_dict


def warriner_dict():
    """Parses the Warriner Ratings sentiment lexicon to a dict"""
    path = os.path.join(BASE_DIR, "src/src_text/sentiment/lexicons/", "WarrinerRatings.csv")

    lexicon = {}
    with open(path, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=",")

        for index, row in enumerate(data):
            if index == 0:
                continue
            else:
                word = row[1]
                valence = float(row[2])
                arousal = float(row[5])
                dominance = float(row[8])
                score = {"valence": valence, "arousal": arousal, "dominance": dominance}
                lexicon[word] = score

    return lexicon


def nrc_dict():
    """Parses the NRC EmoLex sentiment lexicon to a dict"""

    path = os.path.join(BASE_DIR, "src/src_text/sentiment/lexicons/", "NRC_EmoLex.txt")

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
    """Parses the SentiWordNet sentiment lexicon to a dict"""

    path = os.path.join(BASE_DIR, "src/src_text/sentiment/lexicons/", "SentiWordNet.txt")

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
