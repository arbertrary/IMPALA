import numpy as np


# def part(lst, sz): return [lst[i:i + sz] for i in range(0, len(lst), sz)]
#
#
# def partition(lst, sections: int):
#     sz = int(len(lst) / sections)
#     newlist = [lst[i:i + sz] for i in range(0, len(lst), sz)]
#
#     newlist = newlist[0:sections]
#
#     return newlist
#
#
# def chunkIt(seq, num):
#     avg = len(seq) / float(num)
#     out = []
#     last = 0.0
#
#     while last < len(seq):
#         out.append(seq[int(last):int(last + avg)])
#         last += avg
#
#     return out

def split(a, n):
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
