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
    answer_list = []

    random.shuffle(answers)
    

    for i in range(0, 1000):
        answer_list.append(answers[i])

    return answer_list


def word_list():

    five_letter_words = read_words()

    possible_letters = list('abcdefghijklmnopqrstuvwxyz')
    
    return five_letter_words, possible_letters




def filter_guessed_letters(constraints_string):
    if len(constraints_string) == 0:
        return []
    wordle = list("_____")
    yellows = list("_____")
    letter_in_wrong_pos = []
    no_letter = []
    #print(len(constraints_string))
    #print(constraints_string)
    
    for i in range(0, len(constraints_string), 2):   
        count = 0
        if constraints_string[i+1] == '2':
            letter_in_wrong_pos.append(constraints_string[i])
            yellows[int(i/2)] = constraints_string[i]
        if constraints_string[i+1] == '3':
            no_letter.append(constraints_string[i])
        if constraints_string[i+1] == '1':
            wordle[int(i/2)] = constraints_string[i]
        count = count + 1
        
    #print(wordle)

    return wordle, letter_in_wrong_pos, no_letter, yellows


def grey_letter(possible_words, grey_letters, guess_list):
    #print(guess_list)
    #print('grey letters')
    words = []
    for char in grey_letters:
        if char not in guess_list:
            for word in possible_words:
                if char in word:
                    words.append(word)
                    #possible_words.remove(word)

        if char in guess_list:
            for word in possible_words:
                list(word)
                for i in range(0, len(guess_list)):
                    if guess[i] != '_':
                        if word[i] != guess_list[i]:
                            words.append(''.join(word))
            
            

    words = list(set(words))

    for word in words:
        if word in possible_words:
            possible_words.remove(word)

            


    return possible_words



def yellow_letter(possible_words, yellow_letters, yellow_in_guess):
    yellows = len(yellow_letters) - 1
    dup_list = []
    list2 = []
    #print(yellow_in_guess)
    #print('yellow letters')

    for word in possible_words:
        list(word)
        for i in range(0, len(yellow_in_guess)):
            if yellow_in_guess[i] != '_':
                if word[i] == yellow_in_guess[i]:
                    list2.append(word)

    list2 = list(set(list2))

    for word in list2:
        if word in possible_words:
            possible_words.remove(word)
                    


    
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
                
def narrow_down(words, grey_letters, yellow_letters, guess_list, guess_yellows, guess_str):
    #print(grey_letters)
    #print(yellow_letters)
    #print(guess_list)
    #print(guess_yellows)
    #print(len(words))
    words = grey_letter(words, grey_letters, guess_list)
    print(len(words))
    
    if len(yellow_letters) != 0:
        words = yellow_letter(words, yellow_letters, guess_yellows)
    #print(len(words))
    
    if guess_list.count('_') != 5:
        words = green_letter(words, guess_list)
    #print(len(words))

    if guess_str in words:
        words.remove(guess_str)

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




def compare(guess_str, answer):
    """make the guess readable for the algorithm"""

    print('we are guessing:    {}'.format(guess_str))
    

    
    input_cons = []
    for i in range(0, 5):
        if guess_str[i] == answer[i]:
            input_cons.append(guess_str[i])
            input_cons.append('1')

        if guess_str[i] not in answer:
            input_cons.append(guess_str[i])
            input_cons.append('3')

        if guess_str[i] in answer:
            if guess_str[i] != answer[i]:
                input_cons.append(guess_str[i])
                input_cons.append('2')

    input_cons = ''.join(input_cons)
    return input_cons



"""  actual game order functions  """




def game_turn1(guess_str, answer):
    
    
    yellow = []
    grey = []
    

    constraints_string = compare(guess_str, answer)

    guess, yellow, grey, guess_yellow = filter_guessed_letters(constraints_string)

    return guess, yellow, grey, guess_yellow


def game_turn2(possible_words):


    p_dict = get_pattern_dict(possible_words)
    
    entrop = calculate_entropies(possible_words, p_dict)

    if len(entrop) == 0:
        print('out of possible words')

        return end == 1

    else:
        fin_max = max(entrop, key=entrop.get)
        entrop_value = entrop[fin_max]

        print('We suggest {} to be the next guess, it has an entropy of :  {}'.format(fin_max, entrop_value))

    return fin_max



def wordle(answer):

    answer = answer
    print('we are trying to guess the word:  {}'.format(answer))
    guess_str = 'arise' # we take the first guess to always be arise
    possible_words, letters = word_list()

    yellow_letters = []
    grey_letters = []
    green_letters = []
    count = 0
    won = 0
    games_played = 0

    for t in range(1,20):
        count += 1
        #print(guess_str)

        if guess_str == answer:
            print('correct word was guessed:  {}'.format(answer))
            print(' number of attempts:  {}'.format(count))
            print('')
            print('               ---------------------------------------------------------------')
            print('')
            if count > 6:
                won = 0
            else:
                won = 1
            return count, won

        yellow = []
        grey = []
        guess_yellows = []

        guess1, yellow, grey, guess_yellows = game_turn1(guess_str, answer)

        yellow_letters.extend(yellow)
        grey_letters.extend(grey)

        yellow_letters = list(set(yellow_letters))
        grey_letters = list(set(grey_letters))

        possible_letters = [ char for char in letters if char not in grey_letters]


        possible_words = narrow_down(possible_words, grey_letters, yellow_letters, guess1, guess_yellows, guess_str)
    
        guess_str = game_turn2(possible_words)

        

def game():

    wins = 0
    guesses = []
    games_played = 0
    games_won = []
    games_won2 = []
    
    answers = get_answers()
    #answers = ['blaze']

    for i in answers:
        
        games_played += 1
        print('game number:   {}'.format(games_played))
        a, b = wordle(i)

        wins += b


        if b == 1:
            games_won.append('won')
        if b != 1:
            games_won.append('lost')

        games_won2.append(b)

        
        guesses.append(a)

    games_won2 = np.array(games_won2)
    win_rate = np.mean(games_won2)

    guesses = np.array(guesses)
    mean_guess = np.mean(guesses)

    print('{}  wins'.format(wins))

    print('{}  win rate'.format(win_rate))

    print('mean number of guesses =  {}'.format(mean_guess))

    

    ind = list(range(1, len(answers)+1))
    index_list = []
    for i in ind:
        index_list.append(i)

    d = { 'words' : answers , 'guesses' : guesses , 'result' : games_won}
    df = pd.DataFrame( data = d, index = index_list)

    df.to_csv("1000_wordle_trials.csv")

    return df


#      game
if __name__ == '__main__':

    df = game()
