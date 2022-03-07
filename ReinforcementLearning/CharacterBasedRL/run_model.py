import gym
from stable_baselines3 import PPO

from ReinforcementLearning.model_evaluation import test_model

import ReinforcementLearning.CharacterBasedRL.gym_wordle
from root import ROOT_DIR

if __name__ == "__main__":
    env = gym.make("WordleChar-v0")
    model = PPO.load(f"{ROOT_DIR}/ReinforcementLearning/CharacterBasedRL/models/best_model.zip")
    test_model(env=env, model=model, tests=1)