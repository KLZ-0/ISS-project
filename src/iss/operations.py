from iss import plotter

import numpy as np


def center_clip_frame(frame):
    cliplim = max(frame.min(), frame.max(), key=abs)
    return np.asarray([1 if sample > 0.7*cliplim else -1 if sample < -0.7*cliplim else 0 for sample in frame])
