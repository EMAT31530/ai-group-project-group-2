import gym
import optuna
from stable_baselines3 import PPO

from ReinforcementLearning.trial_eval_callback import TrialEvalCallback
#import ReinforcementLearning.CharacterBasedRL.wordle_env.wordle_env
import ReinforcementLearning.WordBasedRL.wordle_gym


class Objective:
    def __init__(self, env_id, ppo_hyperparameters_func, n_eval_episodes=3, n_time_steps=int(2e4),
                 n_evaluations=2):

        self.env_id = env_id
        self.params_func = ppo_hyperparameters_func
        self.n_eval_episodes = n_eval_episodes
        self.n_time_steps = n_time_steps
        self.n_evaluations = n_evaluations

    def __call__(self, trial):
        eval_freq = int(self.n_time_steps / self.n_evaluations)

        policy = "MlpPolicy"

        kwargs = {
            "policy": policy,
            "env": self.env_id,
        }

        kwargs.update(self.params_func(trial))
        # Create the RL model
        model = PPO(**kwargs)
        # Create env used for evaluation
        eval_env = gym.make(kwargs["env"])
        # Create the callback that will periodically evaluate
        # and report the performance
        eval_callback = TrialEvalCallback(
            eval_env,
            trial,
            n_eval_episodes=self.n_eval_episodes,
            eval_freq=eval_freq,
            deterministic=False,
        )

        nan_encountered = False
        try:
            model.learn(self.n_time_steps, callback=eval_callback)
        except AssertionError as e:
            # Sometimes, random hyperparameters can generate NaN
            print(e)
            nan_encountered = True
        finally:
            # Free memory
            model.env.close()
            eval_env.close()

        # Tell the optimizer that the trial failed
        if nan_encountered:
            return float("nan")

        if eval_callback.is_pruned:
            raise optuna.exceptions.TrialPruned()

        return eval_callback.last_mean_reward
