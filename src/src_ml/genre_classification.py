import pandas
import csv
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning)
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, f1_score


def nrc_cat():
    scores_33 = [0.056302, 0.076142, 0.037774, 0.071414, 0.056571, 0.132324, 0.141000, 0.062723, 0.045405,
                 0.085375]

    scores_66 = [0.069257, 0.090724, 0.047087, 0.089884, 0.075523, 0.150747, 0.164399, 0.073317, 0.053537, 0.100305]

    with open("nrc_random_genres.csv") as csvfile:
        reader = csv.reader(csvfile)

        with open("nrccategorical.csv", "w") as newfile:
            writer = csv.writer(newfile, delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerow(
                ["Movie", "Anger", "Anticipation", "Disgust", "Fear", "Joy", "Negative", "Positive", "Sadness",
                 "Surprise", "Trust", "Genre"])
            for index, row in enumerate(reader):
                newrow = []

                if index == 0:
                    continue
                else:
                    for i, cell in enumerate(row):
                        if i == 0 or i == 11:
                            continue
                        else:
                            c = float(cell)

                            if c <= scores_33[i - 1]:
                                value = -1
                            elif scores_33[i - 1] < c <= scores_66[i - 1]:
                                value = 0
                            else:
                                value = 1

                            newrow.append(value)

                    writer.writerow(
                        [row[0], newrow[0], newrow[1], newrow[2], newrow[3], newrow[4], newrow[5], newrow[6], newrow[7],
                         newrow[8], newrow[9], row[11]])


def vader_cat():
    neg_33 = 0.87

    neg_66 = 0.103

    pos_33 = 0.094
    pos_66 = 0.11404

    neu_33 = 0.785
    neu_66 = 0.809

    comp_33 = -0.999700
    comp_66 = 1.0

    with open("vader_random_genres.csv") as csvfile:
        reader = csv.reader(csvfile)

        with open("categorical.csv", "w") as newfile:
            writer = csv.writer(newfile, delimiter=',', quoting=csv.QUOTE_ALL)
            writer.writerow(["Movie", "Vader Neg", "Vader Pos", "Vader Neu", "Genre"])
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                else:
                    comp = float(row[1])
                    neg = float(row[2])
                    pos = float(row[3])
                    neu = float(row[4])
                    if neg <= neg_33:
                        neg_value = -1
                    elif neg > neg_33 and neg <= neg_66:
                        neg_value = 0
                    else:
                        neg_value = 1

                    if pos <= pos_33:
                        pos_value = -1
                    elif pos > pos_33 and pos <= pos_66:
                        pos_value = 0
                    else:
                        pos_value = 1

                    if neu <= neu_33:
                        neu_value = -1
                    elif neu > neu_33 and neu <= neu_66:
                        neu_value = 0
                    else:
                        neu_value = 1

                    writer.writerow([row[0], neg_value, pos_value, neu_value, row[5]])


def classify():
    # dataframe = pandas.read_csv("nrccategorical.csv")
    # dataframe = pandas.read_csv("categorical.csv")
    # dataframe = pandas.read_csv("vader_random_genres.csv")
    # dataframe = pandas.read_csv("nrc_random_genres.csv")
    dataframe = pandas.read_csv("warriner_random_genres.csv")
    dataset = dataframe.values
    # print(dataframe.describe(percentiles=[.33, .66]))
    # print(dataset)

    # nrc
    # X = dataset[:,1:10]
    # y = dataset[:,11]
    # print(y)

    # vader
    # X= dataset[:,1:5]
    # y=dataset[:,5]

    # vader_cat
    # X =dataset[:,1:4]
    # y = dataset[:,4]
    # # warriner
    X = dataset[:, 1:2]
    y = dataset[:, 2]

    testfilm = X[854]
    print(dataset[854])

    X_train, X_test, y_train, y_test = X[:700], X[700:], y[:700], y[700:]
    # y_train_comedy = (y_train == "Comedy")
    # y_test_comedy = (y_test == "Comedy")

    # sgd_clf = SGDClassifier(random_state=42)
    # sgd_clf.fit(X_train, y_train_comedy)

    # y_scores = sgd_clf.decision_function([testfilm])
    # y_some_digit_pred = (y_scores > 200)
    # print(y_scores)
    # print(y_some_digit_pred)

    import numpy as np

    # shuffle_index = np.random.permutation(699)
    # X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]

    from sklearn.linear_model import SGDClassifier

    sgd_clf = SGDClassifier(random_state=42)
    sgd_clf.fit(X_train, y_train)

    print(sgd_clf.predict([testfilm]))

    some_digit_scores = sgd_clf.decision_function([testfilm])
    print(some_digit_scores)
    print(sgd_clf.classes_)


def main():
    classify()
    # preprocess()
    # nrc_cat()


if __name__ == '__main__':
    main()
