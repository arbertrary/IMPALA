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


def get_feature(path: str, feature: str, block_size: int = 2048, n_mfcc=20) -> np.array:
    """Calculates the rms energy for an audio file by blockwise reading.
    :param path: path of audio file
    :param block_size: default 2048 frames per block
    :returns np.array"""

    # if feature not in ["energy", "tuning"]:
    #     raise ValueError("Wrong audio feature")

    block_gen = sf.blocks(path, blocksize=block_size)

    result_list = []
    test = []
    for y in block_gen:
        test.append(y)
        S = librosa.magphase(librosa.stft(y, window=np.ones))[0]

        if feature == "energy":
            rms = librosa.feature.rmse(S=S)
            # rms = librosa.feature.rmse(y=y)
            result = np.mean(rms)
        elif feature == "tuning":
            result = librosa.estimate_tuning(y, fmin=50.0, fmax=2000.0)
        elif feature == "mfcc":
            mfccs = librosa.feature.mfcc(y, n_mfcc=n_mfcc)
            result = [np.mean(x) for x in mfccs]
        elif feature == "centroid":
            # rolloff = librosa.feature.spectral_rolloff(y)
            # result = np.mean(rolloff.T)
            freq = librosa.feature.spectral_centroid(y)
            result = np.mean(freq.T)
        else:
            pitches, magnitude = librosa.piptrack(y)
            print(pitches.shape)
            result = [np.mean(x) for x in pitches]
            print(np.array(result).shape)
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
    file_duration = sf.info(path).duration

    feature_data = get_feature(path, feature, n_mfcc=4)
    print(feature_data.shape)
    feature_times = []
    time = 0
    duration = 0
    temp = []
    if feature == "mfcc":
        time_per_frame = np.divide(file_duration, len(feature_data.T))
        print(time_per_frame)
        all_mfccs = []
        time_list = []
        for index, mfcc in enumerate(feature_data):
            time = 0
            duration = 0
            temp = []
            current_mfcc = []

            for frame in mfcc:
                if duration < interval_seconds:
                    duration += time_per_frame
                    time += time_per_frame
                    temp.append(frame)
                else:
                    time_stamp = float("{0:.3f}".format(time))
                    if index == 0:
                        time_list.append(time_stamp)

                    current_mfcc.append(np.mean(temp))
                    time += time_per_frame
                    duration = 0
                    temp = []

            all_mfccs.append(current_mfcc)

        results = [time_list, all_mfccs[0], all_mfccs[1], all_mfccs[2], all_mfccs[3]]
        print(np.array(results).shape)
        for r in results:
            print(len(r))
    else:
        time_per_frame = np.divide(file_duration, len(feature_data))
        print(time_per_frame)
        for frame in feature_data:
            if duration < interval_seconds:
                duration += time_per_frame
                time += time_per_frame
                temp.append(frame)
            else:
                # feature_times.append((round(time), np.mean(temp)))
                time = float("{0:.3f}".format(time))
                feature_times.append((time, np.mean(temp)))
                time += time_per_frame
                duration = 0
                temp = []

    # x = [x[0] for x in feature_times]
    # y = [y[1] for y in feature_times]
    # plt.plot(x, y)
    # plt.tight_layout()
    # plt.show()
    return feature_times


