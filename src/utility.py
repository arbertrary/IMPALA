import numpy as np


def part(lst, sz): return [lst[i:i + sz] for i in range(0, len(lst), sz)]


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
