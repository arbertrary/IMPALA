"""Sentiment analysis of subtitle files"""

import matplotlib.pyplot as plt
from matplotlib import dates
from sentiment import ImpalaSent
from subtitles import get_sub_sentences
from datetime import datetime


def get_subs_sentiment(subs_filename: str):
    """Analyse dialogue from subtitles"""

    sentiment = ImpalaSent()

    sentences = get_sub_sentences(subs_filename)

    scores = []
    times = []

    for s in sentences:
        arousal = sentiment.score(s[1])[1]
        if (arousal == 0):
            continue
        else:
            time = datetime.strptime(s[0], "%H:%M:%S,%f")

            scores.append(arousal)
            times.append(time)

    scores = scores[::3]
    print(len(scores))
    times = times[::3]

    times = dates.date2num(times)

    # plt.subplot(212)
    # plt.ylabel("Arousal")
    # plt.xlabel("time")
    #
    # plt.plot_date(times, scores, fmt="-", color="b", label="Arousal")
    # plt.xlim(times[0], times[-1])
    # plt.gca().xaxis.set_major_locator(dates.MinuteLocator(byminute=range(0, 60, 10)))
    # plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
    #
    # plt.tight_layout()
    # plt.show()

    return scores, times


def main():
    """main function"""
    # path = "/home/armin/Studium/Bachelor/CodeBachelorarbeit/IMPALA/src/testfiles/hellraiser_subs.xml"
    path = "/home/armin/Studium/Bachelor/CodeBachelorarbeit/IMPALA/src/testfiles/star-wars-4_subs.xml"
    get_subs_sentiment(path)


if __name__ == '__main__':
    main()
