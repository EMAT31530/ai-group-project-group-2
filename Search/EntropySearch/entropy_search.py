import collections
import pickle
from typing import List

from numpy.random import choice
# import matplotlib.pyplot as plt
import numpy as np

from Search.EntropySearch.calculate_entropy import filter_uncommon_letters
from wordle import Wordle
from Data.data import get_all_words
from helpers import get_remaining_words_guess_known

initial_word_list = filter_uncommon_letters(get_all_words())
random_answer = choice(initial_word_list)
w = Wordle(random_answer)

with open("entropy.pkl", "rb") as f:
    entropy = pickle.load(f)

full_entropy = {word: 0 for word in initial_word_list}

for word in entropy.keys():
    full_entropy[word] = entropy[word][1]

print(full_entropy)


def max_entropy_word(word_list: List[str]) -> str:
    return max(word_list, key=lambda x: full_entropy[x])


def simulate(start_word=None, epochs=100):
    wins = 0
    win_percents = []
    guesses = []
    action_space_size = {i: 0 for i in range(1, 7)}

    for i in range(epochs):
        word_list = initial_word_list.copy()
        while not w.is_game_over:
            if start_word and w.attempt_number == 0:
                max_entropy_guess = start_word
            else:
                max_entropy_guess = max_entropy_word(word_list)

            if w.attempt_number == 0:
                print(max_entropy_guess)

            _, guess_state, _ = w.guess_word(max_entropy_guess)
            word_list = get_remaining_words_guess_known(word_list, guess_state)
            action_space_size[w.attempt_number] += np.shape(word_list)[0]

        if w.won:
            # print(f"Attempt Number: {w.attempt_number}")
            # print(f"Winning guess: {random_guess}")
            # print("\n")
            wins += 1
            guesses.append(w.attempt_number)
        win_percents.append(wins / (i + 1))
        w.reset()

    return guesses, win_percents, action_space_size