def __plot_energy(energy: np.array, duration):
    """Helper function to plot the audio energy calculated in get_feature"""
    block_dur = duration / len(energy)
    time = 0
    x = []
    for e in energy:
        x.append(time)
        time += block_dur

    minor_ticks = np.arange(0, x[-1], 5)

    plt.figure(figsize=(15, 5))
    # plt.subplot(211)
    plt.title("Audio Energy for \"Selfie From Hell\"")
    # plt.semilogy(times, energy, color="b", label="RMS Energy")
    # plt.semilogy(energy, color="b", label="RMS Energy")
    # plt.plot(energy)
    # plt.semilogy(x, energy, label="RMS Energy")
    plt.plot(x, energy, label="RMS Energy")

    plt.legend(loc='best')
    plt.xticks(minor_ticks)
    plt.xlim(x[0], x[-1])
    plt.ylabel("Hz")
    plt.xlabel("Seconds")

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
    feature = partition_audiofeature(audio_path, feature, interval_seconds=0.5)
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
    # testaudio = os.path.join(BASE_DIR, "src/testfiles", "220_440_880.wav")
    # testaudio = os.path.join(BASE_DIR, "src/testfiles", "880_Sine_wave.mp3")

    data = [audio1, audio2, audio3, audio4, audio5, audio6]

    audio1csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "blade.csv")
    audio2csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "hellboy.csv")
    audio3csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "predator.csv")
    audio4csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "scream_ger.csv")
    audio5csv = os.path.join(BASE_DIR, "data/audio_csvfiles", "star-wars-4.csv")

    # for d in data:
    #     new_name = d.replace(".wav", "1024.csv")
    #     path = os.path.join(BASE_DIR, "data/data_audio", d)
    #     write_audiocsv(path, new_name, feature="energy")

    # test = partition_audiofeature(testaudio, feature="energy", interval_seconds=0.5)
    # print(test)
    # feature = get_feature(testaudio, feature="centroid")
    # duration = sf.info(testaudio).duration

    # feature = get_feature(testaudio, feature="mfcc", n_mfcc=4)
    # feature2 = get_feature(testaudio, feature="centroid")
    # feature2 = get_feature(testaudio, feature="energy")
    # feature3 = get_feature(testaudio, feature="tuning")
    # feature3 = util.sliding_window(list(feature3), 10)

    time = datetime.now()
    test = partition_audiofeature(testaudio, feature="mfcc")

    time2 = datetime.now()
    diff = time2 - time

    print(diff)
    # y,sr = librosa.load(testaudio)
    # tuning = librosa.estimate_tuning(y,sr)
    # print(tuning)
    # feature = librosa.feature.mfcc(y,sr)
    # feature2 = librosa.feature.spectral_centroid(y,sr)
    #
    # pitches, magnitude = librosa.piptrack(y)
    # librosa.display.specshow(pitches)
    # plt.show()

    # plt.figure()
    # plt.subplot(211)
    # plt.title("Spectral Centroids of \"Selfie From Hell\"")
    # plt.plot(feature2.T)
    # plt.ylabel("Frequency")
    # plt.xlabel("Frames")
    # plt.xlim(0, len(feature2))
    # plt.subplot(212)
    # plt.title("MFCC Spectrogram of \"Selfie From Hell\"")
    # print(len(feature3))
    # plt.plot(feature3)
    # # plt.xlim(0,len(feature3))
    # # librosa.display.specshow(feature, x_axis="frames")
    # # plt.xlabel("")
    # # plt.colorbar(orientation="horizontal")
    # plt.show()

    # freq = get_feature(testaudio, feature="frequency")
    # mfccs = get_feature(testaudio, feature="mfcc")
    # print(mfccs.shape)
    # piptrack = get_feature(testaudio, feature="piptrack")

    # rms_energy(testaudio)

    # pitches, magnitude = librosa.piptrack(y,sr)
    #
    # print(pitches.shape, magnitude.shape)
    # print(np.max(pitches[400]))

    # time = datetime.now()
    #
    # y,sr = librosa.load(testaudio)
    # test = librosa.feature.spectral_centroid(y)
    # # plt.plot(test.T)
    # plt.semilogy(test.T)
    # plt.show()

    # plt.figure()
    # plt.suptitle("Spectral centroid frequency, Energy and Tuning Deviation for \"Selfie From Hell \"")
    # plt.subplot(311)
    # freq = get_feature(testaudio, "frequency")
    # plt.semilogy(freq.T, label='Spectral centroid frequency')
    # # plt.plot(freq.T, label='Spectral centroid frequency')
    #
    # plt.ylabel('Hz')
    # plt.xlabel("Blocks")
    # # plt.xticks([])
    # plt.xlim([0, freq.shape[-1]])
    # plt.legend()
    # plt.subplot(312)
    # energy = get_feature(testaudio, "energy")
    # plt.semilogy(energy, label="RMS Energy")
    # plt.ylabel("Energy")
    # plt.xlabel("Blocks")
    # plt.xlim(0, len(energy))
    # plt.legend()
    # plt.subplot(313)
    # tuning = get_feature(testaudio, "tuning")
    # tuning = util.sliding_window(list(tuning), 10)
    # plt.plot(tuning, label="Estimated tuning deviation from A440 (smoothed)")
    # plt.ylabel("Tuning deviation")
    # plt.xlabel("Blocks")
    # plt.xlim(0, len(tuning))
    # plt.legend()
    # plt.tight_layout()
    # plt.show()


if __name__ == '__main__':
    main()
