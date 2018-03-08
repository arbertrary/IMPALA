import numpy as np


def split(a, n):
    """Splits list into n parts of roughly equal size.
    to prevent that there is one "rest" element"""
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def sliding_window(inputlist: list, win_size: int):
    windows = []
    current_mean = []

    for index, score in enumerate(inputlist):
        if index + win_size <= len(inputlist):
            temp = inputlist[index:index + win_size]
            current_mean = np.mean(temp)
            windows.append(current_mean)
        else:
            temp = inputlist[index:]
            i = len(temp)
            while i < win_size:
                temp.append(current_mean)
                i += 1
            current_mean = np.mean(temp)
            windows.append(current_mean)

    return windows


def mean_normalize(energy: np.array):
    mean = np.mean(energy)
    test2 = [x / mean for x in energy]
    return test2
