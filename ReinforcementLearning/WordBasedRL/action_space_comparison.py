import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import load_results
from stable_baselines3.common.results_plotter import ts2xy

from Data.constants import ACTION_SPACE_SIZES
from ReinforcementLearning.model_evaluation import evaluate_word_model, get_word_evaluation_results
from ReinforcementLearning.training import moving_average
from root import ROOT_DIR


def get_best_model(n):
    return PPO.load(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}/best_model.zip")


def get_models(sizes):
    return {n: get_best_model(n) for n in sizes}


def get_reward(n):
    x, y = ts2xy(load_results(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}"), 'timesteps')
    y = moving_average(y, window=1000)
    x = x[len(x) - len(y):]
    return x, y


def get_rewards(sizes):
    return {n: get_reward(n) for n in sizes}


def get_word_model_evaluations(sizes):
    data = get_models(sizes)
    return {n: evaluate_word_model(data[n]) for n in data.keys()}


def plot_rewards(sizes):
    data = get_rewards(sizes)
    for n in data.keys():
        plt.plot(data[n][0], data[n][1], label=str(n))
    plt.title("Learning Curves")
    plt.ylabel("Mean Episode Reward")
    plt.xlabel("Time Steps")
    plt.legend()
    plt.show()


def plot_win_rates(sizes):
    data = {n: get_word_evaluation_results(n) for n in sizes}

    for n in data.keys():
        plt.plot([x for x in range(len(data[n][1]))], data[n][1], label=n)
        # plt.scatter(n, data[n][1][-1])

    plt.ylabel("Win Rate")
    plt.xlabel("Games Played")
    plt.legend()
    plt.show()


def plot_expected_observed_win_rate(sizes):
    data = {n: get_word_evaluation_results(n) for n in sizes}

    expected_win_rates = [6 / n for n in sizes]
    observed_win_rates = [data[n][1][-1] for n in sizes]

    plt.scatter(range(len(expected_win_rates)), expected_win_rates, label="Probabilty")
    plt.scatter(range(len(observed_win_rates)), observed_win_rates, label="Observed")

    plt.show()


if __name__ == "__main__":
    plt.style.use("seaborn-bright")
    #sizes = ACTION_SPACE_SIZES
    sizes = [7, 10, 13, 16, 19, 23, 30, 40, 50, 100, 300]
    plot_expected_observed_win_rate(sizes)
    #plot_rewards([7, 10, 13, 16, 19, 23, 300])
    #plot_win_rates([7, 10, 13, 16, 19, 23, 300])
