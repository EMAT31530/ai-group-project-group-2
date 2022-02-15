from wordle_env.src.wordle_word_env import WordleWordEnv
from wordle_env.src.wordle_char_env import WordleCharEnv


def decode(word):
    return [ord(char) - 97 for char in word.lower()]


# env = WordleCharEnv()
env = WordleWordEnv()

observation = env.reset()

for _ in range(10):
    env.render()
    action = env.action_space.sample()  # your agent here (this takes random actions)
    observation, reward, done, info = env.step(decode("speed"))

    if done:
        observation = env.reset()

env.close()
