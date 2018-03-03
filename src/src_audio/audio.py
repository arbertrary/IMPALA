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

    print("complete")
    y, sr = librosa.load(audio_path)

    S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
    rms = librosa.feature.rmse(S=S)

    test = librosa.amplitude_to_db(S, ref=np.max)

    plt.subplot(211)
    plt.semilogy(rms.T, label='RMS Energy')
    plt.subplot(212)
    librosa.display.specshow(test, sr=22050, y_axis='log', x_axis='time')
    plt.colorbar(format='%+2.0f dB')

    plt.title('log Power spectrogram')
    plt.tight_layout()

    plt.show()


def get_feature(path: str, feature: str, block_size: int = 2048) -> np.array:
    """Calculates the rms energy for an audio file by blockwise reading.
    :param path: path of audio file
    :param block_size: default 2048 frames per block
    :returns np.array"""

    if feature not in ["energy", "tuning"]:
        raise ValueError("Wrong audio feature")

    block_gen = sf.blocks(path, blocksize=block_size)

    result_list = []

    for y in block_gen:
        S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        # rms = librosa.feature.rmse(S=S)

        if feature == "energy":
            rms = librosa.feature.rmse(y=y)
            result = np.mean(rms)
        else:
            result = librosa.estimate_tuning(y)

        result_list.append(result)

    block_gen.close()
    # energy = np.array(result_list)
    return np.array(result_list)


def normalize(energy: np.array):
    mean = np.mean(energy)
    print(mean)
    # test1 = [x-mean for x in energy]
    # test1data =pd.DataFrame(test1)
    # print(test1data.describe())
    test2 = [x / mean for x in energy]
    test2data = pd.DataFrame(test2)
    print(np.median(test2))

    # plt.subplot(211)
    # plt.plot(energy)
    # plt.subplot(312)
    # plt.plot(test1)
    # plt.subplot(212)
    # plt.plot(test2)
    # plt.show()
    return test2


def partition_audiofeature(path: str, feature: str, interval_seconds: float = 1.0):
    """Partitions (currently) die energy of an audio file into intervals.
    :param path: audio file path
    :param interval_seconds: duration of intervals in seconds as float. defaults to 1s"""
    duration = sf.info(path).duration

    feature = get_feature(path, feature)
    time_per_frame = np.divide(duration, len(feature))

    feature_times = []
    time = 0
    duration = 0
    temp = []
    for frame in feature:
        if duration < interval_seconds:
            duration += time_per_frame
            time += time_per_frame
            temp.append(frame)
        else:
            feature_times.append((round(time), np.mean(temp)))
            # feature_times.append((time, temp))
            time += time_per_frame
            duration = 0
            temp = []

    # x = [x[0] for x in feature_times]
    # y = [y[1] for y in feature_times]
    # plt.plot(x, y)
    # plt.tight_layout()
    # plt.show()
    return feature_times


def __plot_energy(energy: np.array):
    """Helper function to plot the audio energy calculated in get_feature"""
    # plt.figure()
    plt.subplot(211)
    plt.title("")
    # plt.semilogy(times, energy, color="b", label="RMS Energy")
    # plt.semilogy(energy, color="b", label="RMS Energy")
    plt.plot(energy)
    plt.legend(loc='best')

    plt.xlim(0, len(energy))
    plt.xlabel("seconds")

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
    # testlist = util.sliding_window(testlist, 1000)
    # plt.plot(testlist)
    # plt.ylim(-0.5, 0.5)
    # plt.xlim(0,len(testlist))
    # plt.tight_layout()
    # plt.show()
    # return asdf


def write_audiocsv(audio_path: str, dest_path: str, feature: str):
    feature = partition_audiofeature(audio_path, feature)
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

    data = ["blade.wav", "hellboy.wav", "predator.wav", "scream_ger.wav", "star-wars-4.wav", "the-matrix.wav"]

    audio1csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "blade.csv")
    audio2csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "hellboy.csv")
    audio3csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "predator.csv")
    audio4csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "scream_ger.csv")
    audio5csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "star-wars-4.csv")

    for d in data:
        new_name = d.replace(".wav", "_tuning.csv")
        path = os.path.join(BASE_DIR, "data/data_audio", d)
        write_audiocsv(path, new_name, feature="tuning")

    # blockwise_processing(audio5)
    # partition_audiofeature(testaudio, "tuning")


if __name__ == '__main__':
    main()
