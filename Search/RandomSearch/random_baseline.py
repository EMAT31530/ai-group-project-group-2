import collections

import matplotlib.pyplot as plt
import numpy as np

from random_search import simulate

guesses, win_percents, action_space = simulate("aback", epochs=1000)
#fig, ax = plt.subplots(2)

# Guesses Figure
guess_frequencies = collections.Counter(guesses)
for i in guess_frequencies.keys():
    guess_frequencies[i] = guess_frequencies[i] / len(guesses)
# ax[0].set_title("Guesses taken")
"""ax[0].set_xticks(guess_frequencies.keys())
ax[0].set_ylabel("Frequency")
ax[0].set_xlabel("Guesses")
ax[0].bar(guess_frequencies.keys(), guess_frequencies.values())

# Win Percentages Figure
#ax[1].set_title("Win %")
ax[1].set_ylabel("Win Proportion")
ax[1].set_xlabel("Games Played")
ax[1].plot([i + 1 for i in range(len(win_percents))], win_percents)
plt.tight_layout()"""

#plt.show()

n_games = len(win_percents)
mean_actions = {i: action_space[i] / n_games for i in action_space.keys()}

plt.bar(mean_actions.keys(), mean_actions.values())
plt.show()

print(f"Guess frequencies: {guess_frequencies}")
print(f"Mean Guesses: {np.mean(guesses)}")
print(f"Win Proportion: {win_percents[-1] * 100}")
