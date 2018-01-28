import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, os.pardir))


def rms_energy(audiofile):
    print("complete")
    y, sr = librosa.load(audiofile)
    # test = librosa.util.frame(y, frame_length=1024, hop_length=128)
    # print("shape of y ", y.shape)
    # print("shape of librosa.util.frame(y) ", test.shape)
    # print("Samplerate: ", sr)
    # print("length of complete audio signal: ", len(y))

    S = librosa.magphase(librosa.stft(y, window=np.ones))[0]
    # print("shape of S", S.shape)
    # print("length of S[0]: ", len(S[0]))
    # print(S[0])
    # print(S[0][0])
    rms = librosa.feature.rmse(S=S)
    # print("length of rms.T: ", len(rms.T))
    # print("shape of rms ", rms.shape)

    # plt.figure()
    # plt.subplot(311)
    # plt.semilogy(rms.T, label='RMS Energy')
    # plt.plot(y)
    # plt.xticks([])
    # plt.xlim([0, rms.shape[-1]])
    # plt.legend(loc='best')
    # plt.subplot(312)

    test = librosa.amplitude_to_db(S, ref=np.max)
    # print("shape of librosa.amplitude_to_db:", test.shape)

    mel = librosa.feature.melspectrogram(y=y)
    # mfccs = librosa.feature.mfcc(y=y, sr=sr)

    # print("shape of librosa.feature.melspectrogram", mel.shape)
    # print("shape of librosa.power_to_db(mel)", librosa.power_to_db(mel).shape)
    # print("shape of librosa.amplitude_do_db(mel", librosa.amplitude_to_db(mel).shape)

    d = librosa.power_to_db(mel)
    librosa.display.specshow(test, sr=22050, y_axis='log', x_axis='time')
    # librosa.display.specshow(mfccs, x_axis="time")
    plt.colorbar(format='%+2.0f dB')

    # plt.subplot(313)
    # librosa.display.specshow(librosa.amplitude_to_db(mel, ref=np.max), sr=sr, y_axis='log', x_axis='time')

    # plt.title('log Power spectrogram')
    # plt.tight_layout()

    # plt.show()


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


def partition_audiofeature(path: str, dialogue_duration: float):
    """Teilt die Ergebniswerte der Audiofeatures in Intervalle von X Sekunden """
    duration = sf.info(path).duration
    energy = get_energy(path)

    print(duration)
    print(len(energy))
    time_per_frame = np.divide(duration, len(energy))
    print(time_per_frame)

    energy_times = []
    time = 0
    duration = 0
    temp = []

    # Hier könnte ich auch die average timedifference aus subtitles.py benutzen, sodass es individuell für jede film ist
    for frame in energy:
        if duration < dialogue_duration:
            duration += time_per_frame
            time += time_per_frame
            temp.append(frame)
        else:
            energy_times.append((time, temp))
            duration = 0
            temp = []

    for e in energy_times:
        print(e)

    # plot_energy(np.array(energy_times[0][1]))


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
        # Varianten:

        # D = librosa.magphase(librosa.stft(y, window=np.ones))[0]
        # D = librosa.stft(y)
        D = librosa.feature.melspectrogram(y=y)
        # D = librosa.feature.melspectrogram(y=y, sr=22050, n_mels=256)
        # a = librosa.amplitude_to_db(D)
        a = librosa.power_to_db(D)
        # a = librosa.feature.mfcc(y=y, sr=22050)

        test = [np.mean(x) for x in a]

        if i == 1:
            # print(a.shape)
            # print(mel.shape)
            # print(a)
            # print(test)
            i += 1
        testlist.append(test)
        i += 1

    print(np.array(testlist).T.shape)
    asdf = np.array(testlist).T
    block_gen.close()
    block_duration = duration / i
    test = duration / len(testlist)
    print("duration: ", block_duration, test)
    # plt.figure()
    # plt.title("")
    librosa.display.specshow(asdf, sr=22050, y_axis='mel', x_axis='frames')
    plt.colorbar(format='%+2.0f dB')
    # np.savetxt("test.csv", asdf, delimiter=",")
    plt.tight_layout()
    # plt.show()


def main():
    selfie_audio = os.path.join(BASE_DIR, "src/testfiles/" "selfiefromhell.wav")
    # # print(sf.info(selfie_audio).duration)
    # hellraiser_audio = os.path.join(BASE_DIR, "src/testfiles/", "hellraiser.wav")
    #
    # time = datetime.now()
    # plt.subplot(211)
    # # plt.title("blockwise")
    # # blockwise_processing(selfie_audio)
    # # plt.subplot(212)
    # # plt.title("als ganzes")
    # rms_energy(selfie_audio)
    # time2 = datetime.now()
    # diff = time2 - time
    #
    # print(diff)
    # plt.show()
    partition_audiofeature(selfie_audio, 2.5)


if __name__ == '__main__':
    main()
