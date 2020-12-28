from os import path

import numpy as np
import soundfile

from iss.res import audiopath, frame_size


def load_data(filename, delay):
    # load data
    data, samplerate = soundfile.read(path.join(audiopath, filename))
    data = data[delay:samplerate + delay]
    # samplerate, data = wavfile.read(path.join(audiopath, filename))
    # data = data[0:samplerate].astype(np.float32)

    # remove DC part
    data -= np.mean(data)

    # normalize (peaks will be 1 and -1)
    data /= np.abs(data).max()

    # plot
    # plotter.plot(data, "1_" + path.splitext(filename)[0] + ".pdf",
    #              title="Signal",
    #              xlabel="Time [ms]")

    return data, samplerate


def load_frames(filename, delay):
    data, samplerate = load_data(filename, delay)

    # 20ms frames @ 16kHz
    frame_len = int(frame_size * (samplerate / 1000))
    frame_step = int(frame_len / 2)

    frames = []
    for i in range(99):
        frames.append(data[i * frame_step:(i * frame_step) + frame_len])

    return frames, samplerate


def load_file_as_frames(filename, delay=0):
    return load_frames(filename, delay)


def load_file_as_signal(filename):
    return soundfile.read(path.join(audiopath, filename))


def save_file(filename, data, samplerate):
    soundfile.write(path.join(audiopath, filename), data, samplerate)
