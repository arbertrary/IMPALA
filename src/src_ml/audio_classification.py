import pandas
import numpy as np
import csv
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning)
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, f1_score

dataframe = pandas.read_csv("Warriner_Class.csv")
dataset = dataframe.values

X = dataset[:, :3]
# print(X)
y = dataset[:, 3]
# print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

print(len(X_train))

y_train_louder = (y_train == "loud")
print(len(y_train_louder))
y_test_louder = (y_test == "loud")

# clf = SGDClassifier(random_state=42)
# clf.fit(X_train, y_train_louder)
clf = SVC(C=1, kernel="linear")
clf.fit(X_train, y_train_louder)

# print(sgd_clf.predict([test_scene]))
y_pred = clf.predict(X_test)
print(confusion_matrix(y_test_louder, y_pred))
# print(f1_score(y_train_louder, y_train_pred))
# test = cross_val_score(sgd_clf, X_train, y_train_louder, cv=3, scoring="accuracy")
# print(test)
