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
letter_frequencies = pickle.load(open("letter_frequencies.pkl ", "rb"))


def letter_sum(word: str):
    count = 0
    for letter in word:
        count += letter_frequencies[letter]
    return count


def max_letter_frequency(word_list: List[str]):
    return max(word_list, key=lambda x: letter_sum(set(x)))


def simulate(start_word=None, epochs=100):
    wins = 0
    win_percents = []
    guesses = []
    action_space_size = {i: 0 for i in range(1, 7)}

    for i in range(epochs):
        word_list = initial_word_list.copy()
        while not w.is_game_over:
            if start_word and w.attempt_number == 0:
                guess = start_word
            else:
                guess = max_letter_frequency(word_list)
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
