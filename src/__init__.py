import os

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))

fountain1 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "blade.txt")
fountain2 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "hellboy.txt")
fountain3 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "predator.txt")
fountain4 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "scream.txt")
fountain5 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "star-wars-4.txt")
fountain6 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "the-matrix.txt")
fountain7 = os.path.join(BASE_DIR, "data/moviescripts_fountain", "indiana-jones-and-the-last-crusade.txt")

audio1 = os.path.join(BASE_DIR, "data/audio_csvfiles", "blade.csv")
audio2 = os.path.join(BASE_DIR, "data/audio_csvfiles", "hellboy.csv")
audio3 = os.path.join(BASE_DIR, "data/audio_csvfiles", "predator.csv")
audio4 = os.path.join(BASE_DIR, "data/audio_csvfiles", "scream_ger.csv")
audio5 = os.path.join(BASE_DIR, "data/audio_csvfiles", "star-wars-4.csv")
audio6 = os.path.join(BASE_DIR, "data/audio_csvfiles", "the-matrix.csv")
audio7 = os.path.join(BASE_DIR, "data/audio_csvfiles", "indiana-jones-3_ger.csv")

tuning1 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "blade_tuning.csv")
tuning2 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "hellboy_tuning.csv")
tuning3 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "predator_tuning.csv")
tuning4 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "scream_ger_tuning.csv")
tuning5 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "star-wars-4_tuning.csv")
tuning6 = os.path.join(BASE_DIR, "data/audio_csvfiles/tuning", "the-matrix_tuning.csv")

script1 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "blade_man.xml")
script2 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "hellboy_man.xml")
script3 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "predator_man.xml")
script4 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "scream_man.xml")
script5 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "star-wars-4_man.xml")
script6 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "the-matrix_man.xml")
script7 = os.path.join(BASE_DIR, "data/moviescripts_xml_time_manually", "indiana-jones-3_man.xml")

subs1 = os.path.join(BASE_DIR, "data/subtitles_xml/", "blade_subs.xml")
subs2 = os.path.join(BASE_DIR, "data/subtitles_xml/", "hellboy_subs.xml")
subs3 = os.path.join(BASE_DIR, "data/subtitles_xml/", "predator_subs.xml")
subs4 = os.path.join(BASE_DIR, "data/subtitles_xml/", "scream_subs.xml")
subs5 = os.path.join(BASE_DIR, "data/subtitles_xml/", "star-wars-4_subs.xml")
subs6 = os.path.join(BASE_DIR, "data/subtitles_xml/", "the-matrix_subs.xml")
subs7 = os.path.join(BASE_DIR, "data/subtitles_xml/", "indiana-jones-and-the-last-crusade_subs.xml")

data_fountain = [(fountain1, audio1), (fountain2, audio2), (fountain3, audio3), (fountain4, audio4),
                 (fountain5, audio5), (fountain6, audio6), (fountain7, audio7)]
data_fountain_tune = [(fountain1, tuning1), (fountain2, tuning2), (fountain3, tuning3), (fountain4, tuning4),
                      (fountain5, tuning5), (fountain6, tuning6)]

data_script = [(script1, audio1), (script2, audio2), (script3, audio3), (script4, audio4), (script5, audio5),
               (script6, audio6), (script7, audio7)]
data_script_tune = [(script1, tuning1), (script2, tuning2), (script3, tuning3), (script4, tuning4),
                    (script5, tuning5),
                    (script6, tuning6)]
data_subs = [(subs1, audio1), (subs2, audio2), (subs3, audio3), (subs4, audio4), (subs5, audio5), (subs6, audio6),
         (subs7, audio7)]
