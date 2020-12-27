import numpy as np

CORRELATION_MARGIN = 30


def center_clip_frame(frame):
    cliplim = max(frame.min(), frame.max(), key=abs)
    return np.asarray([1.0 if sample > 0.7 * cliplim else -1.0 if sample < -0.7 * cliplim else 0.0 for sample in frame])


def autocorrelate_frame(frame):
    rs = []

    for k in range(0, 300):
        f1 = frame[k:]
        f2 = frame[:len(frame) - k]

        rs.append(np.sum(f1.dot(f2)))

    return np.asarray(rs)


def frames_to_base_frequency(frames, samplerate):
    freqs = []

    for frame in frames:
        lag = np.argmax(autocorrelate_frame(frame)[CORRELATION_MARGIN:]) + CORRELATION_MARGIN
        freqs.append(samplerate / lag)

    return np.asarray(freqs)
