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
    test = librosa.util.frame(y, frame_length=1024, hop_length=128)
    print("shape of y ", y.shape)
    print("shape of librosa.util.frame(y) ", test.shape)
    print("Samplerate: ", sr)

    print("length of complete audio signal: ", len(y))

    S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
    print("shape of S", S.shape)
    print("length of S[0]: ", len(S[0]))
    print(S[0])
    print(S[0][0])
    rms = librosa.feature.rmse(S=S)
    print("length of rms.T: ", len(rms.T))
    print("shape of rms ", rms.shape)

    plt.figure()
    plt.subplot(311)
    # plt.semilogy(rms.T, label='RMS Energy')
    plt.plot(y)
    # plt.xticks([])
    # plt.xlim([0, rms.shape[-1]])
    plt.legend(loc='best')
    plt.subplot(312)

    test = librosa.amplitude_to_db(S, ref=np.max)
    print("shape of librosa.amplitude_to_db:", test.shape)

    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    print("shape of librosa.feature.melspectrogram", mel.shape)
    print("shape of librosa.power_to_db(mel)", librosa.power_to_db(mel).shape)
    print("shape of librosa.amplitude_do_db(mel", librosa.amplitude_to_db(mel).shape)
    librosa.display.specshow(librosa.power_to_db(mel, ref=np.max), sr=sr, y_axis='log', x_axis='time')

    plt.subplot(313)
    librosa.display.specshow(librosa.amplitude_to_db(mel, ref=np.max), sr=sr, y_axis='log', x_axis='time')

    plt.title('log Power spectrogram')
    plt.tight_layout()

    plt.show()


def get_energy(path: str) -> np.ndarray:
    block_gen = sf.blocks(path, blocksize=1024)
    rate = sf.info(path).samplerate
    duration = sf.info(path).duration

    energy_list = []

    for y in block_gen:
        # y = np.mean(bl, axis=0)
        S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        rms = librosa.feature.rmse(S=S)
        m = np.mean(rms)
        energy_list.append(m)

    block_gen.close()
    # l = len(energy_list)
    # dec = np.array_split(np.array(energy_list), l / 10)
    # print(len(dec))

    # energy_list = [np.mean(a) for a in dec]

    # block_duration = np.divide(duration, len(energy_list))
    # times = []
    # time = 0
    # i = 1
    # while i <= len(energy_list):
    #     times.append(time)
    #     time += block_duration
    #     i += 1
    return np.array(energy_list)


def plot_energy(energy: np.array):
    plt.figure()
    plt.subplot(211)
    plt.title("")
    # plt.plot(times, np.array(testlist))
    # plt.semilogy(times, energy, color="b", label="RMS Energy")
    plt.semilogy(energy, color="b", label="RMS Energy")
    plt.legend(loc='best')

    # plt.xlim(0, duration)
    plt.xlim(0, len(energy))
    plt.xlabel("seconds")

    plt.subplot(212)
    # librosa.display.specshow(np.array(chromas), y_axis='chroma', x_axis='time')

    plt.title('Hellraiser RMS Energy')
    plt.tight_layout()

    plt.show()


def blockwise_processing(path):
    block_gen = sf.blocks(path, blocksize=2048)
    rate = sf.info(path).samplerate
    duration = sf.info(path).duration
    testlist = []

    i = 1
    for y in block_gen:
        mel = librosa.feature.melspectrogram(y=y)
        a = librosa.power_to_db(mel)
        # S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        # a= librosa.amplitude_to_db(S, ref=np.max)

        m = np.mean(a)
        test = [np.mean(x) for x in a]

        if i == 1:
            print(a.shape)
            print(mel.shape)
            # print(a)
            print(test)
            i += 1
        testlist.append(test)

    print(np.array(testlist).T.shape)
    asdf = np.array(testlist).T
    block_gen.close()

    plt.figure()
    plt.title("")
    librosa.display.specshow(asdf, y_axis='log', x_axis='time')

    plt.tight_layout()
    plt.show()


def main():
    selfie_audio = os.path.join(PAR_DIR, DATA_DIR, "selfiefromhell.wav")

    hellraiser_audio = os.path.join(PAR_DIR, DATA_DIR, "hellraiser.wav")

    time = datetime.now()
    blockwise_processing(selfie_audio)
    # rms_energy(selfie_audio)
    time2 = datetime.now()
    diff = time2 - time

    print(diff)


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
