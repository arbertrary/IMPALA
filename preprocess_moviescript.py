import textwrap
import os
import re


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

        # test = '\n'.join(test)

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
            scenelist.append(text[i] + text[i + 1])

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
            scenelist.append(text[i] + text[i + 1])

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
                while(i + 1 < len(lines) and lines[i + 1].strip()):
                    if(re.search('[(|)]', lines[i + 1].strip())):
                        i += 1
                    else:
                        dialogue.append(lines[i + 1].strip().lower())
                        i += 1

                i += 1
            else:
                i += 1

    return(dialogue)


def main():
    print(extract_moviedialogue("testmovie.txt"))


if __name__ == '__main__':
    main()
