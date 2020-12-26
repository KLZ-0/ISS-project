from iss import plotter
from iss.res import audiopath, frame_size

import numpy as np
import soundfile
from scipy.io import wavfile

from os import path


def load_data(filename):
    # load data
    data, samplerate = soundfile.read(path.join(audiopath, filename))
    data = data[0:samplerate]
    # samplerate, data = wavfile.read(path.join(audiopath, filename))
    # data = data[0:samplerate].astype(np.float32)

    # remove DC part
    data -= np.mean(data)

    # normalize (peaks will be 1 and -1)
    data /= np.abs(data).max()

    # plot
    plotter.plot(data, path.splitext(filename)[0] + ".pdf")

    return data, samplerate


def load_frames(filename):
    data, samplerate = load_data(filename)

    # 20ms frames @ 16kHz
    frame_len = int(frame_size * (samplerate / 1000))
    frame_step = int(frame_len/2)

    frames = []
    for i in range(99):
        frames.append(data[i*frame_step:(i*frame_step) + frame_len])

    return frames


def process_file(filename):
    frames = load_frames(filename)
    plotter.plot(frames[0], path.splitext(filename)[0] + "_frame.pdf")
