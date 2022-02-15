import random

from wordle_env.wordle_env.src.wordle_word_env import WordleWordEnv
from Data.data import *

words = get_answers() + get_allowed_guesses()


def decode(word):
    return [ord(char) - 97 for char in word.lower()]


# env = WordleCharEnv()
env = WordleWordEnv()

observation = env.reset()

for _ in range(10):
    env.render()
    action = env.action_space.sample()  # your agent here (this takes random actions)
    observation, reward, done, info = env.step(decode(random.choice(words)))

    if done:
        observation = env.reset()

env.close()
