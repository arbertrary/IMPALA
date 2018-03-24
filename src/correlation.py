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


def main():
    csvfile = os.path.join(BASE_DIR, "data/audiosentiment_csvfiles/7mv_audiosent_all.csv")

    df = pd.read_csv(csvfile)

    energy = df.get("Audio Energy").values
    neg = df.get("Vader neg").values
    neu = df.get("Vader neu").values
    pos = df.get("Vader pos").values
    compound = df.get("Vader compound").values


    # test = correlation(csvfile, "Vader neg", "Audio Energy")
    # print(test[0])
    # print(test[2])
    # print()
    # test = correlation(csvfile, "Vader neu", "Audio Energy")
    # print(test[0])
    # print(test[2])
    # print()
    # test = correlation(csvfile, "Vader pos", "Audio Energy")
    # print(test[0])
    # print(test[2])
    # print()
    # test = correlation(csvfile, "Vader compound", "Audio Energy")
    # print(test[0])
    # print(test[2])
    permutationtest(energy, compound, 1000000)

    # directory = os.path.join(BASE_DIR, "src")
    #
    # indices = ["Anger", "Anticipation", "Disgust", "Fear", "Joy", "Negative",
    #            "Positive", "Sadness", "Surprise", "Trust"]
    #
    # for i in indices:
    #     print(r"\textbf{" + i + "}", r"\\")
    #     for file in os.listdir(directory):
    #         if ".csv" not in file:
    #             continue
    #         csvfile = os.path.join(directory, file)
    #         print("\n", r"\textit{" + file.replace("_audiosent_all.csv", "") + "}", "\n")
    #         t = correlation(csvfile, i, "Audio Energy", raw=True)
    #         print("spearman: ", "%.3f" % t[0][0], r"\\", "\np-value: ", t[0][1], r"\\")
    #         # print("pearson: ", t[1][0], "\np-value: ", t[1][1])
    #         print("kendall's tau: ", "%.3f" % t[2][0], r"\\", "\np-value: ", t[2][1], r"\\")
    #         print(r"\\")


if __name__ == '__main__':
    main()
