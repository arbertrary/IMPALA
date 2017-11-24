"""Sentiment analysis of subtitle files"""
import matplotlib.pyplot as plt
import matplotlib
from preprocess_subtitles import get_dialogue_with_time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from textblob import TextBlob
# from afinn import Afinn


def subdialogue_sentiment(subs_filename):
    """Analyse dialogue from subtitles"""
    subtitles = get_dialogue_with_time(subs_filename)

    x = []
    scores = []

    for s in subtitles:

        blob = TextBlob(s[1])
        score = blob.sentiment.polarity

        if score != 0.0:
            x.append(s[0])
            scores.append(score)

    x = matplotlib.dates.date2num(x)

    plt.plot_date(x,scores)
    plt.show()


def main():
    """main function"""
    subdialogue_sentiment("Star-Wars-A-New-HopeSubtitles.srt")


if __name__ == '__main__':
    main()
