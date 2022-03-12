import pickle

import gym
import matplotlib.pyplot as plt
import numpy as np
from stable_baselines3 import PPO

from ReinforcementLearning.model_evaluation import evaluate_character_model
import ReinforcementLearning.CharacterBasedRL.wordle_env.wordle_env
from root import ROOT_DIR


def normalize(dictionary):
    total_sum = sum(dictionary.values())
    factor = 1 / total_sum
    return {key: value * factor for key, value in dictionary.items()}


if __name__ == "__main__":
    with open(f"{ROOT_DIR}/Search/LetterFrequency/letter_frequencies.pkl", "rb") as f:
        letter_frequencies = normalize(pickle.load(f))

    model = PPO.load(f"{ROOT_DIR}/ReinforcementLearning/CharacterBasedRL/models/grey=-2/best_model.zip")

    env = gym.make("WordleChar-v0")
    w, model_letter_frequencies = evaluate_character_model(env, model)
    model_letter_frequencies = normalize(model_letter_frequencies)

    plt.bar(np.arange(len(model_letter_frequencies.keys())), model_letter_frequencies.values(), label="Model Frequency",
            alpha=0.5)
    plt.bar(np.arange(len(letter_frequencies.keys())), letter_frequencies.values(), label="True Frequency", alpha=0.5)
    plt.xticks(range(len(letter_frequencies.keys())), list(letter_frequencies.keys()))
    plt.ylabel("Frequency")
    plt.xlabel("Letter")
    plt.xlim([-1, 26])
    plt.legend()
    plt.show()
