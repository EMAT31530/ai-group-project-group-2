import gym

from ReinforcementLearning.training import train_model, get_best_params, get_smooth_curve, plot_learning_curve
import ReinforcementLearning.CharacterBasedRL.gym_wordle
from root import ROOT_DIR

if __name__ == "__main__":
    env = gym.make("WordleChar-v0")
    study_file_path = f"{ROOT_DIR}/ReinforcementLearning/CharacterBasedRL/studies/study(all_parameters).pkl"
    model_dir = f"{ROOT_DIR}/ReinforcementLearning/CharacterBasedRL/models"
    model_name = "best_model"
    model_args = get_best_params(study_file_path)
    train_model(env=env, model_name=model_name, dir_path=model_dir, model_args=model_args,
                time_steps=1000000, policy="MultiInputPolicy")  # Saves model

    x, y = get_smooth_curve(dir_path=model_dir)

    plot_learning_curve(x, y)
