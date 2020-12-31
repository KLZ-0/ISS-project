import sys
from os import path

import numpy as np
from matplotlib import pyplot as plt

from iss.res import CORREL_FREQ_MARGIN, FIG_SIZE


def debug(data, filename="test.png"):
    time = np.linspace(0., len(data), data.shape[0])
    plt.figure(figsize=FIG_SIZE)
    plt.plot(time, data)

    plt.gca().set_xlabel('$t[ms]$')
    plt.gca().set_title('Signal')
    plt.tight_layout()

    plt.savefig(path.join("outputs", filename))


def plot(data, filename, figsize=FIG_SIZE, title="Title", xlabel="x", ylabel="y", plot_label=None,
         xspan=(0., -1.), correl_samplerate=0):
    if float(xspan[1]) != -1.:
        time = np.linspace(float(xspan[0]), float(xspan[1]), data.shape[0])
    else:
        time = np.linspace(float(xspan[0]), data.shape[0] - 1, data.shape[0])

    plt.figure(figsize=figsize)
    if plot_label:
        plt.plot(time, data, label=plot_label)
    else:
        plt.plot(time, data)

    # plt.gca().set_xticks([0, len(data)/4, len(data)/2, 3*len(data)/4, len(data)])
    # plt.gca().set_xticklabels()

    plt.gca().set_xlabel(xlabel)
    plt.gca().set_ylabel(ylabel)

    plt.gca().set_title(title)
    plt.tight_layout()

    if plot_label:
        plt.legend()

    if correl_samplerate != 0:
        cutoff = int(correl_samplerate / CORREL_FREQ_MARGIN)
        target_dt = data[cutoff:]
        plt.axvline(x=cutoff, color="black")
        plt.stem([target_dt.argmax() + cutoff], [target_dt.max()], linefmt="r")

    plt.savefig(path.join("outputs", filename))


def plot_list(datalist, filename, figsize=FIG_SIZE, title="Title", xlabel="x", ylabel="y", plot_labels=None,
              xspan=(0., -1.)):
    if plot_labels and len(plot_labels) != len(datalist):
        print("Data list size does not match label list size, wtf?", file=sys.stderr)
        return

    if float(xspan[1]) != -1.:
        time = np.linspace(float(xspan[0]), float(xspan[1]), datalist[0].shape[0])
    else:
        time = np.linspace(float(xspan[0]), datalist[0].shape[0] - 1, datalist[0].shape[0])

    plt.figure(figsize=figsize)
    for i in range(len(datalist)):
        if plot_labels:
            plt.plot(time, datalist[i], label=plot_labels[i])
        else:
            plt.plot(time, datalist[i])

    # plt.gca().set_xticks([0, len(data)/4, len(data)/2, 3*len(data)/4, len(data)])
    # plt.gca().set_xticklabels()

    plt.gca().set_xlabel(xlabel)
    plt.gca().set_ylabel(ylabel)

    plt.gca().set_title(title)
    plt.tight_layout()

    if plot_labels:
        plt.legend()

    plt.savefig(path.join("outputs", filename))


def img(data, filename, figsize=(8, 4), title="Title"):
    plt.figure(figsize=figsize)
    plt.imshow(data,
               aspect="auto",
               extent=[0, 1, 0, 8000],
               origin="lower")

    plt.gca().set_xlabel("Time [s]")
    plt.gca().set_ylabel("Frequency [Hz]")

    plt.gca().set_title(title)

    plt.colorbar(label="Spectral power density [dB]")

    plt.savefig(path.join("outputs", filename))


def flush():
    plt.close()
