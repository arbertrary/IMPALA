import os
import numpy as np
import pandas as pd
from scipy import stats

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))


def correlation(csv_path: str, x_variable: str, y_variable: str, raw=True):
    dataframe = pd.read_csv(csv_path)
    x = dataframe.get(x_variable).values
    y = dataframe.get(y_variable).values
    rho = stats.spearmanr(x, y)
    p = stats.pearsonr(x, y)
    tau = stats.kendalltau(x, y)

    return rho, p, tau, len(x)


def permutationtest(a, b, n_perm):
    rho = stats.spearmanr(a, b)
    print(rho)

    greater = 0
    less = 0
    i = 0
    while i < n_perm:
        if i > n_perm:
            break
        i += 1
        np.random.shuffle(a)
        test = stats.spearmanr(a, b)
        if test[0] >= rho[0]:
            greater += 1
        else:
            less += 1
    print("Spearman Coefficient rho=:", rho[0], "p-value=", rho[1])
    print("Permutations with correlation greater rho: ", greater / n_perm)
