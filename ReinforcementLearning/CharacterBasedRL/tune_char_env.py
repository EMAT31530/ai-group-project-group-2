import os.path

from ReinforcementLearning.hyperparameters import default_params
from ReinforcementLearning.objective import Objective
from ReinforcementLearning.tuning import study_hyperparameters, save_study
from root import ROOT_DIR

if __name__ == "__main__":
    objective = Objective(env_id="WordleChar-v0", ppo_hyperparameters_func=default_params, )

    study_dir = f"{ROOT_DIR}/ReinforcementLearning/CharacterBasedRL/studies/"
    study_name = f"study(all_parameters).pkl"

    while True:
        study = study_hyperparameters(objective=objective, file_path=study_dir + study_name, n_trials=100,)
        os.makedirs(study_dir, exist_ok=True)
        save_study(study, study_file_path=study_dir + study_name,
                   df_file_path=study_dir + f"{study_name}_results.csv")
