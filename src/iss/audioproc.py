import iss.input
from iss import plotter, operations

from os import path


class AudioProcessor:
    off_frames = None
    on_frames = None

    def __init__(self):
        self.off_frames = iss.input.load_file("maskoff_tone.wav")
        self.on_frames = iss.input.load_file("maskon_tone.wav")

    def process_signals(self):
        pass
