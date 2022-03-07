import os
import pickle

import numpy as np
from matplotlib import pyplot as plt
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor, load_results
from stable_baselines3.common.results_plotter import ts2xy

from ReinforcementLearning.helpers import is_same_params
from ReinforcementLearning.save_on_best_training_reward_callback import SaveOnBestTrainingRewardCallback
from root import ROOT_DIR


def train_model(env, model_name, dir_path, model_args, time_steps=100000, policy="MlpPolicy"):
    os.makedirs(dir_path, exist_ok=True)
    env = Monitor(env, dir_path)

    callback = SaveOnBestTrainingRewardCallback(model_name=model_name, check_freq=1000, dir_path=dir_path)
    path = os.path.join(dir_path, model_name + ".zip")
    if os.path.exists(path):

        print("Path Exists")
        model = PPO.load(path, env=env, )

        if not is_same_params(get_model_params(model), model_args):
            print("Model Arguments Different")
            print("Creating new model")
            model = PPO(policy, env, **model_args)
            model.learn(total_timesteps=int(time_steps), callback=callback)
        else:
            model.learn(total_timesteps=int(time_steps), callback=callback, reset_num_timesteps=False)

    else:
        print("Path Doesn't Exist")
        print("Creating new model")
        model = PPO(policy, env, **model_args)
        model.learn(total_timesteps=int(time_steps), callback=callback)


def get_best_params(file_path):
    """
    Gets best params from Optuna study.
    :param file_path:
    :return:
    """
    with open(file_path, "rb") as f:
        study = pickle.load(f)

    best_params = study.best_params
    return best_params


def get_model_params(ppo_model: PPO):
    return {
        "batch_size": ppo_model.batch_size,
        "n_steps": ppo_model.n_steps,
        "gamma": ppo_model.gamma,
        "learning_rate": ppo_model.learning_rate,
        "ent_coef": ppo_model.ent_coef,
        'clip_range': ppo_model.clip_range,
        'n_epochs': ppo_model.n_epochs,
        'gae_lambda': ppo_model.gae_lambda,
        'max_grad_norm': ppo_model.max_grad_norm,
        'vf_coef': ppo_model.vf_coef
    }


def moving_average(values, window):
    weights = np.repeat(1.0, window) / window
    return np.convolve(values, weights, 'valid')


def get_smooth_curve(dir_path, window=1000):
    x, y = ts2xy(load_results(dir_path), 'timesteps')
    y = moving_average(y, window=window)
    # Truncate x
    x = x[len(x) - len(y):]

    return x, y


def save_learning_curve(y, file_path):
    with open(file_path, 'w') as f:
        for item in y:
            f.write("%s\n" % item)


def plot_learning_curve(x, y, title='Learning Curve'):
    fig = plt.figure(title)
    plt.plot(x, y)
    plt.xlabel('Time Steps')
    plt.ylabel('Mean Episode Reward')
    plt.title(title)
    plt.show()
