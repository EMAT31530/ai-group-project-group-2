import optuna
import torch
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler


def optimise_hyperparameters(objective, study=None,n_startup_trials=5, n_evaluations=2,
                             n_trials=10, n_jobs=3, timeout=900):
    torch.set_num_threads(1)

    sampler = TPESampler(n_startup_trials=n_startup_trials)
    # Do not prune before 1/3 of the max budget is used
    pruner = MedianPruner(
        n_startup_trials=n_startup_trials, n_warmup_steps=n_evaluations// 3
    )

    if not study:
        study = optuna.create_study(sampler=sampler, pruner=pruner, direction="maximize")

    try:
        study.optimize(objective, n_trials=n_trials, n_jobs=n_jobs, timeout=timeout)
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
