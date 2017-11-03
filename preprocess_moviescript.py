import textwrap
import os
import re
from nltk import word_tokenize

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
def extract_moviedialogue(movie_filename):
    scenelist = separate_scenes(movie_filename)




# compare the dialogue of a subtitle file to the dialogue of a movie script
# how similar are they? is the movie script "correct"
def compare_script_subtitles(movie_filename, subs_filename):
    subs_dialogue = extract_dialogue(subs_filename)








def main():
    compare_script_subtitles('testmovie.txt', 'testsubs.txt')
    #clean_moviescript('Star-Wars-A-New-Hope.txt')
    #clean_moviescript('American-Psycho.txt')
    #test = nltk.word_tokenize(open('testfiles/Star-Wars-A-New-Hope.txt').read())
    #print(set(test))


if __name__ == '__main__':
    main()
