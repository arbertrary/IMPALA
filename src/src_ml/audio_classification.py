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
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, f1_score

dataframe = pandas.read_csv("Warriner_Class.csv")
dataset = dataframe.values

X = dataset[:,:3]
# print(X)
y = dataset[:,3]
# print(y)

X_train, X_test, y_train, y_test = X[:800], X[800:], y[:800], y[800:]

# shuffle_index = np.random.permutation(800)
# X_train, y_train = X_train[shuffle_index], y_train[shuffle_index]

y_train_louder = (y_train == "loud")
y_test_louder = (y_test == "loud")

test_scene = X_test[90]
print(test_scene)
print(y_test[90])

sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train, y_train_louder)

# print(sgd_clf.predict([test_scene]))
y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_louder, cv=3)
print(confusion_matrix(y_train_louder, y_train_pred))
print(f1_score(y_train_louder, y_train_pred))
# test = cross_val_score(sgd_clf, X_train, y_train_louder, cv=3, scoring="accuracy")
# print(test)
