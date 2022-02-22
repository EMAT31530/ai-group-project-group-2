from typing import List

import numpy as np

from Data.data import get_answers

words = get_answers()


def get_remaining_words_guess_known(word_list: List[str], wordle_state):
    # Word list has to be lower case.
    guess = [x.lower() for x in wordle_state[0]]
    correct_letters = [x.lower() for x in wordle_state[1]]
    common_letters = "".join(wordle_state[2]).replace(" ", "").lower()
    uncommon_letters = list(set(guess) - set(common_letters) - set("".join(correct_letters).replace(" ", "")))

    new_list = [w for w in word_list if all(c in w for c in common_letters)]
    new_list = [w for w in new_list if not any(c in w for c in uncommon_letters)]
    new_list = [w for w in new_list if all(c in w for c in "".join(correct_letters).replace(" ", ""))]

    final_list = set(new_list)
    for word in new_list:
        w = list(word)

        for i in range(5):
            if not w[i] != correct_letters[i] and correct_letters[i] != " ":
                final_list.add(word)

    return np.array(list(final_list))


def get_possible_words(word, word_list):
    """
    Gets list of without words that do not provide information given
    the word param.
    :param word: Word.
    :param word_list: Word List.
    :return:
    """

    return [w for w in word_list if any(c in w for c in word)]
