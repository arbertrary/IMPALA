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

dataframe = pandas.read_csv("audio_sent.csv")
dataset = dataframe.values

# print(dataset)
perm = np.random.permutation(dataset)
# print(perm)
X = perm[:, 2:4]
y = perm[:, 4]

X_train, X_test, y_train, y_test = X[:56], X[56:], y[:56], y[56:]

y_train_louder = (y_train == "louder")
y_test_louder = (y_test == "louder")

test_scene = X_test[10]
print(test_scene)
print(y_test[10])

sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train, y_train_louder)

print(sgd_clf.predict(X_test))
y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_louder, cv=3)
print(confusion_matrix(y_train_louder, y_train_pred))
