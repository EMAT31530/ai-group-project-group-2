from random import choice
from typing import List
from Data.data import get_allowed_guesses, get_answers


class Wordle:
    answer: str
    allowable_words: List[str]
    max_attempts: int
    attempt_number: int
    won: bool
    is_game_over: bool

    def __init__(self, answer=None, max_attempts=6):
        self.answer = answer.upper() if answer else choice(get_answers()).upper()
        self.allowable_words = get_allowed_guesses()
        self.max_attempts = max_attempts
        self.attempt_number = 0
        self.is_game_over = False
        self.won = None
        self.state = []

    def guess_word(self, guess: str):
        self.attempt_number += 1
        guess = guess.upper()
        if not self.is_allowable_word(guess):
            raise Exception(f"{guess} is not a valid word.")

        common_letters = self.get_common_letters(guess)
        correct_letters = self.get_letters_with_correct_index(guess)

        guess_state = (list(guess.upper()),
                       correct_letters,
                       self.word_union(common_letters, correct_letters))

        self.state.append(guess_state)
        if self.attempt_number >= self.max_attempts:
            self.is_game_over = True
            self.won = False

        if guess == self.answer:
            self.is_game_over = True
            self.won = True

        return self.state, guess_state, self.is_game_over

    def get_common_letters(self, guess: str) -> List[str]:
        guess_letters = ''.join(guess.upper())
        common_letters = []
        for letter in guess_letters:
            if letter in self.answer:
                common_letters.append(letter)
            else:
                common_letters.append(" ")

        return common_letters

    def get_letters_with_correct_index(self, guess: str) -> List[str]:
        guess = guess.upper()
        correct_letters = []
        for i in range(len(guess)):
            if guess[i] == self.answer[i]:
                correct_letters.append(guess[i])
            else:
                correct_letters.append(" ")

        return correct_letters

    def word_union(self, common_letters, correct_letters):
        from collections import Counter
        new_word = []
        answer_freq = Counter(self.answer)
        visited_letters = set()
        for i in range(len(common_letters)):
            if common_letters[i] == correct_letters[i]:
                new_word.append(" ")
            else:
                if common_letters[i] not in visited_letters and common_letters[i] != " ":
                    if answer_freq[common_letters[i]] == correct_letters.count(common_letters[i]):
                        visited_letters.add(common_letters[i])
                        new_word.append(" ")
                        continue

                    if answer_freq[common_letters[i]] > new_word.count(common_letters[i]):
                        new_word.append(common_letters[i])
                    else:
                        new_word.append(" ")
                else:
                    new_word.append(" ")

        return new_word

    def is_allowable_word(self, word: str) -> bool:
        return word.lower() in self.allowable_words or word.lower() in get_answers()

    def play_game(self):
        while not self.is_game_over:
            print(f"Attempt: {self.attempt_number} / {self.max_attempts}")
            guess = input("Guess word: ")
            _, _, over = self.guess_word(guess)

            [print(x) for x in self.state]
            print("\n")
            if over:
                self.print_game_over(self.won)

    def blind_play_game(self, guess):
        state = []
        while not self.is_game_over:
            print(f"Attempt: {self.attempt_number} / {self.max_attempts}")
            # guess = input("Guess word: ")
            game_state = self.guess_word(guess)
            common_letters = self.get_common_letters(guess)
            correct_letters = self.get_letters_with_correct_index(guess)
            state.append((list(guess.upper()),
                          correct_letters,
                          self.word_union(common_letters, correct_letters)))
            # [print(x) for x in state]
            # print("\n")
            return state, game_state

    def reset(self,):
        self.__init__()

    def print_game_over(self, won) -> None:
        self.is_game_over = True
        if won:
            print("Well done !")
            return
        print(f"The correct word was {self.answer}")
