import textwrap
import os
import re
import string
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz

from preprocess_subtitles import extract_subdialogue

dirpath = 'testfiles'


def clean_moviescript(movie_filename):
    movie_path = os.path.join(dirpath, movie_filename)


    with open(movie_path, 'r', encoding='utf-8') as m:
        text = m.read()
        text = text.strip()

        # text = re.sub('\n+', '', text)
        # print(text)

        # test = m.readlines()
        # test = [textwrap.dedent(line) for line in test]
        # test = [line.strip() for line in test]
        # test = [re.sub('\n+', '', line) for line in test]

        #test = '\n'.join(test)


        # print(test)



# Eigentlich wurden die ja schon alle aussortiert in check_all_moviescripts
        # test = re.search(
        #     '(INT[.:]{0,1} |EXT[.:]{0,1} |INTERIOR[.:]{0,1} |EXTERIOR[.:]{0,1} )',
        #     text)
        # if(not test):
        #     raise ValueError('Inputfile not in correct format!')
        text = re.split(
            '(INT[.:]{0,1} |EXT[.:]{0,1} |INTERIOR[.:]{0,1} |EXTERIOR[.:]{0,1} )',
            text)

        i = 1
        scenelist = []
        while (i < len(text)):
            # print(text[i] + text[i + 1])
            scenelist.append(text[i] + text[i+1])

            i += 2

        for scene in scenelist:
            print(scene)


# separates the scenes of a movie script by splitting at "Scene introductions"
# e.g. INT. or EXT.
def separate_scenes(movie_filename):
    movie_path = os.path.join(dirpath, movie_filename)


    with open(movie_path, 'r', encoding='utf-8') as m:
        text = m.read()
        text = text.strip()

        text = re.split(
            '(INT[.:]{0,1} |EXT[.:]{0,1} |INTERIOR[.:]{0,1} |EXTERIOR[.:]{0,1} )',
            text)

        i = 1
        scenelist = []
        while (i < len(text)):
            # print(text[i] + text[i + 1])
            scenelist.append(text[i] + text[i+1])

            i += 2
    return scenelist


# extracts all dialogue from a moviescript and ignores metatext
# sollte ich dialog als list der lines extrahieren oder als string?
# ich wandle ja eh wieder in strings um fürs tokenizen
def extract_moviedialogue(movie_filename):
    scenelist = separate_scenes(movie_filename)

    dialogue = []

    for scene in scenelist:
        lines = scene.split(os.linesep)

        i = 1
        while (i < len(lines)):
            if(lines[i].strip().isupper()):
                while(i+1 < len(lines) and lines[i+1].strip()):
                    if(re.search('[(|)]', lines[i+1].strip())):
                        i+=1
                    else:
                        dialogue.append(lines[i+1].strip().lower())
                        i+=1

                i +=1
            else:
                i +=1


    return(dialogue)





# compare the dialogue of a subtitle file to the dialogue of a movie script
# how similar are they? is the movie script "correct"
def compare_script_subtitles(movie_filename, subs_filename):
    subs_dialogue = extract_subdialogue(subs_filename)
    movie_dialogue = extract_moviedialogue(movie_filename)

    subs_tokens = word_tokenize(' '.join(subs_dialogue))
    movie_tokens = word_tokenize(' '.join(movie_dialogue))


    found = 0
    not_found = 0
    for token in subs_tokens:
        if(token in movie_tokens):
            found += 1
        else:
            not_found +=1
    print("Found: " +str(found))

    print("Not Found: " + str(not_found))



# Nur zum Testen: Häufigkeit der vorkommenden Wörter zählen
def word_frequency(movie_filename, subs_filename):
    frequency = {}

    movie_dialogue = ' '.join(extract_moviedialogue(movie_filename))
    # subs_dialogue = ' '.join(extract_subdialogue(subs_filename))

    match_pattern = re.findall(r'\b[a-z]{3,15}\b', movie_dialogue)

    for word in match_pattern:
        count = frequency.get(word, 0)
        frequency[word] = count +1

    frequency_list = frequency.keys()

    for words in frequency_list:
        if(frequency[words] > 5):
            print(words, frequency[words])



def find_closest_sentences(movie_filename, subs_filename):
    subs_dialogue = ' '.join(extract_subdialogue(subs_filename))
    subs_dialogue = sent_tokenize(subs_dialogue)

    movie_dialogue = ' '.join(extract_moviedialogue(movie_filename))
    movie_dialogue = sent_tokenize(movie_dialogue)

    print(len(subs_dialogue))

    count = 0
    for sentS in subs_dialogue:
        for sentM in movie_dialogue:
            ratio = fuzz.ratio(sentS, sentM)
#best between 88 and 89
            if(ratio > 88):
                count += 1

                print(sentM)
                print(sentS)
                print(ratio)
                #print("\n")

        else:
            continue
    print(count)



def main():
    # find_closest_sentences("testmovie.txt", "testsubs.txt")
    #find_closest_sentences("Star-Wars-A-New-Hope.txt", "Star-Wars-A-New-HopeSubtitles.srt")
    #word_frequency("Star-Wars-A-New-Hope.txt", "Star-Wars-A-New-HopeSubtitles.srt")
    print(extract_moviedialogue("testmovie.txt"))
    #compare_script_subtitles("testmovie.txt", "testsubs.txt")
    #compare_script_subtitles("American-Psycho.txt", "AmericanPsychoSubtitles.srt")
    # compare_script_subtitles("Star-Wars-A-New-Hope.txt", "Star-Wars-A-New-HopeSubtitles.srt")



if __name__ == '__main__':
    main()
