import os.path

import matplotlib.pyplot as plt
from optuna.visualization.matplotlib import plot_param_importances

from ReinforcementLearning.hyperparameters import default_params
from ReinforcementLearning.objective import Objective
from ReinforcementLearning.tuning import study_hyperparameters, save_study
from root import ROOT_DIR

if __name__ == "__main__":
    n = 70
    stop = input("Make Sure Env Has Correct Action Space: ").lower() != "y"
    if stop:
        exit()
    objective = Objective(env_id="WordleWord-v0", ppo_hyperparameters_func=default_params, )

    study_dir = f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/studies/n={n}/"
    study_name = f"study.pkl"

    while True:
        study = study_hyperparameters(objective=objective, file_path=study_dir + study_name, n_trials=10, )
        os.makedirs(study_dir, exist_ok=True)
        save_study(study, study_file_path=study_dir + study_name,
                   df_file_path=study_dir + f"{study_name}_results.csv")

        #plot_param_importances(study)
        #plt.title(f"n={n}")
        #plt.show()
