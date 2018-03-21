"""Module for processing audio files.
Functions for calculating RMS energy or other audio features."""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf


# BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir))


def get_feature(path: str, feature: str, block_size: int = 2048, **kwargs) -> np.array:
    """Calculates the raw values of a chosen audio feature for an audio file by blockwise reading.
    :param path: path of audio file
    :param feature: which audio feature to extract (currently "energy", "centroid", "mfcc" and "tuning
    :param block_size: default 2048 frames per block
    :returns np.array"""

    if feature not in ["energy", "tuning", "mfcc", "centroid", "pitches"]:
        raise ValueError("Wrong audio feature")

    block_gen = sf.blocks(path, blocksize=block_size)

    result_list = []
    test = []
    for y in block_gen:
        test.append(y)
        S = librosa.magphase(librosa.stft(y, window=np.ones))[0]

        if feature == "energy":
            rms = librosa.feature.rmse(y=y)
            result = np.mean(rms)
        elif feature == "tuning":
            result = librosa.estimate_tuning(y, fmin=50.0, fmax=2000.0)
        elif feature == "mfcc":
            if kwargs.get("n_mfcc"):
                n_mfcc = kwargs.get("n_mfcc")
            else:
                n_mfcc = 4
            mfccs = librosa.feature.mfcc(y, n_mfcc=n_mfcc)
            result = [np.mean(x) for x in mfccs]
        elif feature == "centroid":
            centroids = librosa.feature.spectral_centroid(y)
            result = np.mean(centroids.T)
        elif feature == "pitches":
            pitches, magnitude = librosa.piptrack(y)
            print(pitches.shape)
            print(pitches)
            result = [np.mean(x) for x in pitches]
            print(np.array(result).shape)
            print(result)
            break

        result_list.append(result)
    block_gen.close()

    plt.show()

    if feature == "mfcc":
        r = np.transpose(np.array(result_list))
    else:
        r = np.array(result_list)
    return r


def partition_feature(path: str, feature: str, interval_seconds: float = 1.0):
    """Partitions the raw values of an audio feature into intervals.
    :param path: audio file path
    :param feature: which audio feature to extract (currently "energy", "centroid", "mfcc" and "tuning
    :param interval_seconds: duration of intervals in seconds as float. defaults to 1.0s"""
    file_duration = sf.info(path).duration

    feature_data = get_feature(path, feature, n_mfcc=4)
    feature_times = []
    time = 0
    duration = 0
    temp = []

    if feature == "mfcc":
        time_per_frame = np.divide(file_duration, len(feature_data.T))

        mfccs = []
        times = []
        indices = []

        for index, coeff in enumerate(feature_data):
            current_coeff = []
            if index == 0:
                for i, frame in enumerate(coeff):
                    if duration < interval_seconds:
                        temp.append(frame)
                        indices.append(i)
                        duration += time_per_frame
                        time += time_per_frame
                    else:
                        temp.append(frame)
                        indices.append(i)
                        timestamp = float("{0:.3f}".format(time))
                        times.append((timestamp, indices))
                        current_coeff.append(np.mean(temp))
                        time += time_per_frame
                        duration = 0
                        indices = []
                        temp = []
            else:
                for t in times:
                    value = coeff[t[1][0]:t[1][-1] + 1]
                    current_coeff.append(np.mean(value))
            mfccs.append(current_coeff)
        mfccs = np.transpose(mfccs)

        for index, t in enumerate(times):
            feature_times.append((t[0], mfccs[index]))

        return feature_times
    else:
        time_per_frame = np.divide(file_duration, len(feature_data))

        for frame in feature_data:
            if duration < interval_seconds:
                temp.append(frame)
                duration += time_per_frame
                time += time_per_frame
            else:
                temp.append(frame)
                timestamp = float("{0:.3f}".format(time))
                feature_times.append((timestamp, np.mean(temp)))
                time += time_per_frame
                duration = 0
                temp = []

        return feature_times


def write_audiocsv(audio_path: str, dest_path: str, feature: str, interval_seconds: float = 1.0):
    """Extracts the chosen audio feature from the audio file and writes it to a csv file
    :param audio_path: Path of the audio file
    :param dest_path: destination of the resulting csv file
    :param feature: the audio feature to be extracted
    :param interval_seconds: the length of the audio partitions. defaults to 1.0 seconds"""
    feature_data = partition_feature(audio_path, feature, interval_seconds)
    with open(dest_path, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        if feature == "mfcc":
            col_names = ["Time"]
            print(feature_data[0][1])
            for i in range(1, len(feature_data[0][1]) + 1):
                col_names.append("mfcc" + str(i))
            writer.writerow(col_names)

            for e in feature_data:
                cells = [e[0]]
                for x in e[1]:
                    cells.append(x)

                writer.writerow(cells)
        else:
            writer.writerow(["Time", feature])
            for e in feature_data:
                writer.writerow([e[0], e[1]])
