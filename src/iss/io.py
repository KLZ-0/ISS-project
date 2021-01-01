from os import path

import numpy as np
import soundfile

from iss.res import audiopath, FRAME_DURATION, SAMPLE_DURATION


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

    return data, samplerate


def load_frames(filename, delay, frame_size):
    data, samplerate = load_data(filename, delay)

    totoal_dur = SAMPLE_DURATION * samplerate

    frame_len = int(frame_size * samplerate)
    frame_step = int(frame_len / 2)

    frames = []
    frame_start = 0
    while frame_start + frame_len <= totoal_dur:
        frames.append(data[frame_start:frame_start + frame_len])
        frame_start += frame_step

    return frames, samplerate


def load_file_as_frames(filename, delay=0, frame_size=FRAME_DURATION):
    return load_frames(filename, delay, frame_size)


def load_file_as_signal(filename):
    return soundfile.read(path.join(audiopath, filename))


def save_file(filename, data, samplerate):
    soundfile.write(path.join(audiopath, filename), data, samplerate)
