import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
from datetime import datetime

CUR_DIR = os.path.dirname(__file__)
PAR_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
DATA_DIR = "testfiles"

audio_path = os.path.join(PAR_DIR, DATA_DIR, "selfiefromhell.wav")


# audio_path = os.path.join(PAR_DIR, DATA_DIR, "hellraiser.wav")


def rms_energy(audiofile):
    y, sr = librosa.load(audiofile)

    S = librosa.magphase(librosa.stft(y, window=np.ones, center=False))[0]
    rms = librosa.feature.rmse(S=S)
    # rms = librosa.feature.rmse(y=y)

    plt.figure()
    plt.subplot(211)
    plt.semilogy(rms.T, label='RMS Energy')
    plt.xticks([])
    plt.xlim([0, rms.shape[-1]])
    plt.legend(loc='best')
    plt.subplot(212)

    test = librosa.amplitude_to_db(S, ref=np.max)
    librosa.display.specshow(test, y_axis='log', x_axis='time')

    plt.title('log Power spectrogram')
    plt.tight_layout()

    plt.show()


def test(path):
    block_gen = sf.blocks(path, blocksize=1024)
    testlist = []

    for bl in block_gen:
        y = np.mean(bl, axis=1)

        # rms = librosa.feature.rmse(y=y)
        S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        rms = librosa.feature.rmse(S=S)
        m = np.mean(rms)
        testlist.append(m)

    l = len(testlist)

    # plt.figure()
    plt.subplot(211)
    plt.title("")
    plt.semilogy(testlist, label="RMS Energy")
    plt.xlim(0, l)

    # plt.subplot(212)

    # Das ganze Problem bei diesem blockweisen einlesen ist, dass für jeden Block ein array erstellt wird
    # als wäre der Block die ganze audio file
    # um das für die ganze audio file zu plotten müsste ich aber alle diese arrays zusammenkleben und dann plotten,
    # aber anscheinend geht das nicht,

    # plt.subplot(311)
    # plt.title('Hellraiser 1/3')
    # i = l//3
    # plt.semilogy(testlist[0:i])
    #
    # plt.subplot(312)
    # plt.title('Hellraiser 2/3')
    #
    # j = 2*l//3
    # plt.semilogy(testlist[i:j])
    #
    # plt.subplot(313)
    # plt.title('Hellraiser 3/3')
    #
    # k = 2*l//3
    # plt.semilogy(testlist[k:])

    plt.tight_layout()
    # plt.show()


def test2(path):
    block_gen = sf.blocks(path, blocksize=1024)
    testlist = []

    for bl in block_gen:
        y = np.mean(bl, axis=1)
        testlist.append(y)

    flat_list = [item for sublist in testlist for item in sublist]
    y = np.array(flat_list)

    S = librosa.magphase(librosa.stft(y, window=np.ones, center=False))[0]
    rms = librosa.feature.rmse(S=S)

    # plt.figure()
    plt.subplot(212)
    plt.title("")
    plt.semilogy(rms.T, label="RMS Energy")
    plt.xlim(0, rms.shape[-1])

    plt.tight_layout()
    # plt.show()


def main():
    time = datetime.now()
    rms_energy(audio_path)
    # test(audio_path)
    time2 = datetime.now()
    diff = time2 - time
    print("alle features etc für jeden block einzeln berechnen:")
    print(diff)

    # time = datetime.now()
    # test2(audio_path)
    # time2 = datetime.now()
    # diff = time2 - time
    #
    # print("blöcke sammeln und dann die liste flatten")
    # print(diff)
    #
    # plt.show()


if __name__ == '__main__':
    main()
