import string
import pickle
import sys
import itertools

from read_words import read_words
from scipy.stats import entropy
from os.path import exists
from functools import partial
from collections import defaultdict, Counter




def word_list():

    five_letter_words = read_words()

    possible_letters = list('abcdefghijklmnopqrstuvwxyz')
    
    return five_letter_words, possible_letters




def filter_guessed_letters(constraints_string):
    if len(constraints_string) == 0:
        return []
    wordle = list("_____")
    letter_in_wrong_pos = []
    no_letter = []
    
    for i in range(0, len(constraints_string), 2):
        count = 0
        if constraints_string[i+1] == '2':
            letter_in_wrong_pos.append(constraints_string[i])
        if constraints_string[i+1] == '3':
            no_letter.append(constraints_string[i])
        if constraints_string[i+1] == '1':
            wordle[int(i/2)] = constraints_string[i]
        count = count + 1
        
    print(wordle)

    return wordle, letter_in_wrong_pos, no_letter


def grey_letter(possible_words, grey_letters):
    
    for char in grey_letters:
        for word in possible_words:
            if char in word:
                possible_words.remove(word)


    return possible_words


def yellow_letter(possible_words, yellow_letters):
    yellows = len(yellow_letters) - 1
    dup_list = []
    for char in yellow_letters:
        for word in possible_words:
            if char in word:
                dup_list.append(word)

    dup = {x for x in dup_list if dup_list.count(x) > yellows}

    possible_words = dup
                
    return possible_words




def green_letter(possible_words, guess):
    
    greens = 5 - guess.count('_')
    dup_list = []
    for word in possible_words:
        list(word)
        for i in range(0, len(guess)):
            if guess[i] != '_':
                if word[i] == guess[i]:
                    dup_list.append(''.join(word))


    dup = {x for x in dup_list if dup_list.count(x) > greens - 1}

    possible_words = dup

    return possible_words


                
                    
# add function for yellow characters            
                
def narrow_down(words, grey_letters, yellow_letters, guess):
    
    print(len(words))
    words = grey_letter(words, grey_letters)
    print(len(words))
    
    if len(yellow_letters) != 0:
        words = yellow_letter(words, yellow_letters)
    print(len(words))
    
    if guess.count('_') != 5:
        words = green_letter(words, guess)
    print(len(words))

    return words

            

"""def get_pattern(guess):
    pattern = [0]*5

    for i in range(1, len(constraints_string), 2):
        if constraints_string[i] == '1':
            pattern[int((i-1)/2)] = 2
        if constraints_string[i] == '2':
            pattern[int((i-1)/2)] = 1
    
    return tuple(pattern)"""


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


    
            

def entrop_calc(words):
    best_guess = ""
    best_entropy = 0

    for word in words:
        w
        




if __name__ == '__main__':

    possible_words, letters = word_list()
    print(len(possible_words))

    constraints_string = input("Please input constraint string: (ex. t1e2a2r3s3 would mean the word contains a 't' in the correct position, 'e' and 'a' in wrong positions and does not contain 'r' or 's')\n")
        # todo: validation checking
    guess, yellow_letters, grey_letters = filter_guessed_letters(constraints_string)

    possible_letters = [ char for char in letters if char not in grey_letters]
    
    string1 = 'guess: {}'.format(guess)
    print(string1)
    string2 = 'yellow: {}'.format(yellow_letters)
    print(string2)
    string3 = 'rey: {}'.format(grey_letters)
    print(string3)
    string4 = 'possible_letters: {}'.format(possible_letters)
    print(string4)

    possible_words = narrow_down(possible_words, grey_letters, yellow_letters, guess)
