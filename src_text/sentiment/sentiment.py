import csv
import os
import re
from nltk import word_tokenize
from numpy import mean

PAR_DIR = os.path.abspath(os.path.join(os.curdir, os.pardir))
DATA_DIR = os.path.join(PAR_DIR, "lexicons")


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

        val = []
        aro = []
        for word in words:
            score = self.lexicon.get(word)

            if score:
                a = float(score[1])
                v = float(score[0])

                # if v < 5.06 and a > 4.21:
                val.append(v)
                aro.append(a)

        if len(val) != 0 and len(aro) != 0:
            valence = mean(val)
            arousal = mean(aro)
            # return valence, arousal
        elif len(val) != 0 and len(aro) == 0:
            valence = mean(val)
            arousal = 0

        elif len(val) == 0 and len(aro) != 0:
            valence = 0
            arousal = mean(aro)
        else:
            valence = 0
            arousal = 0

            # return None

        # print(valence, arousal)
        return valence, arousal


def warriner_dict():
    path = os.path.join(DATA_DIR, "WarrinerRatings.csv")

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
                temp = (valence, arousal, dominance)
                lexicon[word] = temp

    return lexicon


def nrc_dict():
    path = os.path.join(DATA_DIR, "NRC_EmoLex.txt")

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
                temp_dict[key] = value
                lexicon[word] = temp_dict
                temp_dict = {}

    return lexicon


def sentiwordnet_dict():
    path = os.path.join(DATA_DIR, "SentiWordNet.txt")

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
    test = ImpalaSent()
    print(test.score("Hey, this really is a shit fucking sentence!"))

    # test2 = ImpalaSent("SentiWordNet")
    # print(test2.score("happy"))

    # test3 = ImpalaSent("NRC")
    # print(test3.score("happy"))


if __name__ == '__main__':
    main()
