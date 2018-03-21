import pandas
import numpy as np
import os
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, f1_score
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import PolynomialFeatures

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir))

path = os.path.join(BASE_DIR, "data/audiosentiment_csvfiles/7mv_audiosent_Warriner.csv")
# path = os.path.join(BASE_DIR, "src/6mv_mfcc_combined.csv")
dataframe = pandas.read_csv(path)

# dataframe = pandas.read_csv("6mv_mean_audio_raw_normalized_combined.csv")

dataset = dataframe.values
X = dataset[:, np.newaxis, 4]
# X = dataset[:,5:9]
print(X)
# y = dataset[:,9]
y = dataset[:, 5]

print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

regr = linear_model.LinearRegression()

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
plt.xlabel("Dominance")
plt.ylabel("Audio Energy")
# plt.xticks(())
# plt.yticks(())
plt.tight_layout()
plt.show()
