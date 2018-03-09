import pandas
import numpy as np
import csv
import warnings
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

dataframe = pandas.read_csv("6mv_mean_audio_raw_combined_sent.csv")
dataset = dataframe.values
X = dataset[:,np.newaxis,4]
print(X)
y = dataset[:,9]
print(y)

X_train = X[:800]
X_test = X[800:]

y_train = y[:800]
y_test = y[800:]

regr = linear_model.LinearRegression()

regr.fit(X_train, y_train)

y_pred = regr.predict(X_test)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"% mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(y_test, y_pred))

# Plot outputs
plt.scatter(X_test, y_test,  color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
