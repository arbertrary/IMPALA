import pandas
import csv
import numpy as np
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning)
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import KFold, train_test_split
from sklearn.model_selection import cross_validate, cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.base import clone


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


def classify_comedy():
    # Jeder film hat 9 werte
    # z.B. für Valence: 29% der gefundenen wörter sind positiv, 63% der wörter sind eher neutral, 8% sind negativ usw
    dataframe = pandas.read_csv("new_genres.csv")
    dataset = dataframe.values

    X = dataset[:, 1:10]
    y = dataset[:, 10]
    # print(X)
    # print(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    y_train_comedy = (y_train == "Comedy")
    y_test_comedy = (y_test == "Comedy")

    sgd_clf = SGDClassifier(random_state=42)
    sgd_clf.fit(X_train, y_train_comedy)

    # print(cross_val_score(sgd_clf, X_train, y_train_comedy, cv=3, scoring="accuracy"))

    y_pred = cross_val_predict(sgd_clf, X_test, y_test_comedy, cv=3)
    print(confusion_matrix(y_test_comedy, y_pred))
    print(precision_score(y_test_comedy, y_pred))
    print(recall_score(y_test_comedy, y_pred))
    print(f1_score(y_test_comedy, y_pred))


def classify_comedy_kfold():
    # Jeder film hat 9 werte
    # z.B. für Valence: 29% der gefundenen wörter sind positiv, 63% der wörter sind eher neutral, 8% sind negativ usw
    dataframe = pandas.read_csv("new_genres.csv")
    dataset = dataframe.values

    X = dataset[:, 1:10]
    y = dataset[:, 10]
    # print(X)
    # print(y)

    y_comedy = (y == "Comedy")
    sgd_clf = SGDClassifier(random_state=4)
    f1scores = []
    kf = KFold(n_splits=10)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train_comedy, y_test_comedy = y_comedy[train_index], y_comedy[test_index]
        sgd_clf.fit(X_train, y_train_comedy)
        y_pred = sgd_clf.predict(X_test)

        # print(confusion_matrix(y_test_comedy, y_pred))
        # print(precision_score(y_test_comedy, y_pred))
        # print(recall_score(y_test_comedy, y_pred))
        # print(f1_score(y_test_comedy, y_pred))
        f1scores.append(f1_score(y_test_comedy, y_pred))

    print(np.mean(f1scores))


def main():
    classify_comedy()
    # classify_comedy_kfold()


if __name__ == '__main__':
    main()
