import sys

import numpy as np
from numpy.fft import fft, ifft, fftshift
from scipy.signal import lfilter, get_window

from iss.res import CORREL_FREQ_MARGIN, ALIGN_MIN_FREQ, ALIGNED_FRAME_DURATION


def center_clip_frame(frame):
    cliplim = abs(max(frame.min(), frame.max(), key=abs))
    return np.asarray([1 if sample > 0.7 * cliplim else -1 if sample < -0.7 * cliplim else 0 for sample in frame])


def correlate_frame(frame1, frame2, min_margin=0, max_margin=-1):
    if len(frame1) != len(frame2):
        print("Frame lenghts don't match, wtf?", file=sys.stderr)
        sys.exit(1)

    if max_margin == -1:
        max_margin = len(frame1)

    rs = []

    for k in range(int(min_margin), max_margin):
        f1 = frame1[k:]
        f2 = frame2[:len(frame1) - k]

        rs.append(f1.dot(f2))

    return np.asarray(rs)


def frames_to_base_frequency(frames, samplerate):
    freqs = []
    corr_margin = samplerate / CORREL_FREQ_MARGIN

    for frame in frames:
        wf = center_clip_frame(frame)
        lag = np.argmax(correlate_frame(wf, wf, corr_margin)) + corr_margin
        freqs.append(samplerate / lag)

    return np.asarray(freqs)


def fft_spectrum_list(frames):
    return fft(frames, 1024)[:, :512]


def fft_spectrum(frames):
    return fft(frames, 1024)[:512]


def logarithmize_spectrum(fft_frames):
    return 10 * np.log10((np.abs(fft_frames) ** 2) + 1e-20)


def impulse_response(frequency_response):
    return ifft(frequency_response, n=512)[:256]


def apply_filter(data, flt):
    return lfilter(a=[1], b=flt.real, x=data)


def overlap_add(data, flt):
    # L is chosen such that N = L+M-1 is an integer power-of-2
    N = 2 << (flt.shape[0] - 1).bit_length()
    step = N - flt.shape[0] + 1
    samples = data.shape[0]

    flt_fft = fft(flt, n=N)

    filtered_data = np.zeros(samples + N)
    for n in range(0, samples, step):
        filtered_data[n:n + N] += ifft(
            fft(data[n:n + step], n=N) * flt_fft
        ).real

    return filtered_data[:samples]


def align_frames(frames1, frames2, samplerate, min_corr_margin=3):
    max_margin = int(samplerate / (ALIGN_MIN_FREQ * 2))
    target_frame_size = int(samplerate * ALIGNED_FRAME_DURATION)

    shifts = []

    for frame_n in range(len(frames1)):
        f_off = center_clip_frame(frames1[frame_n])
        f_on = center_clip_frame(frames2[frame_n])

        dt1 = np.argmax(correlate_frame(f_off, f_on, min_margin=min_corr_margin, max_margin=max_margin))
        dt2 = np.argmax(correlate_frame(f_on, f_off, min_margin=min_corr_margin, max_margin=max_margin))
        delta = min(dt1, dt2) + min_corr_margin

        if dt1 < dt2:
            frames1[frame_n] = frames1[frame_n][delta:]
            frames2[frame_n] = frames2[frame_n][:len(frames2[frame_n]) - delta]
        else:
            frames2[frame_n] = frames2[frame_n][delta:]
            frames1[frame_n] = frames1[frame_n][:len(frames1[frame_n]) - delta]

        frames2[frame_n] = frames2[frame_n][:target_frame_size]
        frames1[frame_n] = frames1[frame_n][:target_frame_size]

        shifts.append(delta if dt1 < dt2 else -delta)

    return np.asarray(shifts)


def window_frames(frames):
    window = get_window("hann", frames[0].shape[-1])
    fft_res = fft(window, 1024) / (len(window) / 2.0)
    response = np.abs(fftshift(fft_res / abs(fft_res).max()))

    return [frame * window for frame in frames], window, response
