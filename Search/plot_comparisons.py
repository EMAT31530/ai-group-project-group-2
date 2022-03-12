from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from Search.save_results import get_results


def plot_mean_guesses(data):
    for n in data.keys():
        plt.bar(n, sum(data[n][0]) / len(data[n][0]))
    plt.title("")
    plt.ylabel("Mean Guesses")
    plt.xlabel("Search Method")
    plt.show()
    plt.clf()


def plot_win_percentages(data):
    for n in data.keys():
        plt.plot([_ for _ in range(len(data[n][1]))], data[n][1],
                 label=str(n) + r" ($\bar{g}$ = " + str(round(np.mean(data[n][0]), 2))
                       + ")")
    plt.title("")
    plt.ylabel("Win Rate")
    plt.xlabel("Games Played")
    plt.legend(title="Search Metric")
    plt.show()
    plt.clf()


if __name__ == "__main__":
    results = {
        "Random": get_results("RandomSearch"),
        "Letter Frequency": get_results("LetterFrequency"),
        "Vowels Frequency": get_results("VowelSearch"),
        "Entropy": get_results("EntropySearch")
    }

    plt.style.use("seaborn-bright")
    plot_win_percentages(results)
    plot_mean_guesses(results)
