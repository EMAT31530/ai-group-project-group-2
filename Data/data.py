from typing import List

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
    return read_words_from_file(f"{ROOT_DIR}/Data/wordle-allowed-guesses.txt")


def get_answers() -> List[str]:
    return read_words_from_file(f"{ROOT_DIR}/Data/wordle-answers-alphabetical.txt")
