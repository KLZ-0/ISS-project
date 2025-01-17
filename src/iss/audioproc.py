import sys

import numpy as np

import iss.io
from iss import plotter, operations
from iss.res import ALIGNED_FRAME_DURATION


# Post-submission note:
# This was implemented in a tight time constraint and the code should be optimized and reformatted
# but because this code was already submitted I am not going to do so...
#
# e.g. the plotting should have been separated from the task methods
# -> some the tasks need to be run multiple times (this would eliminate the need for "run_n")
class AudioProcessor:
    run_n = 0

    # set in task 4
    # used in task 11
    valid_frames = {"off": [], "on": []}

    # set in task5
    fft_on = None
    fft_off = None

    # set in task 6
    freq_response = None

    # set in task 7
    impulse_response = None

    def __init__(self):
        # task 1, 2, 3
        self.off_frames, self.off_sr = iss.io.load_file_as_frames("maskoff_tone.wav", frame_size=ALIGNED_FRAME_DURATION)
        self.on_frames, self.on_sr = iss.io.load_file_as_frames("maskon_tone.wav", frame_size=ALIGNED_FRAME_DURATION)

        self.off_tone, self.off_tone_sr = iss.io.load_file_as_signal("maskoff_tone.wav")
        self.off_sentence, self.off_sentence_sr = iss.io.load_file_as_signal("maskoff_sentence.wav")
        self.on_sentence, self.on_sentence_sr = iss.io.load_file_as_signal("maskon_sentence.wav")

    def reload_frames(self):
        self.off_frames, self.off_sr = iss.io.load_file_as_frames("maskoff_tone.wav")
        self.on_frames, self.on_sr = iss.io.load_file_as_frames("maskon_tone.wav", delay=20)

    def process_signals(self):
        # base tasks
        self.task3()
        self.task4()
        self.task5()
        self.task6()
        self.task7()
        plotter.flush()
        self.task8()
        self.task10()
        plotter.flush()

        # task 13
        self.run_n = 3
        self.task13()
        self.task6()
        self.task7()
        self.task13b()

        # reload the original frames, but with different frame size
        self.reload_frames()

        # task 15 - phase shift
        self.run_n = 1
        self.task15()
        self.task5()
        self.task6()
        self.task7()
        self.task15b()
        plotter.flush()

        # reload the original frames
        self.reload_frames()

        # task 11 - window function + also shifted because it looks better
        self.run_n = 2
        self.task15()
        self.task11()
        self.task5()
        self.task6()
        self.task7()
        self.task11b()
        plotter.flush()

    def task3(self):
        if self.run_n == 0:
            plotter.plot_list([self.off_frames[0], self.on_frames[0]], "3_frames.pdf",
                              title="Frame",
                              xlabel="Time [s]",
                              xspan=(0, ALIGNED_FRAME_DURATION),
                              plot_labels=["Mask off", "Mask on"])

    def task4(self):
        the_chosen_one = self.on_frames[0]
        if self.run_n == 0:
            plotter.plot(the_chosen_one, "4_frame.pdf",
                         title="Frame",
                         xlabel="Time [s]",
                         xspan=(0, ALIGNED_FRAME_DURATION))

        wf = operations.center_clip_frame(the_chosen_one)
        if self.run_n == 0:
            plotter.plot(wf, "4_frame_clipped.pdf",
                         title="70% Center clipping",
                         xlabel="Samples")

        wf = operations.correlate_frame(wf, wf, 0)
        if self.run_n == 0:
            plotter.plot(wf, "4_frame_autocorrelated.pdf",
                         title="Autocorrelation",
                         xlabel="Samples",
                         correl_samplerate=self.on_sr)

        freqs_off = operations.frames_to_base_frequency(self.off_frames, self.off_sr)
        freqs_on = operations.frames_to_base_frequency(self.on_frames, self.on_sr)
        if self.run_n == 0:
            plotter.plot_list([freqs_off, freqs_on], "4_base_frequencies.pdf",
                              title="Base frequency per frame",
                              xlabel="Frames",
                              ylabel="$f0$ [Hz]",
                              plot_labels=["Mask off", "Mask on"])

        for i in range(len(self.off_frames)):
            if freqs_off[i] == freqs_on[i]:
                self.valid_frames["off"].append(self.off_frames[i])
                self.valid_frames["on"].append(self.on_frames[i])

        print("4 OFF", "\n- Mean:\t\t", np.mean(freqs_off), "\n- Variance:\t", np.var(freqs_off))
        print("4 ON", "\n- Mean:\t\t", np.mean(freqs_on), "\n- Variance:\t", np.var(freqs_on))

    def task5(self):
        self.fft_off = operations.fft_spectrum_list(self.off_frames)
        if self.run_n == 0:
            plotter.img(operations.logarithmize_spectrum(self.fft_off).T, "5_spectrum_maskoff.pdf",
                        title="Spectrogram - mask off")

        self.fft_on = operations.fft_spectrum_list(self.on_frames)
        if self.run_n == 0:
            plotter.img(operations.logarithmize_spectrum(self.fft_on).T, "5_spectrum_maskon.pdf",
                        title="Spectrogram - mask on")

    def task6(self):
        t_on = np.mean(np.abs(self.fft_on), axis=0)
        t_off = np.mean(np.abs(self.fft_off), axis=0)
        self.freq_response = t_on / (t_off + 1e-20)

        if self.run_n == 0:
            plotter.plot(operations.logarithmize_spectrum(self.freq_response), "6_frequency_response.pdf",
                         title="Mask frequency response",
                         xlabel="Frequency [Hz]",
                         ylabel="Gain [dB]",
                         xspan=(0, self.off_sr / 2))

    def task7(self):
        self.impulse_response = operations.impulse_response(self.freq_response)
        if self.run_n == 0:
            plotter.plot(self.impulse_response.real, "7_impulse_response.pdf",
                         title="Mask impulse response",
                         xlabel="Time [s]",
                         xspan=(0, ALIGNED_FRAME_DURATION))

    def task8(self):
        plotter.plot(self.off_sentence, "8_signal_maskoff.pdf",
                     title="Original signal (maskoff)",
                     xlabel="Time [s]",
                     xspan=(0, self.off_sentence.shape[0] / self.off_sentence_sr))

        plotter.plot(self.on_sentence, "8_signal_maskon.pdf",
                     title="Target signal (maskon)",
                     xlabel="Time [s]",
                     xspan=(0, self.on_sentence.shape[0] / self.on_sentence_sr))

        dt = operations.apply_filter(self.off_sentence, self.impulse_response)
        plotter.plot(dt, "8_signal_filtered.pdf",
                     title="Filtered signal (maskoff + filter)",
                     xlabel="Time [s]",
                     xspan=(0, dt.shape[0] / self.off_sentence_sr))
        iss.io.save_file("sim_maskon_sentence.wav", dt, self.off_sentence_sr)

        dt = operations.apply_filter(self.off_tone, self.impulse_response)
        iss.io.save_file("sim_maskon_tone.wav", dt, self.off_tone_sr)

    def task10(self):
        dt = operations.overlap_add(self.off_sentence, self.impulse_response)
        iss.io.save_file("sim_maskon_sentence_overlap_add.wav", dt, self.off_sentence_sr)
        plotter.plot(dt, "10_signal_filtered.pdf",
                     title="Filtered signal - overlap-add (maskoff + filter)",
                     xlabel="Time [s]",
                     xspan=(0, dt.shape[0] / self.off_sentence_sr))

        dt = operations.overlap_add(self.off_tone, self.impulse_response)
        iss.io.save_file("sim_maskon_tone_overlap_add.wav", dt, self.off_tone_sr)

    def task11(self):
        plotter.flush()
        plotter.plot_list([self.off_frames[0], self.on_frames[0]], "11_frames_before.pdf",
                          title="Frames before an applied window function",
                          xlabel="Samples",
                          plot_labels=["Mask off", "Mask on"])

        plotter.plot(np.abs(operations.fft_spectrum(self.on_frames[0])),
                     "11_frame_spectrum_before.pdf",
                     title="Frequency domain before an applied window function",
                     xlabel="Frequency [Hz]",
                     xspan=(0, self.off_sr / 2))

        self.off_frames, window, response = operations.window_frames(self.off_frames)
        self.on_frames, _, _ = operations.window_frames(self.on_frames)
        plotter.plot(window, "11_window.pdf",
                     title="Window time domain",
                     xlabel="Sample",
                     ylabel="Amplitude",
                     xspan=(0, ALIGNED_FRAME_DURATION))

        plotter.plot(operations.logarithmize_spectrum(response), "11_response.pdf",
                     title="Window frequency domain",
                     xlabel="Normalized frequency",
                     ylabel="Magnitude [dB]",
                     xspan=(-0.5, 0.5))

        plotter.plot_list([self.off_frames[0], self.on_frames[0]], "11_frames_after.pdf",
                          title="Frames after an applied window function",
                          xlabel="Samples",
                          plot_labels=["Mask off", "Mask on"])

        plotter.plot(np.abs(operations.fft_spectrum(self.on_frames[0])),
                     "11_frame_spectrum_after.pdf",
                     title="Frequency domain after an applied window function",
                     xlabel="Frequency [Hz]",
                     xspan=(0, self.off_sr / 2))
        plotter.flush()

    def task11b(self):
        dt = operations.apply_filter(self.off_sentence, self.impulse_response)
        iss.io.save_file("sim_maskon_sentence_window.wav", dt, self.off_sentence_sr)

        dt = operations.apply_filter(self.off_tone, self.impulse_response)
        iss.io.save_file("sim_maskon_tone_window.wav", dt, self.off_tone_sr)

    def task13(self):
        if len(self.valid_frames["off"]):
            self.fft_off = operations.fft_spectrum_list(self.valid_frames["off"])
            self.fft_on = operations.fft_spectrum_list(self.valid_frames["on"])
        else:
            # if no suitable frames found, continue with 5
            self.task5()

    def task13b(self):
        plotter.plot(operations.logarithmize_spectrum(self.freq_response), "13_frequency_response.pdf",
                     title="Mask Frequency response (only from matching frames)",
                     xlabel="Frequency [Hz]",
                     ylabel="Gain [dB]",
                     xspan=(0, self.off_sr / 2))

        dt = operations.apply_filter(self.off_sentence, self.impulse_response)
        iss.io.save_file("sim_maskon_sentence_only_match.wav", dt, self.off_sentence_sr)

        dt = operations.apply_filter(self.off_tone, self.impulse_response)
        iss.io.save_file("sim_maskon_tone_only_match.wav", dt, self.off_tone_sr)

    def task15(self):
        """
        NOTE: This function modifies already set class variables
        """

        if self.run_n == 1:
            plotter.plot_list([self.off_frames[0], self.on_frames[0]], "15_frames_before.pdf",
                              title="Frames before alignment",
                              xlabel="Time [ms]",
                              plot_labels=["Mask off", "Mask on"])

        if self.off_sr != self.on_sr:
            print("Samplerates don't match, wtf?", file=sys.stderr)
            sys.exit(1)

        dt = operations.align_frames(self.off_frames, self.on_frames, samplerate=self.off_sr)

        if self.run_n == 1:
            plotter.plot_list([self.off_frames[0], self.on_frames[0]], "15_frames_after.pdf",
                              title="Frames after alignment",
                              xlabel="Time [ms]",
                              plot_labels=["Mask off", "Mask on"])

        if self.run_n == 1:
            plotter.plot(dt, "15_shifts.pdf",
                         title="Phase shift per frame",
                         xlabel="Frames",
                         ylabel="Phase shift [samples]")

    def task15b(self):
        dt = operations.apply_filter(self.off_sentence, self.impulse_response)
        iss.io.save_file("sim_maskon_sentence_phase.wav", dt, self.off_sentence_sr)

        dt = operations.apply_filter(self.off_tone, self.impulse_response)
        iss.io.save_file("sim_maskon_tone_phase.wav", dt, self.off_tone_sr)
