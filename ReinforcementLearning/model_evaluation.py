import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from root import ROOT_DIR


def test_model(env, model, tests=1):
    for i in range(tests):
        obs = env.reset()
        done = False
        while not done:
            action, _states = model.predict(obs)
            obs, rewards, done, info = env.step(action)
            env.render()


def evaluate_word_model(env, model, episodes=1000, play_random=False, verbose=False):
    guesses = []
    win_rates = []
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

            obs, rewards, done, info = env.step(action)
            if env.attempts == 1:
                starting_words.append(action)
            if env.won:
                guesses.append(env.attempts)
                wins += 1
            win_rates.append(wins / (i + 1))

            if verbose:
                env.render()

    return guesses, win_rates, starting_words


def plot_word_model_win_rate(win_rates, n=None):
    print(f"Win Rate = {win_rates[-1]}")
    plt.plot([x for x in range(len(win_rates))], win_rates)
    if n:
        plt.title(f"n={n}")
        plt.axhline(y=6 / n, color="red", linestyle="--")
    plt.show()


def save_word_evaluation_results(guesses, win_rates, n):
    with open(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}/guesses.txt", "w+") as f:
        for guess in guesses:
            f.write(f"{guess}\n")

    with open(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}/win_rates.txt", "w+") as f:
        for rate in win_rates:
            f.write(f"{rate}\n")


def get_word_evaluation_results(n):
    with open(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}/guesses.txt", "r") as f:
        guesses = f.read().splitlines()
        guesses = [float(g) for g in guesses]

    with open(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}/win_rates.txt", "r") as f:
        win_rates = f.read().splitlines()
        win_rates = [float(r) for r in win_rates]

    return guesses, win_rates
