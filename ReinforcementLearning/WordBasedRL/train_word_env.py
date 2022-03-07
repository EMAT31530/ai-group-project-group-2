import gym

from ReinforcementLearning.training import train_model, get_best_params, get_smooth_curve, plot_learning_curve
import ReinforcementLearning.WordBasedRL.wordle_gym
from root import ROOT_DIR

if __name__ == "__main__":
    experiment_args = {"batch_size": 256,
                       "n_steps": 64,
                       "gamma": 0.995,
                       "learning_rate": 0.0005537882778359183,
                       "ent_coef": 0.003004556645041577,
                       "clip_range": 0.4,
                       "n_epochs": 5,
                       "gae_lambda": 0.8,
                       "max_grad_norm": 0.7,
                       "vf_coef": 0.5253199800797684}

    rewards = {50: 15.71,
               40: 40.19}
    n = 100
    env = gym.make("WordleWord-v0")
    env.change_num_words(n)
    study_file_path = f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/studies/n={n}/study.pkl"
    model_dir = f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={n}"
    model_name = "best_model"
    model_args = experiment_args if n == 300 else get_best_params(study_file_path)
    #del model_args["net_arch"]
    #del model_args["activation_fn"]
    train_model(env=env, model_name=model_name, dir_path=model_dir, model_args=model_args,
                time_steps=1000000, best_mean_reward=rewards[n])  # Saves model

    x, y = get_smooth_curve(dir_path=model_dir)

    plot_learning_curve(x, y)
