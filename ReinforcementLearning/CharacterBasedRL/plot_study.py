import pickle

from matplotlib import pyplot as plt
from optuna.importance import get_param_importances
#from optuna.visualization.matplotlib import plot_param_importances, plot_parallel_coordinate
from optuna.visualization import plot_parallel_coordinate
from optuna.visualization.matplotlib import plot_slice

if __name__ == "__main__":
    with open("study8.pkl", "rb") as f:
        study = pickle.load(f)

    all_params = ["batch_size", "n_epochs", "vf_coef",
              "ent_coef", "learning_rate", "clip_range", "gamma", "grad_norm",
                  "gae_lamda", "n_steps"]
    kept_params = ["batch_size", "learning_rate", "vf_coef",
              "gamma"]
    plt.style.use("seaborn-bright")
    importances = get_param_importances(study)
    #importances.pop("activation_fn")
    #importances.pop("net_arch")
    print(importances)
    print(*importances.keys())
    x = [_ for _ in importances.keys()]
    y = [_ for _ in importances.values()]
    #plt.barh(x, y)
    #plt.gca().invert_yaxis()
    #plt.ylabel("Hyper-Parameter")
    #plt.xlabel("Importance for Objective Function")
    #plt.show()
    plot_slice(study, kept_params)
    plt.show()
    f = plot_parallel_coordinate(study, kept_params)
    f.show()