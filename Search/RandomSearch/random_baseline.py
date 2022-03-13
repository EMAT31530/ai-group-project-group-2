import collections

import matplotlib.pyplot as plt
import numpy as np

from Search.save_results import save_results
from random_search import simulate

if __name__ == "__main__":
    guesses, win_percents, action_space = simulate(epochs=1000)
    save_results("RandomSearch", guesses, win_percents)
"""fig, ax = plt.subplots(2)

# Guesses Figure
guess_frequencies = collections.Counter(guesses)
for i in guess_frequencies.keys():
    guess_frequencies[i] = guess_frequencies[i] / len(guesses)
# ax[0].set_title("Guesses taken")
ax[0].set_xticks(list(guess_frequencies.keys()))
ax[0].set_ylabel("Frequency")
ax[0].set_xlabel("Guesses")
ax[0].bar(guess_frequencies.keys(), guess_frequencies.values())

# Win Percentages Figure
#ax[1].set_title("Win %")
ax[1].set_ylabel("Win Proportion")
ax[1].set_xlabel("Games Played")
ax[1].plot([i + 1 for i in range(len(win_percents))], win_percents)
plt.tight_layout()

plt.show()
plt.clf()

n_games = len(win_percents)
mean_actions = {i: action_space[i] / n_games for i in action_space.keys()}

plt.bar(mean_actions.keys(), mean_actions.values())
plt.show()

print(f"Guess frequencies: {guess_frequencies}")
print(f"Mean Guesses: {np.mean(guesses)}")
print(f"Win Percent: {win_percents[-1] * 100} %")
"""

plt.style.use("seaborn-bright")
plt.bar(action_space.keys(), action_space.values())
plt.xticks(list(action_space.keys()))
plt.ylabel("Mean Number of Possible Words")
plt.xlabel("Guess Number")
for i, v in enumerate(action_space.values()):
    plt.text(i - .25 , v + 30, str(round(v, 0)), color='black')
plt.show()

"""
Mean Guesses: 5.2217573221757325
Win Percent: 23.9 %
"""
