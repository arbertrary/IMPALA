import csv
import pandas
import matplotlib.pyplot as plt
import numpy as np


df = pandas.read_csv("6mv_mean_audio_raw_combined_sent.csv")
print(df.describe())

with open("6mv_mean_audio_raw_normalized_combined.csv") as csvfile:
    reader = csv.reader(csvfile)
    audio = []
    df = pandas.read_csv("6mv_mean_audio_raw_normalized_combined.csv")

    # min = np.min(df.get("Audio Level"))
    # max = np.max(df.get("Audio Level"))
    with open("Warriner_Class.csv", "w") as newfile:
        writer = csv.writer(newfile, delimiter=',', quoting=csv.QUOTE_ALL)

        for row in reader:
            if row[-1] == "Audio Level":
                continue
            else:
                z = float(row[-1])
                # audio.append(((z-min)/max-min))

                if z <= 0.25:
                    level = "silent"
                elif 0.25 < z <= 0.50:
                    level = "medium"
                elif 0.50 < z <= 0.75:
                    level = "loud"
                else:
                    level = "loudest"

                r = [row[2], row[3],row[4], level]
                writer.writerow(r)


