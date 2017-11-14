"""Sentiment analysis of subtitle files"""
import matplotlib.pyplot as plt

from preprocess_subtitles import extract_subdialogue
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


def subdialogue_sentiment(subs_filename):
    """Analyse dialogue from subtitles"""
    subs_dialogue = ' '.join(extract_subdialogue(subs_filename))
    subs_dialogue = tokenize.sent_tokenize(subs_dialogue)

    sid = SentimentIntensityAnalyzer()
    compounds = []
    for sent in subs_dialogue:
        score = sid.polarity_scores(sent)
        compounds.append(score.get('compound'))

    plt.plot(compounds)
    plt.xlabel("Sentences in Subtitledialogue")
    plt.ylabel("Compound of sentence")
    plt.show()


def main():
    """main function"""
    subdialogue_sentiment('testsubs.txt')


if __name__ == '__main__':
    main()
