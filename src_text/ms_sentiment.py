"""Sentiment analysis on movie scripts """

import afinnscript
import matplotlib.pyplot as plt
from preprocess_moviescript import separate_scenes, extract_moviedialogue
from preprocess_subtitles import extract_subdialogue
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

    compounds1 = []
    cuml1 = 0.0
    for sent in subs_dialogue:
        # nltk VADER
        # score = sid.polarity_scores(sent).get('compound')
        # score = afinn.score(sent)

        # TextBlob
        sentiment = TextBlob(sent)
        score = sentiment.sentiment.polarity

        cuml1 += score
        compounds1.append(cuml1)

    cuml2 = 0.0
    compounds2 = []
    for sent in subs_dialogue:
        # nltk VADER
        #score = sid.polarity_scores(sent).get('compound')
        score = afinnscript.sentiment(sent)

        # TextBlob
        # sentiment = TextBlob(sent)
        # score = sentiment.sentiment.polarity

        cuml2 += score
        compounds2.append(cuml2)

    plt.subplot(211)
    plt.plot(compounds1)
    plt.xlabel("Sentences in Subtitle Dialogue")
    plt.ylabel("Cumulative sentiment")

    plt.subplot(212)
    plt.plot(compounds2)
    plt.xlabel("Sentences in Movie Dialogue")
    plt.ylabel("Cumulative sentiment")


def scenesentiment(movie_filename: str):
    """Calculate sentiment of scenes in the moviescript"""
    scenelist = separate_scenes(movie_filename)

    scorelist = []

    sid = SentimentIntensityAnalyzer()
    afinn = Afinn()
    for scene in scenelist:
        # cuml = 0.0

        scene = ' '.join([line.strip() for line in scene.split('\n')])
        # print(scene)
        sentences = tokenize.sent_tokenize(scene)


        test = []

        for sent in sentences:
            # TextBlob
            # sentiment = TextBlob(sent)
            # score = sentiment.sentiment.polarity

            # nltk VADER
            # score = sid.polarity_scores(sent).get('compound')

            # afinn
            # score = afinn.score(sent)

            #afinnscript
            score = afinnscript.sentiment(sent)

            test.append(score)

        avg = sum(test) / len(test)
        # cuml = cuml + avg

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
    #     "Star-Wars-A-New-HopeSubtitles.srt",
    #     "Star-Wars-A-New-Hope.txt")
    plt.show()


if __name__ == '__main__':
    main()
