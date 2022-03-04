import collections

import matplotlib.pyplot as plt
import numpy as np

from Search.save_results import save_results
from vowels_search import simulate

guesses, win_percents, action_space = simulate(epochs=1000)
save_results("VowelSearch", guesses, win_percents)
fig, ax = plt.subplots(2)

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

n_games = len(win_percents)
mean_actions = {i: action_space[i] / n_games for i in action_space.keys()}

plt.bar(mean_actions.keys(), mean_actions.values())
plt.show()
plt.clf()

print(f"Guess frequencies: {guess_frequencies}")
print(f"Mean Guesses: {np.mean(guesses)}")
print(f"Win Percentage: {win_percents[-1] * 100}%")

"""
Guess frequencies: Counter({6: 0.4732510288065844, 5: 0.2839506172839506, 4: 0.18106995884773663, 3: 0.05761316872427984, 2: 0.00411522633744856})
Mean Guesses: 5.1646090534979425
Win Percentage: 24.3%
"""