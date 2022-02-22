import collections
from numpy.random import choice
# import matplotlib.pyplot as plt
import numpy as np

from wordle import Wordle
from Data.data import get_answers, get_allowed_guesses
from helpers import get_remaining_words_guess_known

get_word_list = lambda: np.concatenate((get_answers(), get_allowed_guesses()))
initial_word_list = get_word_list()
# print(word_list.shape)
# print(f"i: {i}")
random_answer = choice(initial_word_list)
# print(f"random_answer: {random_answer}")
w = Wordle(random_answer)


# print(w.answer)

def simulate(start_word=None, epochs=100):
    wins = 0
    win_percents = []
    guesses = []
    action_space_size = {i: 0 for i in range(1, 7)}

    for i in range(epochs):
        word_list = initial_word_list.copy()
        while not w.is_game_over:
            if start_word and w.attempt_number == 0:
                random_guess = start_word
            else:
                random_guess = choice(word_list)
            # print(random_guess)
            _, guess_state, _ = w.guess_word(random_guess)
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
