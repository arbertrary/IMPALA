import csv
import os
import re

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

    def score(self, word: str):
        return self.lexicon[word]


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
                temp = {"valence": valence, "arousal": arousal, "dominance": dominance}
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
    test = ImpalaSent()
    print(test.score("able"))

    test2 = ImpalaSent("SentiWordNet")
    print(test2.score("able"))

    test3 = ImpalaSent("NRC")
    print(test3.score("able"))



if __name__ == '__main__':
    main()
