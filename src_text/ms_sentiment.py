"""Sentiment analysis on movie scripts """

import numpy as np
import matplotlib.pyplot as plt
from parse_moviescript import extract_moviedialogue, get_scene_tuples
from pp_subtitles import extract_subdialogue
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from textblob import TextBlob
from afinn import Afinn


def dialogue_sentiment(subs_filename: str, movie_filename: str):
    """Calculate sentiment of extracted dialogue from movie and subtitle + plot"""
    subs_dialogue = ' '.join(extract_subdialogue(subs_filename))
    subs_dialogue = tokenize.sent_tokenize(subs_dialogue)

    movie_dialogue = ' '.join(extract_moviedialogue(movie_filename))
    movie_dialogue = tokenize.sent_tokenize(movie_dialogue)

    sid = SentimentIntensityAnalyzer()
    afinn = Afinn()

    textblob_scores = []
    vader_scores = []
    afinn_scores = []
    for sentence in subs_dialogue:
        # TextBlob
        blob = TextBlob(sentence)
        score1 = blob.sentiment.polarity
        textblob_scores.append(score1)

        # nltk VADER
        # Idea: ignore neutral sentences
        # How to keep range of x-axis?
        score2 = sid.polarity_scores(sentence).get('compound')
        if score2 <= -0.5 or score2 >= 0.5:
            vader_scores.append(score2)
        # else:
        #     vader_scores.append(0)

        # AFINN
        score3 = afinn.score(sentence)
        afinn_scores.append(score3)

    textblob_mscores = []
    vader_mscores = []
    afinn_mscores = []
    for sentence in movie_dialogue:
        # TextBlob
        blob = TextBlob(sentence)
        score1 = blob.sentiment.polarity
        textblob_mscores.append(score1)

        # nltk VADER
        score2 = sid.polarity_scores(sentence).get('compound')
        vader_mscores.append(score2)

        # AFINN
        score3 = afinn.score(sentence)
        afinn_mscores.append(score3)

    # x = range(0, len(textblob_scores))
    # xnew = np.linspace(0, len(textblob_scores), 300)
    # test = spline(x,textblob_scores,xnew)

    plt.subplot(321)
    # plt.plot(xnew, test)
    plt.plot(textblob_scores)
    plt.axhline(y=0, color='k')
    plt.xlabel("Sentences in Subtitle Dialogue")
    plt.ylabel("TextBlob")

    plt.subplot(322)
    plt.plot(textblob_mscores)
    plt.axhline(y=0, color='k')
    plt.xlabel("Sentences in Movie Dialogue")
    plt.ylabel("TextBlob")

    plt.subplot(323)
    plt.axhline(y=0, color='k')
    plt.plot(vader_scores)
    plt.xlabel("Sentences in Subtitle Dialogue")
    plt.ylabel("VADER")

    plt.subplot(324)
    plt.axhline(y=0, color='k')
    plt.plot(vader_mscores)
    plt.xlabel("Sentences in Movie Dialogue")
    plt.ylabel("VADER")

    plt.subplot(325)
    plt.axhline(y=0, color='k')
    plt.plot(afinn_scores)
    plt.xlabel("Sentences in Subtitle Dialogue")
    plt.ylabel("AFINN")

    plt.subplot(326)
    plt.axhline(y=0, color='k')
    plt.plot(afinn_mscores)
    plt.xlabel("Sentences in Movie Dialogue")
    plt.ylabel("AFINN")


def scenesentiment(movie_filename: str):
    """Calculate sentiment of scenes in the moviescript"""
    scenelist = get_scene_tuples(movie_filename)
    scorelist = []

    sid = SentimentIntensityAnalyzer()
    afinn = Afinn()
    for scene in scenelist:
        scene = ' '.join([line.strip() for line in scene[1].split('\n')])
        sentences = tokenize.sent_tokenize(scene)

        # sentiment = TextBlob(scene[1])
        # score = sentiment.sentiment.polarity
        # scorelist.append(score)

        test = []
        for sentence in sentences:
            # TextBlob
            sentiment = TextBlob(sentence)
            score = sentiment.sentiment.polarity

            # nltk VADER
            # score = sid.polarity_scores(sentence).get('compound')

            # afinn
            # score = afinn.score(sentence)

            test.append(score)

        avg = sum(test) / len(test)

        scorelist.append(avg)

    fullavg = sum(scorelist) / len(scorelist)

    # plt.ylim(-0.5, 0.5)
    plt.plot(scorelist)
    plt.axhline(y=0, color='k')
    plt.text(0, 0.4, "Total avg compound: " + str("%.3f" % fullavg))
    plt.ylabel("Avg score of scene")
    plt.xlabel("Scenes " + movie_filename)


def main():
    """Main function"""

    plt.subplot(311)
    scenesentiment("Scream.txt")
    plt.subplot(312)
    scenesentiment("Pitch-Black.txt")
    plt.subplot(313)
    scenesentiment("Cars-2.txt")

    # dialogue_sentiment('AmericanPsychoSubtitles.srt', 'American-Psycho.txt')
    # dialogue_sentiment(
    # "Star-Wars-A-New-HopeSubtitles.srt",
    # "Star-Wars-A-New-Hope.txt")
    plt.show()


if __name__ == '__main__':
    main()
