import math
import os
import pickle
import time
from datetime import timedelta

import numpy as np
from timeit import default_timer as timer
from Data.data import get_all_words
from root import ROOT_DIR
from wordle import Wordle


def get_distribution(guess, answer):
    w = Wordle(answer)
    _, guess_state, _ = w.guess_word(guess)

    yellow_letters = "".join(guess_state[2]).replace(" ", "")
    green_letters = "".join(guess_state[1]).replace(" ", "")

    n_yellows = len(yellow_letters)
    n_greens = len(green_letters)
    n_greys = 5 - n_greens - n_yellows

    return n_greys, n_greens, n_yellows


def get_aggregate_distribution(word, word_list):
    dist = (0, 0, 0)

    for w in word_list:
        dist = tuple(map(sum, zip(dist, get_distribution(word, w))))

    return [d / sum(dist) for d in dist]


def calculate_entropy(dist):
    entropy = 0
    for x in dist:
        if x > 0:
            entropy -= x * math.log2(x)

    return entropy


def save_dictionary(file_name, dictionary):
    with open(file_name, 'wb') as f:
        return pickle.dump(dictionary, f)


def get_dictionary(file_name, word_list):
    print("Getting the dictionary")
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            print("Reading existing dictionary")
            return pickle.load(f)

    print("Creating dictionary for first time")
    #                 Computed, mean guesses, % wins
    entropy_dictionary = {word: (False, 0) for word in word_list}
    save_dictionary(file_name, entropy_dictionary)

    return entropy_dictionary


def filter_uncommon_letters(word_list):
    word_list = [w for w in word_list if "q" not in w]
    word_list = [w for w in word_list if "j" not in w]
    word_list = [w for w in word_list if "w" not in w]
    word_list = [w for w in word_list if "z" not in w]
    word_list = [w for w in word_list if "g" not in w]
    word_list = [w for w in word_list if "f" not in w]
    word_list = [w for w in word_list if "k" not in w]
    return word_list


if __name__ == "__main__":
    file_name = f"{ROOT_DIR}/Search/EntropySearch/entropy.pkl"
    print("Getting word list ... ")
    word_list = get_all_words()
    print("Got word list")

    print("Filtering Word List")
    word_list = filter_uncommon_letters(word_list)
    print(f"New List Length = {len(word_list)}")
    entropy_dict = get_dictionary(file_name, word_list)

    for word in entropy_dict.keys():
        if entropy_dict[word][0] is False:
            start = timer()
            print(f"Word: {word}")
            entropy = calculate_entropy(get_aggregate_distribution(word, word_list))
            entropy_dict[word] = (True, entropy)
            end = timer()
            print(f"Entropy = {entropy} ({print(timedelta(seconds=end-start))}s)\n")
            save_dictionary(file_name, entropy_dict)

    """entropies = pickle.load(open("entropy.pkl ", "rb"))

    entropies = dict(sorted(entropies.items(),
                            key=lambda item: item[1], reverse=True))


    for k, v in entropies.items():
        print(f"{k} | {v[1]}")"""

