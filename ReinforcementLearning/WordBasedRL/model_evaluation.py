import sys
from collections import Counter

from stable_baselines3 import PPO
import matplotlib.pyplot as plt
import gym

sys.path.append("")
sys.path.append("..")
import wordle_gym


def evaluate_model(model, episodes=1000, play_random=False, verbose=False):
    env = gym.make("wordle-v0")

    guesses = []
    win_p = []
    wins = 0
    starting_words = []
    for i in range(episodes):
        obs = env.reset()
        done = False

        while not done:
            if play_random:
                action = env.action_space.sample()
            else:
                action, _states = model.predict(obs)
            if len(env.guesses) == 0:
                starting_words.append(env._valid_words[action][0])
            obs, rewards, done, info = env.step(action)
            if env.won:
                guesses.append(env.attempts)
                wins += 1
                win_p.append(wins / (i + 1))

            if verbose:
                env.render()

    return guesses, win_p


def plot_model_results(guesses, win_p):
    print(f"% = {win_p[-1]}")
    plt.plot([x for x in range(len(win_p))], win_p)
    plt.show()

if __name__ == "__main__":
    model = PPO.load("train_agents/tmp/best_model.zip")
