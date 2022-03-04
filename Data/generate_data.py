import random
from typing import List

from Data.constants import ACTION_SPACE_SIZES
from Data.data import get_all_words
from root import ROOT_DIR


def create_word_lists(n_words_vec: List[str], word_list: List[str], n_letters=5):
    word_lists = {n: None for n in n_words_vec}
    word_lists[n_words_vec[-1]] = random.sample(list(word_list), n_words_vec[-1])
    for n in range(2, len(n_words_vec) + 1):
        word_lists[n_words_vec[-n]] = random.sample(word_lists[n_words_vec[-n + 1]], n_words_vec[-n])

    for n in n_words_vec:
        with open(f"{ROOT_DIR}/Data/{n}_{n_letters}_letter_words.txt", "w") as f:
            for word in word_lists[n]:
                f.write(f"{word}\n")


"""def generate_from_prexisting(n1, n2):
    

    :param n1: Closest But Smaller than n1 Word List
    :param n2: New Word List Length
    :return:
    

    n_words_to_add = n2 - n1

    with open(f"{ROOT_DIR}/Data/{n1}_{5}_letter_words.txt", "r") as f:
        n1_words = f.read().splitlines()

    with open(f"{ROOT_DIR}/Data/{n2}_{5}_letter_words.txt", "r") as f:
        n2_words = f.read().splitlines()

    unique_words = list(set(n1_words).symmetric_difference(set(n2_words)))

    n1_words.append(random.sample(unique_words), n_words_to_add)
    with open(f"{ROOT_DIR}/Data/{n}_5_letter_words.txt", "w") as f:
        for word in unique_words:
            f.write(f"{word}\n")"""


if __name__ == "__main__":
    create_word_lists(ACTION_SPACE_SIZES, get_all_words(), 5)