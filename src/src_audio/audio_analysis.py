"""Module for processing audio files.
Functions for alculating RMS energy or other audio features (mel spectrogram etc)."""


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
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


def get_energy(path: str, block_size: int = 2048) -> np.array:
    """Calculates the rms energy for an audio file by blockwise reading.
    :param path: path of audio file
    :param block_size: default 2048 frames per block
    :returns np.array"""
    block_gen = sf.blocks(path, blocksize=block_size)

    energy_list = []

    for y in block_gen:
        S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        # rms = librosa.feature.rmse(S=S)
        rms = librosa.feature.rmse(y=y)
        m = np.mean(rms)
        energy_list.append(m)

    block_gen.close()
    return np.array(energy_list)


def partition_audiofeature(path: str, interval_seconds: float = 1.0):
    """Partitions (currently) die energy of an audio file into intervals.
    :param path: audio file path
    :param interval_seconds: duration of intervals in seconds as float. defaults to 1s"""
    duration = sf.info(path).duration
    energy = get_energy(path)

    time_per_frame = np.divide(duration, len(energy))

    energy_times = []
    time = 0
    duration = 0
    temp = []
    for frame in energy:
        if duration < interval_seconds:
            duration += time_per_frame
            time += time_per_frame
            temp.append(frame)
        else:
            energy_times.append((round(time), np.mean(temp)))
            # energy_times.append((time, temp))
            duration = 0
            temp = []
    return energy_times


def __plot_energy(energy: np.array):
    """Helper function to plot the audio energy calculated in get_energy"""
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
        D = librosa.feature.melspectrogram(y=y)
        # D = librosa.feature.melspectrogram(y=y, sr=22050, n_mels=256)
        # a = librosa.amplitude_to_db(D)
        a = librosa.power_to_db(D)
        # a = librosa.feature.mfcc(y=y, sr=22050)

        test = [np.mean(x) for x in a]

        testlist.append(test)
    print(np.array(testlist).T.shape)
    asdf = np.array(testlist).T
    block_gen.close()

    return asdf


def main():
    selfie_audio = os.path.join(BASE_DIR, "src/testfiles/" "selfiefromhell.wav")
    # hellraiser_audio = os.path.join(BASE_DIR, "src/testfiles/", "hellraiser.wav")
    star_wars_audio = os.path.join(BASE_DIR, "src/testfiles", "star-wars-4.wav")
    # blade_audio = os.path.join(BASE_DIR, "src/testfiles/", "blade.wav")

    energy = partition_audiofeature(star_wars_audio)
    data = pd.DataFrame(energy)
    print(data.describe())
    time = datetime.now()
    time2 = datetime.now()
    diff = time2 - time

    print(diff)


if __name__ == '__main__':
    main()
