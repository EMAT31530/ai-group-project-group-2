import pickle
from collections import Counter

import gym
import matplotlib.pyplot as plt
from stable_baselines3 import PPO

from ReinforcementLearning.model_evaluation import evaluate_word_model
from ReinforcementLearning.WordBasedRL.starting_words.entropy_percentiles import get_entropy_percentiles
import ReinforcementLearning.WordBasedRL.wordle_gym.envs
from root import ROOT_DIR

if __name__ == "__main__":
    percentiles = []
    words = []
    k = [7, 8, 9, 10, 13, 16, 23, 30, 40, 50, 60, 70, 100, 300]
    for n in k:
        env = gym.make("WordleWord-v0")
        env.change_num_words(n)
        model = PPO.load(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}/best_model.zip", env=env)
        with open(f"{ROOT_DIR}/Data/subsets/entropy/entropy_s={n}.pkl", "rb") as f:
            entropy_dict = pickle.load(f)
        _, _, starting_words = evaluate_word_model(env, model=model)

        word_count = Counter(starting_words)
        max_entropy = max(word_count.values())
        starting_word = [k for k, v in word_count.items()
                         if v == max_entropy]

        entropy_percentiles = get_entropy_percentiles(entropy_dict)
        percentile = entropy_percentiles[starting_word[0]]
        percentiles.append(percentile)
        words.append([k for k, v in entropy_percentiles.items() if v == percentile])

        with open(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/starting_words/percentiles.txt", "w+") as f:
            for p in percentiles:
                f.write(f"{p}\n")

        with open(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/starting_words/sizes.txt", "w+") as f:
            for size in k:
                f.write(f"{size}\n")