from os import path

import numpy as np
from matplotlib import pyplot as plt


def debug(data):
    time = np.linspace(0., len(data), data.shape[0])
    plt.figure(figsize=(8, 4))
    plt.plot(time, data)

    plt.gca().set_xlabel('$t[ms]$')
    plt.gca().set_title('Signal')
    plt.tight_layout()

    plt.savefig(path.join("outputs", "test.pdf"))


def plot(data, filename, tick_start=0, tick_end=20):
    time = np.linspace(0., len(data), data.shape[0])
    # time = np.arange(0, len(data), 1)
    plt.figure(figsize=(8, 4))
    plt.plot(time, data)

    # plt.gca().set_xticks([0, len(data)/4, len(data)/2, 3*len(data)/4, len(data)])
    # plt.gca().set_xticklabels()

    plt.gca().set_xlabel('$t[ms]$')
    plt.gca().set_title('Signal')
    plt.tight_layout()

    plt.savefig(path.join("outputs", filename))


def plot_list(datalist, filename, tick_start=0, tick_end=20):
    time = np.linspace(0., len(datalist[0]), datalist[0].shape[0])
    # time = np.arange(0, len(data), 1)
    plt.figure(figsize=(8, 4))
    for data in datalist:
        plt.plot(time, data)

    # plt.gca().set_xticks([0, len(data)/4, len(data)/2, 3*len(data)/4, len(data)])
    # plt.gca().set_xticklabels()

    plt.gca().set_xlabel('$t[ms]$')
    plt.gca().set_title('Signal')
    plt.tight_layout()

    plt.savefig(path.join("outputs", filename))
