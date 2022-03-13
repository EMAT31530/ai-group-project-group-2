import gym
from stable_baselines3 import PPO

from ReinforcementLearning.model_evaluation import evaluate_word_model, test_model, plot_word_model_win_rate, \
    get_word_evaluation_results, save_word_evaluation_results
from root import ROOT_DIR

import ReinforcementLearning.WordBasedRL.wordle_gym


def get_model(n):
    return PPO.load(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}/best_model.zip")


if __name__ == "__main__":
    n = 70
    env = gym.make("WordleWord-v0")
    env.change_num_words(n)
    model = get_model(n)
    test_model(env, model)
    # g, w = get_evaluation_results(n)
    g, w, s = evaluate_word_model(env, model, episodes=1000)
    plot_word_model_win_rate(w, n=n)
    save_word_evaluation_results(g, w, n)
