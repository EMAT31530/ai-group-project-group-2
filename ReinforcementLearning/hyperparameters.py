from typing import Union, Callable, Dict, Any

import optuna


def linear_schedule(initial_value: Union[float, str]) -> Callable[[float], float]:
    """
    Linear learning rate schedule.
    :param initial_value: (float or str)
    :return: (function)
    """
    if isinstance(initial_value, str):
        initial_value = float(initial_value)

    def func(progress_remaining: float) -> float:
        """
        Progress will decrease from 1 (beginning) to 0
        :param progress_remaining: (float)
        :return: (float)
        """
        return progress_remaining * initial_value

    return func


def default_params(trial: optuna.Trial) -> Dict[str, Any]:
    """
    Sampler for PPO hyperparameters.
    :param trial:
    :return:
    """
    batch_size = trial.suggest_categorical("batch_size", [32, 64, 128, 256, 512])
    n_steps = trial.suggest_categorical("n_steps", [64, 128, 256, 512, 1024, 2048])
    gamma = trial.suggest_categorical("gamma", [0.9, 0.95, 0.99, 0.995, 0.999, 0.9999])
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-3)
    lr_schedule = "constant"
    # Uncomment to enable learning rate schedule
    # lr_schedule = trial.suggest_categorical('lr_schedule', ['linear', 'constant'])
    ent_coef = trial.suggest_loguniform("ent_coef", 1e-4, 1e-2)
    clip_range = trial.suggest_categorical("clip_range", [0.1, 0.2, 0.3, 0.4])
    n_epochs = trial.suggest_categorical("n_epochs", [1, 5, 10, 20])
    gae_lambda = trial.suggest_categorical("gae_lambda", [0.8, 0.9, 0.92, 0.95, 0.98, 0.99, 1.0])
    max_grad_norm = trial.suggest_categorical("max_grad_norm", [0.3, 0.5, 0.7, 0.9, 1, 2, 5])
    vf_coef = trial.suggest_uniform("vf_coef", 0, 1)

    if batch_size > n_steps:
        batch_size = n_steps

    if lr_schedule == "linear":
        learning_rate = linear_schedule(learning_rate)

    return {
        "n_steps": n_steps,
        "batch_size": batch_size,
        "gamma": gamma,
        "learning_rate": learning_rate,
        "ent_coef": ent_coef,
        "clip_range": clip_range,
        "n_epochs": n_epochs,
        "gae_lambda": gae_lambda,
        "max_grad_norm": max_grad_norm,
        "vf_coef": vf_coef,
    }


def reduced_char_ppo_params(trial: optuna.Trial) -> Dict[str, Any]:
    batch_size = trial.suggest_categorical("batch_size", [32, 64, 128, 256, 512])
    n_steps = trial.suggest_categorical("n_steps", [64, 128, 256, 512, 1024, 2048])
    gamma = trial.suggest_categorical("gamma", [0.8, 0.9, 0.95, 0.99, 0.995, 0.999, 0.9999])
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-3)
    lr_schedule = "constant"
    vf_coef = trial.suggest_uniform("vf_coef", 0, 1)

    if batch_size > n_steps:
        batch_size = n_steps

    if lr_schedule == "linear":
        learning_rate = linear_schedule(learning_rate)

    return {
        "batch_size": batch_size,
        "gamma": gamma,
        "learning_rate": learning_rate,
        "vf_coef": vf_coef,
    }