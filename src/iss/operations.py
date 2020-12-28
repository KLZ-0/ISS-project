import numpy as np
from numpy.fft import fft, ifft
from scipy.signal import lfilter

from iss.res import CORREL_FREQ_MARGIN


def center_clip_frame(frame):
    cliplim = abs(max(frame.min(), frame.max(), key=abs))
    return np.asarray([1 if sample > 0.7 * cliplim else -1 if sample < -0.7 * cliplim else 0 for sample in frame])


def autocorrelate_frame(frame, correl_margin):
    rs = []

    for k in range(int(correl_margin), len(frame)):
        f1 = frame[k:]
        f2 = frame[:len(frame) - k]

        rs.append(f1.dot(f2))

    return np.asarray(rs)


def frames_to_base_frequency(frames, samplerate):
    freqs = []
    corr_margin = samplerate / CORREL_FREQ_MARGIN

    for frame in frames:
        wf = center_clip_frame(frame)
        lag = np.argmax(autocorrelate_frame(wf, corr_margin)) + corr_margin
        freqs.append(samplerate / lag)

    return np.asarray(freqs)


def fft_spectrum(frames):
    return fft(frames, 1024)[:, :512]


def logarithmize_spectrum(fft_frames):
    return 10 * np.log10((np.abs(fft_frames) ** 2) + 1e-20)


def impulse_response(frequency_response):
    return np.abs(ifft(frequency_response))


def apply_filter(data, flt):
    return lfilter(a=[1], b=flt, x=data)
