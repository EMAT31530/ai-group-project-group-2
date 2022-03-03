import gym
import optuna
from stable_baselines3 import PPO

from ReinforcementLearning.sample_ppo_params import sample_ppo_params
from ReinforcementLearning.trial_eval_callback import TrialEvalCallback

import ReinforcementLearning.WordBasedRL.wordle_gym


def ppo_objective(trial: optuna.Trial, n_eval_episodes=3, n_timesteps=int(2e4),
                  n_evaluations=2) -> float:
    eval_freq = int(n_timesteps / n_evaluations)
    kwargs = {
        "policy": "MlpPolicy",
        "env": "wordle-v0",
    }

    kwargs.update(sample_ppo_params(trial))
    # Create the RL model
    model = PPO(**kwargs)
    # Create env used for evaluation
    eval_env = gym.make(kwargs["env"])
    # Create the callback that will periodically evaluate
    # and report the performance
    eval_callback = TrialEvalCallback(
        eval_env,
        trial,
        n_eval_episodes=n_eval_episodes,
        eval_freq=eval_freq,
        deterministic=False,
    )

    nan_encountered = False
    try:
        model.learn(n_timesteps, callback=eval_callback)
    except AssertionError as e:
        # Sometimes, random hyperparams can generate NaN
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
