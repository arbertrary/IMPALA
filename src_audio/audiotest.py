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


def rms_energy(audiofile):
    print("complete")
    y, sr = librosa.load(audiofile)
    print("Samplerate: ", sr)

    print("length of complete audio signal: ", len(y))

    S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
    print(S.shape)
    rms = librosa.feature.rmse(S=S)
    print("length of rms.T: ", len(rms.T))
    print(rms.shape)

    plt.figure()
    plt.subplot(211)
    plt.semilogy(rms.T, label='RMS Energy')
    # plt.xticks([])
    plt.xlim([0, rms.shape[-1]])
    plt.legend(loc='best')
    plt.subplot(212)

    test = librosa.amplitude_to_db(S, ref=np.max)
    print("shape of librosa.amplitude_to_db:", test.shape)

    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    print("shape of librosa.feature.melspectrogram", mel.shape)
    print("shape of librosa.power_to_db(mel)", librosa.power_to_db(mel).shape)
    librosa.display.specshow(librosa.power_to_db(mel), sr=sr, y_axis='log', x_axis='time')
    # librosa.display.specshow(S, sr=sr, y_axis='log', x_axis='time')

    plt.title('log Power spectrogram')
    plt.tight_layout()

    plt.show()


def test(path):
    block_gen = sf.blocks(path, blocksize=1024)
    rate = sf.info(path).samplerate
    duration = sf.info(path).duration
    print(rate)
    testlist = []

    i = 1
    for bl in block_gen:
        y = np.mean(bl, axis=1)
        S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        rms = librosa.feature.rmse(S=S)
        m = np.mean(rms)
        testlist.append(m)


    block_gen.close()
    l = len(testlist)
    dec = np.array_split(np.array(testlist), l/100)
    print(len(dec))

    testlist = [np.mean(a) for a in dec]

    block_duration = np.divide(duration, len(testlist))
    times = []
    time = 0
    i = 1
    while i <= len(testlist):
        times.append(time)
        time += block_duration
        i += 1

    print(l)

    plt.figure()
    plt.subplot(211)
    plt.title("")
    plt.plot(times, np.array(testlist))
    plt.semilogy(times, np.array(testlist), color="b", label="RMS Energy")
    plt.legend(loc='best')

    plt.xlim(0, duration)
    plt.xlabel("seconds")

    plt.subplot(212)
    # librosa.display.specshow(np.array(chromas), y_axis='chroma', x_axis='time')

    plt.title('Hellraiser RMS Energy')
    plt.tight_layout()

    # Das ganze Problem bei diesem blockweisen einlesen ist, dass für jeden Block ein array erstellt wird
    # als wäre der Block die ganze audio file
    # um das für die ganze audio file zu plotten müsste ich aber alle diese arrays zusammenkleben und dann plotten,
    # aber anscheinend geht das nicht,

    plt.tight_layout()
    plt.show()


def test2(path):
    print("blockwise:")
    rate = sf.info(path).samplerate
    print("samplerate: ", rate)

    block_gen = sf.blocks(path, blocksize=1024)
    testlist = []

    for bl in block_gen:
        # np.mean ist nötig weil die blöcke ein 2D array der Länge l=blocksize
        # mit subarrays length 2 sind
        # np.mean macht daraus ein einzelnes Array der länge blocksize
        y = np.mean(bl, axis=1)

        testlist.extend(y)
    block_gen.close()

    y = np.array(testlist)
    print("length of block list: ", len(y))

    S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
    rms = librosa.feature.rmse(S=S)

    print("length of rms.T: ", len(rms.T))
    plt.figure()
    plt.subplot(211)
    plt.title("")
    plt.semilogy(rms.T, label="RMS Energy")
    plt.xlim(0, rms.shape[-1])

    plt.subplot(212)

    test = librosa.amplitude_to_db(S, ref=np.max)
    librosa.display.specshow(test, sr=rate, y_axis='log', x_axis='time')
    plt.tight_layout()
    # plt.show()


def main():
    selfie_audio = os.path.join(PAR_DIR, DATA_DIR, "selfiefromhell.wav")

    hellraiser_audio = os.path.join(PAR_DIR, DATA_DIR, "hellraiser.wav")

    time = datetime.now()
    test(hellraiser_audio)
    # test2(selfie_audio)
    # print("")
    # rms_energy(selfie_audio)
    time2 = datetime.now()
    diff = time2 - time

    print(diff)
    # plt.show()

    # info = sf.info(selfie_audio, verbose=True)
    # print(info)
    # print(info.duration)


# block size 1024:
# blocks: 4385
# items in flat list: 4489344

# block size 256:
# blocks: 17537
# 4489344
# rms.T length = 9

# rms_energy:
# length of y = 2244672 (= 4489344/2)
# rms.T length = 4385 (= block anzahl bei block size 1024?)


if __name__ == '__main__':
    main()
