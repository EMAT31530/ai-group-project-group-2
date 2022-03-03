import string
from typing import List

import numpy as np

from root import ROOT_DIR


def read_words_from_file(file_path) -> List[str]:
    """
    Assumes txt file of line seperated words.
    :param file_path:
    :return: A list of words.
    """
    with open(file_path, 'r') as f:
        words = []
        for line in f:
            word = line.strip()
            words.append(word)
    return words


def get_allowed_guesses() -> List[str]:
    return np.array(read_words_from_file(f"{ROOT_DIR}/Data/wordle-allowed-guesses.txt"))


def get_answers() -> List[str]:
    return np.array(read_words_from_file(f"{ROOT_DIR}/Data/wordle-answers-alphabetical.txt"))


def get_all_words(n_letters=5) -> List[str]:
    if n_letters == 5:
        return np.concatenate((get_answers(), get_allowed_guesses()))
    elif n_letters == 3:
        return np.array(read_words_from_file(f"{ROOT_DIR}/Data/3_letter_words.txt"))


def decode_letter(index: int) -> str:
    return string.ascii_lowercase[index]


def encode_letter(letter: str) -> int:
    return string.ascii_lowercase.index(letter)
