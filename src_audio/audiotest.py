import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display


CUR_DIR = os.path.dirname(__file__)
PAR_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
DATA_DIR = "testfiles"

audio_path = os.path.join(PAR_DIR, DATA_DIR, "selfiefromhell.mp3")


def rms_energy(audiofile):
    y, sr = librosa.load(audiofile)


    S = librosa.magphase(librosa.stft(y, window=np.ones, center=False))[0]
    rms = librosa.feature.rmse(S=S)

    plt.figure()
    plt.subplot(211)
    plt.semilogy(rms.T, label='RMS Energy')
    plt.xticks([])
    plt.xlim([0, rms.shape[-1]])
    plt.legend(loc='best')
    plt.subplot(212)
    librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time')

    plt.title('log Power spectrogram')
    plt.tight_layout()

    plt.show()


def main():
    rms_energy(audio_path)


if __name__ == '__main__':
    main()

