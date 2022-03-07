import os.path
import pickle
import optuna
import torch

from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler
from optuna.visualization import plot_optimization_history, plot_param_importances, plot_contour, plot_edf, plot_slice, \
    plot_parallel_coordinate, plot_intermediate_values


def study_hyperparameters(objective, file_path, n_trials=20):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            study = pickle.load(f)
            study = optimise_hyperparameters(objective=objective, study=study, n_trials=n_trials, )
    else:
        study = optimise_hyperparameters(objective=objective, study=None, n_trials=n_trials)

    return study


def save_study(study, study_file_path, df_file_path):
    # Write report
    study.trials_dataframe().to_csv(df_file_path)

    with open(study_file_path, "wb+") as f:
        pickle.dump(study, f)


def optimise_hyperparameters(objective, study=None, n_startup_trials=5, n_evaluations=2,
                             n_trials=10, timeout=900):
    torch.set_num_threads(1)

    sampler = TPESampler(n_startup_trials=n_startup_trials)
    # Do not prune before 1/3 of the max budget is used
    pruner = MedianPruner(
        n_startup_trials=n_startup_trials, n_warmup_steps=n_evaluations // 3
    )

    if not study:
        study = optuna.create_study(sampler=sampler, pruner=pruner, direction="maximize")

    try:
        study.optimize(objective, n_trials=n_trials, timeout=timeout)
    except KeyboardInterrupt:
        pass

    print("Number of finished trials: ", len(study.trials))

    print("Best trial:")
    trial = study.best_trial

    print(f"  Value: {trial.value}")

    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")

    print("  User attrs:")
    for key, value in trial.user_attrs.items():
        print(f"    {key}: {value}")

    return study


def get_study(file_path):
    with open(file_path, "rb+") as f:
        return pickle.load(f)


def plot_all(study):
    fig1 = plot_optimization_history(study)
    fig2 = plot_param_importances(study)
    fig3 = plot_contour(study)
    fig4 = plot_edf(study)
    fig5 = plot_slice(study)
    fig7 = plot_parallel_coordinate(study)
    fig8 = plot_intermediate_values(study)

    fig1.show()
    fig2.show()
    fig3.show()
    fig4.show()
    fig5.show()
    fig7.show()
    fig8.show()
