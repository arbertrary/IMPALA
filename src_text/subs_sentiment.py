"""Sentiment analysis of subtitle files"""
import matplotlib.pyplot as plt
from matplotlib import dates
from pp_subtitles import get_dialogue_with_time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from textblob import TextBlob
from afinn import Afinn


def subdialogue_sentiment(subs_filename):
    """Analyse dialogue from subtitles"""
    subtitles = get_dialogue_with_time(subs_filename)

    x = []
    scores = []

    sid = SentimentIntensityAnalyzer()
    afinn = Afinn()

    for s in subtitles:
        #Textblob
        blob = TextBlob(s[1])
        score = blob.sentiment.polarity
        if score != 0.0:
            x.append(s[0])
            scores.append(score)

        #VADER
       # score = sid.polarity_scores(s[1]).get('compound')
        #if score != 0:
         #   x.append(s[0])
          #  scores.append(score)

        #Afinn
       # score = afinn.score(s[1])
        #if score !=0:
         #   x.append(s[0])
          #  scores.append(score)



    x = dates.date2num(x)

    plt.plot_date(x, scores)
    plt.show()


def main():
    """main function"""
    subdialogue_sentiment("Star-Wars-A-New-HopeSubtitles.srt")


if __name__ == '__main__':
    main()
