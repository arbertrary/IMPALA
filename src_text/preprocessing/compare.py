"""Comparing movie scripts and subtitle file.
Upcoming: annotating movie scripts with time codes from subtitles """
import re

from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz
from pp_subtitles import extract_subdialogue
from parse_moviescript import extract_moviedialogue


def compare_script_subtitles(movie_filename: str, subs_filename: str):
    """compare the dialogue of a subtitle file to the dialogue of a movie script"""
    subs_dialogue = extract_subdialogue(subs_filename)
    movie_dialogue = extract_moviedialogue(movie_filename)

    subs_tokens = word_tokenize(' '.join(subs_dialogue))
    movie_tokens = word_tokenize(' '.join(movie_dialogue))

    found = 0
    not_found = 0
    for token in subs_tokens:
        if token in movie_tokens:
            found += 1
        else:
            not_found += 1
    print("Found: " + str(found))

    print("Not Found: " + str(not_found))


def word_frequency(movie_filename: str, subs_filename: str):
    """Nur zum Testen: Häufigkeit der vorkommenden Wörter zählen"""

    frequency = {}

    movie_dialogue = ' '.join(extract_moviedialogue(movie_filename))
    # subs_dialogue = ' '.join(extract_subdialogue(subs_filename))

    match_pattern = re.findall(r'\b[a-z]{3,15}\b', movie_dialogue)

    for word in match_pattern:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

    frequency_list = frequency.keys()

    for words in frequency_list:
        if frequency[words] > 5:
            print(words, frequency[words])


def find_closest_sentences(movie_filename: str, subs_filename: str):
    """Find closest matching sentences"""
    subs_dialogue = ' '.join(extract_subdialogue(subs_filename))
    subs_dialogue = sent_tokenize(subs_dialogue)

    movie_dialogue = ' '.join(extract_moviedialogue(movie_filename))
    movie_dialogue = sent_tokenize(movie_dialogue)

    print(len(subs_dialogue))

    done1 =[]
    done2 = []
    count = 0
    for subsent in subs_dialogue:
        for moviesent in movie_dialogue:
            if moviesent not in done2 and subsent not in done1:
                ratio = fuzz.ratio(subsent, moviesent)
    # best between 88 and 89
                if ratio > 70:
                    done1.append(subsent)
                    done2.append(moviesent)
                    count += 1

                    print(moviesent)
                    print(subsent)
                    print(ratio)
                    # print("\n")

                else:
                    continue
    print(count)


def test_needleman(movie_filename: str, subs_filename: str):
    """testing nwalign3"""

    subs_dialogue = ' '.join(extract_subdialogue(subs_filename))
    subs_dialogue = word_tokenize(subs_dialogue)

    movie_dialogue = ' '.join(extract_moviedialogue(movie_filename))
    movie_dialogue = word_tokenize(movie_dialogue)

    for subsent in subs_dialogue:
        for moviesent in movie_dialogue:
            test = nw.global_align(subsent, moviesent)


            score = nw.score_alignment(test[0].upper(), test[1].upper(), gap_open=-10, gap_extend=-5, matrix='PAM250')
            if score > 10:
                print(test[0])
                print(test[1])
                print(score)


def main():
    """main function"""
    # find_closest_sentences("testmovie.txt", "testsubs.txt")
    # find_closest_sentences("Star-Wars-A-New-Hope.txt",
    # "Star-Wars-A-New-HopeSubtitles.srt")
    find_closest_sentences("American-Psycho.txt", "AmericanPsychoSubtitles.srt")



    # word_frequency(
    #     "Star-Wars-A-New-Hope.txt",
    #     "Star-Wars-A-New-HopeSubtitles.srt")
    # compare_script_subtitles("testmovie.txt", "testsubs.txt")
    # compare_script_subtitles("Star-Wars-A-New-Hope.txt",
    # "Star-Wars-A-New-HopeSubtitles.srt")
    #test = nw.global_align("est", "testlul")

    # print(test[0].upper())
    # print(test[1])

    #print(nw.score_alignment(test[0].upper(), test[1].upper(), gap_open=-5, gap_extend=-2, matrix='PAM250'))
    # print(nw.score_alignment('CEELECANTH', '-PELICAN--', gap_open=-5,
    # gap_extend=-2, matrix='PAM250'))

    # test_needleman("Star-Wars-A-New-Hope.txt", "Star-Wars-A-New-HopeSubtitles.srt")
    # test_needleman("testmovie.txt", "testsubs.txt")


if __name__ == '__main__':
    main()