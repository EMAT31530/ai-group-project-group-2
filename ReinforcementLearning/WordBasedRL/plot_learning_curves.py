import matplotlib.pyplot as plt

from Data.constants import ACTION_SPACE_SIZES
from ReinforcementLearning.training import get_smooth_curve, plot_learning_curve
from root import ROOT_DIR

if __name__ == "__main__":
    sizes = ACTION_SPACE_SIZES

    for _ in sizes:
        #with open(f"{ROOT_DIR}/ReinforcementLearning/models/n={_}/n={_}.txt") as f:
            #lc = f.read().splitlines()
        try:
            x, y = get_smooth_curve(dir_path=f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/models/n={_}")

            if _ < 850:
                plt.plot(x, y, label=_)
        except Exception:
            continue

    plt.legend()
    plt.show()