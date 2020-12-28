import numpy as np

import iss.input
from iss import plotter, operations


class AudioProcessor:
    # set in __init__
    off_sr = 0
    on_sr = 0
    off_frames = None
    on_frames = None

    # set in task5
    fft_on = None
    fft_off = None

    # set in task 6
    freq_response = None

    # set in task 7
    impulse_response = None

    def __init__(self):
        # task 1, 2, 3
        self.off_frames, self.off_sr = iss.input.load_file("maskoff_tone.wav")
        self.on_frames, self.on_sr = iss.input.load_file("maskon_tone.wav", 50)

    def process_signals(self):
        self.task3()
        self.task4()
        self.task5()
        self.task6()
        self.task7()

    def task3(self):
        plotter.plot_list([self.off_frames[0], self.on_frames[0]], "3_frames.pdf",
                          title="Frame",
                          xlabel="Time [ms]",
                          plot_labels=["Mask off", "Mask on"])

    def task4(self):
        the_chosen_one = self.on_frames[0]
        plotter.plot(the_chosen_one, "4_frame.pdf",
                     figsize=(16, 3),
                     title="Frame",
                     xlabel="Time [ms]")

        wf = operations.center_clip_frame(the_chosen_one)
        plotter.plot(wf, "4_frame_clipped.pdf",
                     figsize=(16, 3),
                     title="70% Center clipping",
                     xlabel="Samples")

        wf = operations.autocorrelate_frame(wf, 0)
        plotter.plot(wf, "4_frame_autocorrelated.pdf",
                     figsize=(16, 3),
                     title="Autocorrelation",
                     xlabel="Samples",
                     correl_samplerate=self.on_sr)

        freqs_off = operations.frames_to_base_frequency(self.off_frames, self.off_sr)
        freqs_on = operations.frames_to_base_frequency(self.on_frames, self.on_sr)
        plotter.plot_list([freqs_off, freqs_on], "4_base_frequencies.pdf",
                          figsize=(16, 3),
                          title="Frame base frequencies",
                          xlabel="Frames",
                          ylabel="$f0$ [Hz]",
                          plot_labels=["Mask off", "Mask on"])

        print("4 OFF", "\n- Mean:\t\t", np.mean(freqs_off), "\n- Variance:\t", np.var(freqs_off))
        print("4 ON", "\n- Mean:\t\t", np.mean(freqs_on), "\n- Variance:\t", np.var(freqs_on))

    def task5(self):
        self.fft_off = operations.fft_spectrum(self.off_frames)
        plotter.img(operations.logarithmize_spectrum(self.fft_off).T, "5_spectrum_maskoff.pdf",
                    title="Spectrogram - mask off")

        self.fft_on = operations.fft_spectrum(self.on_frames)
        plotter.img(operations.logarithmize_spectrum(self.fft_on).T, "5_spectrum_maskon.pdf",
                    title="Spectrogram - mask on")

    def task6(self):
        freq_characteristic_frames = self.fft_on / self.fft_off
        # use one of these
        self.freq_response = np.mean(freq_characteristic_frames, axis=0)
        plotter.plot(operations.logarithmize_spectrum(self.freq_response), "6_frequency_response.pdf",
                     figsize=(16, 3),
                     title="Frequency response",
                     xlabel="Frequency [Hz]",
                     ylabel="Gain [dB]")

    def task7(self):
        self.impulse_response = operations.impulse_response(self.freq_response)
        plotter.plot(self.impulse_response, "7_impulse_response.pdf",
                     figsize=(16, 3),
                     title="Impulse response",
                     xlabel="Time [s]",
                     ylabel="Amplitude")
