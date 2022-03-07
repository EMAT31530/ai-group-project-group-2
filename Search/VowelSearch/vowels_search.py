# import matplotlib.pyplot as plt
import pickle
from typing import List

import numpy as np
from numpy.random import choice

from Data.data import get_all_words
from helpers import get_remaining_words_guess_known
from wordle import Wordle

initial_word_list = get_all_words()
random_answer = choice(initial_word_list)
w = Wordle(random_answer)
vowel_frequencies = pickle.load(open("vowel_frequencies.pkl", "rb"))


def max_vowels(word_list: List[str], random=False):
    word_list_vowel_frequencies = {k: vowel_frequencies[k]
                                   for k in vowel_frequencies.keys()
                                   if k in word_list}
    maximum = max(word_list_vowel_frequencies.values())
    maxes = [x for x in word_list_vowel_frequencies.keys()
             if vowel_frequencies[x] == maximum]
    if random:
        return choice(maxes)
    else:
        return Exception("Not implemented")


def simulate(start_word=None, epochs=100):
    wins = 0
    win_percents = []
    guesses = []
    action_space_size = {i: 0 for i in range(1, 7)}

    start_word = max_vowels(initial_word_list, random=True)
    for i in range(epochs):
        word_list = initial_word_list.copy()
        while not w.is_game_over:
            if start_word and w.attempt_number == 0:
                guess = start_word
            else:
                guess = max_vowels(word_list, random=True)
            # print(random_guess)
            _, guess_state, _ = w.guess_word(guess)
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
