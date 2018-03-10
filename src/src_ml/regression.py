import pandas
import numpy as np
import os
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import PolynomialFeatures

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir))

dataframe = pandas.read_csv("6mv_mean_audio_raw_combined_sent.csv")
# dataframe = pandas.read_csv("6mv_mean_audio_raw_normalized_combined.csv")

dataset = dataframe.values
# X = dataset[:, np.newaxis, 3]
X = dataset[:,1:6]
# print(X)
# y = dataset[:,9]
y = dataset[:, 9]

# print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# regr = linear_model.LinearRegression()
regr = linear_model.Ridge(alpha=.5)

# kf = KFold(n_splits=10)
# for train_index, test_index in kf.split(X):
#     # print("TRAIN:", train_index, "TEST:", test_index)
#     X_train, X_test = X[train_index], X[test_index]
#     y_train, y_test = y[train_index], y[test_index]
#     regr.fit(X_train, y_train)
#     y_pred = regr.predict(X_test)
#     # The coefficients
#     print('Coefficients: \n', regr.coef_)
#     # The mean squared error
#     print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
#     # Explained variance score: 1 is perfect prediction
#     print('R^2 score: %.2f' % r2_score(y_test, y_pred))

model = regr.fit(X_train, y_train)
y_pred = regr.predict(X_test)
print(model.score(X_test, y_test))

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('R^2 score: %.2f' % r2_score(y_test, y_pred))
print("Variance: %.2f" % explained_variance_score(y_test, y_pred))


# Plot outputs
plt.scatter(X_test, y_test, color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=3)
plt.xlabel("Scene Time Code in Seconds")
plt.ylabel("Audio Energy")
plt.xticks(())
plt.yticks(())

plt.show()
