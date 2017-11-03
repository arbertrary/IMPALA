
import os
import re
import random
import string
from nltk import word_tokenize

dirpath = 'imsdbScripts'

# removes movie scripts
# 1121 scripts at the beginning
# 29.10.: 974 remaining
# removed scripts that
# a) don't use EXT/INT or EXTERIOR/INTERIOR to separate scenes
# b) have some html tags remaining
#
# 30.10.: 953 remaining
# (removed scripts that don't contain information about author and script at the end)

def check_all_moviescripts(directory):
    incorrect_scripts = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8-sig') as m:
            text = m.read()

            check1 = re.search(
                '(INT[.:]{0,1} |EXT[.:]{0,1} |INTERIOR[.:]{0,1} |EXTERIOR[.:]{0,1} )',
                text)
            check2 = re.search('<[^<]+?>', text)

            if(not check1):
                incorrect_scripts.append(filename)
                # raise ValueError('Inputfile not in correct format!')
            if(check2):
                incorrect_scripts.append(filename)
    print(incorrect_scripts)
    print(len(incorrect_scripts))

    # testset = set(incorrect_scripts)
    for f in incorrect_scripts:
        # os.remove(os.path.join(dirpath, f))


# Checks if there is a paragraph at the end of the file
# that contains writers and genre
# e.g.
# Star Wars: A New Hope
# Writers :   George Lucas
# Genres :   Action  Adventure  Fantasy  Sci-Fi
def check_movieinfo_at_end_of_file(directory):
    end = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as m:
            text = m.read()
            text = text.strip()

            text = text.split('\n\n')
            movieinfo = text[-1]
            if(not ('writers' in movieinfo.lower() and 'Genres : ' in movieinfo)):
                end.append(filename)


    for f in end:
        # os.remove(os.path.join(dirpath, f))

    print(end)
    print(len(end))

# Extracts genres from all moviescripts and writes them to new file
def get_all_genres(directory):
    f = open("allgenres.txt", 'w+')

    allgenres = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as m:
            text = m.read()
            text = text.replace('\xa0',' ')
            #print(text)
            text = text.strip()

            text = text.split('\n\n')
            movieinfo = text[-1]

            movieinfo = movieinfo.split("\n")

            genres = ''
            for line in movieinfo:
                if 'Genres : ' in line:
                    genres = re.sub('Genres : ', '', line)

                    genres = genres.strip()
                    genres = word_tokenize(genres)
                    genres = ','.join(genres)

            moviedata = re.sub('.txt','', filename) + ':' + genres
            allgenres.append(moviedata)


    allgenres = sorted(allgenres)
    # f.write(("\n".join(allgenres)).strip())
    f.close()




def main():
    get_all_genres('imsdbScripts')
    # check_all_moviescripts('imsdbScripts')
    #check_information_at_end_of_file('imsdbScripts')


if __name__ == '__main__':
    main()