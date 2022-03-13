import os
from collections import Counter
from enum import Enum

import gym
import numpy as np
from gym import spaces

from root import ROOT_DIR

WORD_LENGTH = 5
TOTAL_GUESSES = 6
SOLUTION_PATH = "../words/solution.csv"
VALID_WORDS_PATH = "../words/guess.csv"


class LetterState(Enum):
    ABSENT = 0
    PRESENT = 1
    CORRECT_POSITION = 2


class WordleWordEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def get_words(self, n=None):
        if n:
            return open(f"{ROOT_DIR}/Data/subsets/{n}_5_letter_words.txt").read().splitlines()
        return open(os.path.join(self._current_path(), SOLUTION_PATH)).read().splitlines()

    def _current_path(self):
        return os.path.dirname(os.path.abspath(__file__))

    def _read_solutions(self, wor):
        return open(os.path.join(self._current_path(), SOLUTION_PATH)).read().splitlines()

    def _get_valid_words(self, word_list):
        words = []
        for word in word_list:
            words.append((word, Counter(word)))
        return words

    def __init__(self):
        self.n = 70
        words = self.get_words(self.n)
        self._solutions = words
        self._valid_words = self._get_valid_words(words)
        self.action_space = spaces.Discrete(len(self._valid_words))
        self.observation_space = spaces.MultiDiscrete([3] * TOTAL_GUESSES * WORD_LENGTH)
        np.random.seed(0)
        self.reset()

    def decode(self, action):
        return self._valid_words[action][0]

    def change_num_words(self, n):
        self.n = n
        words = self.get_words(self.n)
        self._solutions = words
        self._valid_words = self._get_valid_words(words)
        self.action_space = spaces.Discrete(len(self._valid_words))
        self.observation_space = spaces.MultiDiscrete([3] * TOTAL_GUESSES * WORD_LENGTH)
        np.random.seed(0)
        self.reset()

    def _check_guess(self, guess, guess_counter):
        c = guess_counter & self.solution_ct
        result = []
        correct = True
        reward = 0
        for i, char in enumerate(guess):
            if c.get(char, 0) > 0:
                if self.solution[i] == char:
                    result.append(2)
                    reward += 5
                else:
                    result.append(1)
                    correct = False
                    reward += 2
                c[char] -= 1
            else:
                result.append(0)
                correct = False
        return result, correct, reward

    def step(self, action):
        """
        action: index of word in valid_words

        returns:
            observation: (TOTAL_GUESSES, WORD_LENGTH)
            reward: 0 if incorrect, 1 if correct, -1 if game over w/o final answer being obtained
            done: True if game over, w/ or w/o correct answer
            additional_info: empty
        """
        guess, guess_counter = self._valid_words[action]
        if guess in self.guesses:
            return self.obs, -1, False, {}
        self.attempts += 1
        self.guesses.append(guess)
        result, correct, reward = self._check_guess(guess, guess_counter)
        done = False

        for i in range(self.guess_no * WORD_LENGTH, self.guess_no * WORD_LENGTH + WORD_LENGTH):
            self.obs[i] = result[i - self.guess_no * WORD_LENGTH]

        self.guess_no += 1
        if correct:
            done = True
            self.won = True
            reward = 25
        if self.guess_no == TOTAL_GUESSES:
            done = True
            if not correct:
                self.won = False
                reward = -15
        return self.obs, reward, done, {}

    def reset(self):
        self.solution = self._solutions[np.random.randint(len(self._solutions))]
        self.solution_ct = Counter(self.solution)
        self.guess_no = 0
        self.guesses = []
        self.obs = np.zeros((TOTAL_GUESSES * WORD_LENGTH,))
        self.won = False
        self.attempts = 0
        return self.obs

    def render(self, mode="human"):
        m = {
            0: "⬜",
            1: "🟨",
            2: "🟩"
        }
        print("Solution:", self.solution)
        for g, o in zip(self.guesses, np.reshape(self.obs, (TOTAL_GUESSES, WORD_LENGTH))):
            o_n = "".join(map(lambda x: m[x], o))
            print(g, o_n)

    def close(self):
        pass


if __name__ == "__main__":
    env = WordleWordEnv()
    print(env.action_space)
    print(env.observation_space)
    print(env.solution)
    print(env.step(0))
    print(env.step(0))
    print(env.step(0))
    print(env.step(0))
    print(env.step(0))
    print(env.step(0))
