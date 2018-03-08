"""Module for processing audio files.
Functions for alculating RMS energy or other audio features (mel spectrogram etc)."""

import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
import src.utility as util
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir))


def rms_energy(audio_path: str):
    """Plots the RMS energy and a log power spectrogram of a complete audio file
    1:1 implementation of a librosa example. Not suited for entire movies
    :raises MemoryError if the duration of the audio is longer than 500s. Just for safety."""
    if sf.info(audio_path).duration > 500:
        raise MemoryError("Audio file too large!")

    y, sr = librosa.load(audio_path)

    S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
    rms = librosa.feature.rmse(S=S)
    # rms = librosa.feature.spectral_centroid(S=S)
    test = librosa.amplitude_to_db(S, ref=np.max)

    mfccs = librosa.feature.mfcc(y, sr)
    print(mfccs.shape)

    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=4)
    print(mfccs.T[0])
    print(mfccs.shape)
    print(np.max(mfccs[0]), np.min(mfccs[0]))

    plt.figure()
    plt.subplot(211)
    plt.semilogy(rms.T, label='RMS Energy')
    plt.xticks([])
    # plt.xlim([0, rms.shape[-1]])
    plt.legend(loc="best")
    plt.subplot(212)
    # librosa.display.specshow(test, sr=22050, y_axis='log', x_axis='time')
    # plt.title('log Power spectrogram')
    librosa.display.specshow(mfccs, x_axis="time")
    # plt.plot(mfccs.T)
    plt.title("MFCC")
    plt.tight_layout()

    plt.show()


