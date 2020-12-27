import numpy as np

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
        the_chosen_one = self.on_frames[0]
        plotter.plot(the_chosen_one, "frame.pdf",
                     figsize=(16, 3),
                     title="Frame",
                     xlabel="Time [ms]")

        wf = operations.center_clip_frame(the_chosen_one)
        plotter.plot(wf, "frame_clipped.pdf",
                     figsize=(16, 3),
                     title="70% Center clipping",
                     xlabel="Samples")

        wf = operations.autocorrelate_frame(wf, 0)
        plotter.plot(wf, "frame_autocorrelated.pdf",
                     figsize=(16, 3),
                     title="Autocorrelation",
                     xlabel="Samples")

        freqs_off = operations.frames_to_base_frequency(self.off_frames, self.off_sr)
        freqs_on = operations.frames_to_base_frequency(self.on_frames, self.on_sr)
        plotter.plot_list([freqs_off, freqs_on], "base_frequencies.pdf",
                          figsize=(16, 3),
                          title="Frame base frequencies",
                          xlabel="Frames",
                          ylabel="$f0$ [Hz]",
                          plot_labels=["Mask off", "Mask on"])

        print("OFF", "\n- Mean:\t\t", np.mean(freqs_off), "\n- Variance:\t", np.var(freqs_off))
        print("ON", "\n- Mean:\t\t", np.mean(freqs_on), "\n- Variance:\t", np.var(freqs_on))
