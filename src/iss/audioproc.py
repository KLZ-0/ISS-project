import iss.input
from iss import plotter, operations


class AudioProcessor:
    off_sr = 0
    on_sr = 0
    off_frames = None
    on_frames = None

    def __init__(self):
        self.off_frames, self.off_sr = iss.input.load_file("maskoff_tone.wav")
        self.on_frames, self.on_sr = iss.input.load_file("maskon_tone.wav", 50)

    def process_signals(self):
        wf = operations.center_clip_frame(self.on_frames[0])
        plotter.plot(wf, "frame_clipped.pdf")
        wf = operations.autocorrelate_frame(wf, 0)
        plotter.plot(wf, "frame_autocorrelated.pdf")

        freqs1 = operations.frames_to_base_frequency(self.off_frames, self.off_sr)
        freqs2 = operations.frames_to_base_frequency(self.on_frames, self.on_sr)
        plotter.plot_list([freqs1, freqs2], "base_frequencies.pdf", figsize=(16, 4))