def get_feature(path: str, feature: str, block_size: int = 2048, **kwargs) -> np.array:
    """Calculates the rms energy for an audio file by blockwise reading.
    :param path: path of audio file
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
            # rms = librosa.feature.rmse(S=S)
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
        # at this point, r is in the same shape as when directly calling librosa.feature.mfccs
        # on the entire audio file
        # but is this even necessary?
        # ich meine im endeffekt will ich ja eh die 4 mfccs pro frame
        # also wär's doch sinnvoller das garnicht wieder zu transponieren...
        r = np.transpose(np.array(result_list))
    else:
        r = np.array(result_list)
    return r


def partition_feature(path: str, feature: str, interval_seconds: float = 1.0, **kwargs):
    file_duration = sf.info(path).duration

    feature_data = get_feature(path, feature, **kwargs)
    n_part = round(file_duration / interval_seconds)

    feature_times = []
    time = 0.0
    if feature == "mfcc":
        mfccs = []
        for coeff in feature_data:
            partitions = [np.mean(p) for p in util.split(coeff, n_part)]
            mfccs.append(partitions)

        for frame in np.transpose(mfccs):
            feature_times.append((time, frame))
            time += interval_seconds

    else:
        partitions = list(util.split(feature_data, n_part))
        for p in partitions:
            print(len(p))
            feature_times.append((time, np.mean(p)))
            time += interval_seconds

    return feature_times


def partition_old(path: str, feature: str, interval_seconds: float = 1.0):
    """Partitions (currently) die energy of an audio file into intervals.
    :param path: audio file path
    :param interval_seconds: duration of intervals in seconds as float. defaults to 1s"""
    file_duration = sf.info(path).duration

    feature_data = get_feature(path, feature, n_mfcc=4)
    feature_times = []
    time = 0
    duration = 0
    temp = []
    time_per_frame = np.divide(file_duration, len(feature_data))
    print(time_per_frame)
    for frame in feature_data:
        if duration < interval_seconds:
            duration += time_per_frame
            time += time_per_frame
            temp.append(frame)
        else:
            # feature_times.append((round(time), np.mean(temp)))
            timestamp = float("{0:.3f}".format(time))
            feature_times.append((timestamp, np.mean(temp)))
            time += time_per_frame
            duration = 0
            temp = []

    return feature_times


def __plot_feature(feature: np.array, duration):
    """Helper function to plot the audio energy calculated in get_feature"""
    block_dur = duration / len(feature)
    time = 0
    x = []
    for e in feature:
        x.append(time)
        time += block_dur

    minor_ticks = np.arange(0, x[-1], 5)

    plt.figure(figsize=(15, 5))
    # plt.subplot(211)
    plt.title("Tuning deviation for a test file: Musical Notes A3 (220 Hz), A4 (440 Hz), A5 (880 Hz), A6 (1760 Hz)")
    # plt.semilogy(times, energy, color="b", label="RMS Energy")
    # plt.semilogy(energy, color="b", label="RMS Energy")
    # plt.plot(energy)
    # plt.semilogy(x, energy, label="RMS Energy")
    plt.plot(feature, label="Tuning Deviation (smoothed with sliding window of size 10)")

    plt.legend(loc='best')
    # plt.xticks(minor_ticks)
    # plt.xlim(x[0], x[-1])
    plt.xlim(0, len(feature))
    plt.ylabel("Tuning Deviation")
    plt.xlabel("Frames")

    plt.tight_layout()

    plt.show()


def blockwise_processing(path):
    """Currently just a function to try out things.
    mainly blockwise calculation of other audio features than rms energy"""
    block_gen = sf.blocks(path, blocksize=2048)
    rate = sf.info(path).samplerate
    duration = sf.info(path).duration
    testlist = []

    i = 1
    for y in block_gen:
        # Varianten:
        # D = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        # D = librosa.stft(y)
        # D = librosa.feature.melspectrogram(y=y)
        # D = librosa.feature.melspectrogram(y=y, sr=22050, n_mels=256)
        # a = librosa.amplitude_to_db(D)
        # a = librosa.power_to_db(D)
        # a = librosa.feature.mfcc(y=y, sr=22050)
        # test = [np.mean(x) for x in a]

        test = librosa.estimate_tuning(y)

        testlist.append(test)

    block_gen.close()
    return np.array(testlist)


def write_audiocsv(audio_path: str, dest_path: str, feature: str):
    feature = partition_old(audio_path, feature, interval_seconds=0.5)
    with open(dest_path, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for e in feature:
            writer.writerow([e[0], e[1]])


def main():
    audio1 = os.path.join(BASE_DIR, "data/data_audio", "blade.wav")
    audio2 = os.path.join(BASE_DIR, "data/data_audio", "hellboy.wav")
    audio3 = os.path.join(BASE_DIR, "data/data_audio", "predator.wav")
    audio4 = os.path.join(BASE_DIR, "data/data_audio", "scream_ger.wav")
    audio5 = os.path.join(BASE_DIR, "data/data_audio", "star-wars-4.wav")
    audio6 = os.path.join(BASE_DIR, "data/data_audio", "the-matrix.wav")
    testaudio = os.path.join(BASE_DIR, "data/data_audio", "selfiefromhell.wav")
    testaudio = os.path.join(BASE_DIR, "src/testfiles", "220_440_880_1760.wav")
    # testaudio = os.path.join(BASE_DIR, "src/testfiles", "440_880_1760.wav")

    data = [audio1, audio2, audio3, audio4, audio5, audio6]

    audio1csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "blade.csv")
    audio2csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "hellboy.csv")
    audio3csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "predator.csv")
    audio4csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "scream_ger.csv")
    audio5csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "star-wars-4.csv")

    time = datetime.now()
    # test = partition_feature(testaudio, feature="mfcc", interval_seconds=0.5, n_mfcc=4)
    test = get_feature(testaudio, feature="tuning")
    test = util.sliding_window(list(test), 10)
    duration = sf.info(testaudio).duration
    __plot_feature(test, duration)
    # test2 = partition_old(testaudio, feature="energy", interval_seconds=0.5)
    # print(len(test), len(test2))
    # print(test)
    # print(test2)

    time2 = datetime.now()
    diff = time2 - time

    print(diff)


if __name__ == '__main__':
    main()
