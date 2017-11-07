import matplotlib.pyplot as plt

from preprocess_subtitles import extract_subdialogue
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

def subdialogue_sentiment(subs_filename):
    subs_dialogue = ' '.join(extract_subdialogue(subs_filename))
    subs_dialogue = tokenize.sent_tokenize(subs_dialogue)

    sid = SentimentIntensityAnalyzer()
    compounds = []
    for sent in subs_dialogue:
        ss = sid.polarity_scores(sent)
        compounds.append(ss.get('compound'))

    plt.plot(compounds)
    plt.xlabel("Sentences in Subtitledialogue")
    plt.ylabel("Compound of sentence")
    plt.show()


def main():
    subdialogue_sentiment('testsubs.txt')


if __name__ == '__main__':
    main()
