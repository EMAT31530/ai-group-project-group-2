import string
import pickle
import sys
import itertools
import random
import numpy as np
import pandas as pd

from read_words import read_words
from read_words import read_answers
from scipy.stats import entropy
from os.path import exists
from functools import partial
from collections import defaultdict, Counter



def get_answers():

    answers = read_answers()
    #answers = read_words()
    
    return answers





def calculate_pattern(guess, true):

    wrong = [i for i, v in enumerate(guess) if v != true[i]]
    counts = Counter(true[i] for i in wrong)
    pattern = [2] * 5
    for i in wrong:
        v = guess[i]
        if counts[v] > 0:
            pattern[i] = 1
            counts[v] -= 1
        else:
            pattern[i] = 0
    return tuple(pattern)


def get_pattern_dict(possible_words):
    pattern_dict = defaultdict(lambda: defaultdict(set))
    #pattern_dict = {}
    for word in possible_words:
        for word2 in possible_words:
            pattern = calculate_pattern(word, word2)
            pattern_dict[word][pattern].add(word2)


    return dict(pattern_dict)





def calculate_entropies(possible_words, pattern_dict):
    """Calculate the entropy for every word in `words`, taking into account
    the remaining `possible_words`"""
    entropies = {}
    all_patterns = list(itertools.product([0, 1, 2], repeat=5))
    for word in possible_words:
        counts = []
        for pattern in all_patterns:
            matches = pattern_dict[word][pattern]
            matches = matches.intersection(possible_words)
            counts.append(len(matches))
        entropies[word] = entropy(counts)
    return entropies


if __name__ == '__main__':

    answers = get_answers()

    p_dict = get_pattern_dict(answers)
    
    entrop = calculate_entropies(answers, p_dict)

    best_words = sorted(entrop, key=entrop.get, reverse=True)[:40]

    entrop_value = []

    for word in best_words:
        
        entrop_value.append(entrop[word])

        #print('We suggest {} to be the next guess, it has an entropy of :  {}'.format(fin_max, entrop_value))

    optimal = dict(zip(best_words, entrop_value))
    
    print(optimal)
