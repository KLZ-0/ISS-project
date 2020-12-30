import sys

import numpy as np

import iss.io
from iss import plotter, operations


class AudioProcessor:
    first_run = True

    # set in task5
    fft_on = None
    fft_off = None

    # set in task 6
    freq_response = None

    # set in task 7
    impulse_response = None

    def __init__(self):
        # task 1, 2, 3
        self.off_frames, self.off_sr = iss.io.load_file_as_frames("maskoff_tone.wav")
        self.on_frames, self.on_sr = iss.io.load_file_as_frames("maskon_tone.wav")

        self.off_tone, self.off_tone_sr = iss.io.load_file_as_signal("maskoff_tone.wav")
        self.off_sentence, self.off_sentence_sr = iss.io.load_file_as_signal("maskoff_sentence.wav")
        self.on_sentence, self.on_sentence_sr = iss.io.load_file_as_signal("maskon_sentence.wav")

    def process_signals(self):
        self.task3()
        self.task4()
        self.task5()
        self.task6()
        self.task7()
        self.task8()

        self.first_run = False

        self.task15()
        self.task5()
        self.task6()
        self.task7()
        self.task15b()

    def task3(self):
        if self.first_run:
            plotter.plot_list([self.off_frames[0], self.on_frames[0]], "3_frames.pdf",
                              title="Frame",
                              xlabel="Time [ms]",
                              plot_labels=["Mask off", "Mask on"])

    def task4(self):
        the_chosen_one = self.on_frames[0]
        if self.first_run:
            plotter.plot(the_chosen_one, "4_frame.pdf",
                         title="Frame",
                         xlabel="Time [ms]")

        wf = operations.center_clip_frame(the_chosen_one)
        if self.first_run:
            plotter.plot(wf, "4_frame_clipped.pdf",
                         title="70% Center clipping",
                         xlabel="Samples")

        wf = operations.correlate_frame(wf, wf, 0)
        if self.first_run:
            plotter.plot(wf, "4_frame_autocorrelated.pdf",
                         title="Autocorrelation",
                         xlabel="Samples",
                         correl_samplerate=self.on_sr)

        freqs_off = operations.frames_to_base_frequency(self.off_frames, self.off_sr)
        freqs_on = operations.frames_to_base_frequency(self.on_frames, self.on_sr)
        if self.first_run:
            plotter.plot_list([freqs_off, freqs_on], "4_base_frequencies.pdf",
                              title="Base frequency per frame",
                              xlabel="Frames",
                              ylabel="$f0$ [Hz]",
                              plot_labels=["Mask off", "Mask on"])

        print("4 OFF", "\n- Mean:\t\t", np.mean(freqs_off), "\n- Variance:\t", np.var(freqs_off))
        print("4 ON", "\n- Mean:\t\t", np.mean(freqs_on), "\n- Variance:\t", np.var(freqs_on))

    def task5(self):
        self.fft_off = operations.fft_spectrum(self.off_frames)
        if self.first_run:
            plotter.img(operations.logarithmize_spectrum(self.fft_off).T, "5_spectrum_maskoff.pdf",
                        title="Spectrogram - mask off")

        self.fft_on = operations.fft_spectrum(self.on_frames)
        if self.first_run:
            plotter.img(operations.logarithmize_spectrum(self.fft_on).T, "5_spectrum_maskon.pdf",
                        title="Spectrogram - mask on")

    def task6(self):
        # t_on = np.mean(np.abs(self.fft_on), axis=0)
        # t_off = np.mean(np.abs(self.fft_off), axis=0)
        # self.freq_response = t_on / (t_off + 1e-20)

        t = abs(self.fft_on / self.fft_off)
        self.freq_response = np.mean(t, axis=0)

        if self.first_run:
            plotter.plot(operations.logarithmize_spectrum(self.freq_response), "6_frequency_response.pdf",
                         title="Frequency response",
                         xlabel="Frequency [Hz]",
                         ylabel="Gain [dB]")

    def task7(self):
        self.impulse_response = operations.impulse_response(self.freq_response)
        if self.first_run:
            plotter.plot(np.abs(self.impulse_response), "7_impulse_response.pdf",
                         title="Impulse response",
                         xlabel="Time [s]",
                         ylabel="Amplitude")

    def task8(self):
        plotter.plot(self.off_sentence, "8_signal_maskoff.pdf",
                     title="Original signal (maskoff)",
                     xlabel="Time [s]")

        plotter.plot(self.on_sentence, "8_signal_maskon.pdf",
                     title="Target signal (maskon)",
                     xlabel="Time [s]")

        dt = operations.apply_filter(self.off_sentence, self.impulse_response)
        plotter.plot(dt, "8_signal_filtered.pdf",
                     title="Filtered signal (maskoff + filter)",
                     xlabel="Time [s]")
        iss.io.save_file("sim_maskon_sentence.wav", dt, self.off_sentence_sr)

        dt = operations.apply_filter(self.off_tone, self.impulse_response)
        iss.io.save_file("sim_maskon_tone.wav", dt, self.off_tone_sr)

        # ft = operations.apply_filter(self.off_frames[0], np.abs(self.impulse_response))

        # from numpy.fft import fft
        # plotter.plot_list([abs(fft(self.off_frames[0], 1024)[:512]),
        #                    abs(fft(self.on_frames[0], 1024)[:512]),
        #                    abs(fft(ft, 1024)[:512])
        #                    ],
        #                   "debug.pdf", plot_labels=["original", "target", "filtered"])

        # plotter.plot_list([self.off_frames[0],
        #                    self.on_frames[0],
        #                    ft
        #                    ],
        #                   "debug.pdf", plot_labels=["original", "target", "filtered"])

    def task15(self):
        """
        NOTE: This function modifies already set class variables
        """
        plotter.plot_list([self.off_frames[0], self.on_frames[0]], "15_frames_before.pdf",
                          title="Frame before alignment",
                          xlabel="Time [ms]",
                          plot_labels=["Mask off", "Mask on"])

        if self.off_sr != self.on_sr:
            print("Samplerates don't match, wtf?", file=sys.stderr)
            sys.exit(1)

        dt = operations.align_frames(self.off_frames, self.on_frames, samplerate=self.off_sr)

        plotter.plot_list([self.off_frames[0], self.on_frames[0]], "15_frames_after.pdf",
                          title="Frame after alignment",
                          xlabel="Time [ms]",
                          plot_labels=["Mask off", "Mask on"])

        plotter.plot(dt, "15_shifts.pdf",
                     title="Phase shift per frame",
                     xlabel="Frames",
                     ylabel="Shift [samples]")

    def task15b(self):
        dt = operations.apply_filter(self.off_sentence, self.impulse_response)
        plotter.plot(dt, "15_signal_filtered.pdf",
                     title="Filtered signal (maskoff + phase shift + filter)",
                     xlabel="Time [s]")
        iss.io.save_file("sim_maskon_sentence_phase.wav", dt, self.off_sentence_sr)

        dt = operations.apply_filter(self.off_tone, self.impulse_response)
        iss.io.save_file("sim_maskon_tone_phase.wav", dt, self.off_tone_sr)
