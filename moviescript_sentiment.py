import matplotlib.pyplot as plt
from preprocess_moviescript import separate_scenes, extract_moviedialogue
from preprocess_subtitles import extract_subdialogue
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize


def dialogue_sentiment(subs_filename, movie_filename):
    subs_dialogue = ' '.join(extract_subdialogue(subs_filename))
    subs_dialogue = tokenize.sent_tokenize(subs_dialogue)

    movie_dialogue = ' '.join(extract_moviedialogue(movie_filename))
    movie_dialogue = tokenize.sent_tokenize(movie_dialogue)

    sid = SentimentIntensityAnalyzer()
    compounds1 = []
    for sent in subs_dialogue:
        ss = sid.polarity_scores(sent)
        compounds1.append(ss.get('compound'))

    compounds2 = []
    for sent in movie_dialogue:
        ss = sid.polarity_scores(sent)
        compounds2.append(ss.get('compound'))

    plt.subplot(211)
    plt.plot(compounds1)
    plt.xlabel("Sentences in Subtitle Dialogue")
    plt.ylabel("Compound of sentence")

    plt.subplot(212)
    plt.plot(compounds2)
    plt.xlabel("Sentences in Movie Dialogue")
    plt.ylabel("Compound of sentence")



def scenesentiment(movie_filename):
    #scenelist = separate_scenes('Star-Wars-A-New-Hope.txt')
    scenelist = separate_scenes(movie_filename)
    #print(scenelist)
    # scenelist = separate_scenes("testmovie.txt")
    compounds = []

    for scene in scenelist:
        scene = ' '.join([line.strip() for line in scene.split('\n')])
        #print(scene)
        sentences = tokenize.sent_tokenize(scene)

        sid = SentimentIntensityAnalyzer()
        test = []
        for s in sentences:
            ss = sid.polarity_scores(s)
            test.append(ss.get('compound'))

        avg = sum(test)/len(test)
        # if(avg > 0.2):
        #     print(scene)
        compounds.append(avg)
        #print(avg)

    fullavg = sum(compounds)/len(compounds)
    # print(fullavg)

    #plt.figure(1)
    #plt.subplot(211)
    plt.ylim(-0.5,0.5)
    plt.plot(compounds)
    plt.axhline(y=0, color='k')
    plt.text(0, 0.4, "Total avg compound: " + str("%.3f" % fullavg))
    plt.ylabel("Avg compound of scenes")
    plt.xlabel("Scenes " + movie_filename)

def main():
    # plt.subplot(311)
    # scenesentiment("Friday-the-13.txt")
    # plt.subplot(312)
    # scenesentiment("Warrior.txt")
    # plt.subplot(313)
    # scenesentiment("Cars-2.txt")

    dialogue_sentiment("Star-Wars-A-New-HopeSubtitles.srt", "Star-Wars-A-New-Hope.txt")
    plt.show()

if __name__ == '__main__':
    main()
