import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
from librosa.feature import chroma_stft

CUR_DIR = os.path.dirname(__file__)
PAR_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
DATA_DIR = "testfiles"

# audio_path = os.path.join(PAR_DIR, DATA_DIR, "selfiefromhell.wav")
audio_path = os.path.join(PAR_DIR, DATA_DIR, "hellraiser.wav")


def rms_energy(audiofile):
    y, sr = librosa.load(audiofile)

    S = librosa.magphase(librosa.stft(y, window=np.ones, center=False))[0]
    # rms = librosa.feature.rmse(S=S)
    rms = librosa.feature.rmse(y=y)

    plt.figure()
    plt.subplot(211)
    plt.semilogy(rms.T, label='RMS Energy')
    plt.xticks([])
    plt.xlim([0, rms.shape[-1]])
    plt.legend(loc='best')
    # plt.subplot(212)
    # librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time')

    plt.title('log Power spectrogram')
    plt.tight_layout()

    plt.show()


def test(path):
    block_gen = sf.blocks(path, blocksize=2048)
    testlist = []
    for bl in block_gen:
        y = np.mean(bl, axis=1)
        rms = librosa.feature.rmse(y=y)

        # S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        # rms = librosa.feature.rmse(S=S)

        m = np.median(rms)
        testlist.append(m)

    l = len(testlist)

    plt.figure(figsize=(20, 5))

    plt.subplot(311)
    i = l//3
    plt.semilogy(testlist[0:i])
    plt.subplot(312)
    j = 2*l//3
    plt.semilogy(testlist[i:j])
    plt.subplot(313)
    k = 2*l//3
    plt.semilogy(testlist[k:])


    plt.tight_layout()

    plt.show()



def main():
    # rms_energy(audio_path)
    test(audio_path)
    # plt.show()


if __name__ == '__main__':
    main()
