import pickle
from typing import Dict

from scipy import stats

from root import ROOT_DIR


def get_entropy_percentiles(entropy_dict) -> Dict[str, float]:
    words = entropy_dict.keys()
    entropy_values = sorted([value[1] for value in entropy_dict.values()])
    percentile_dict = {word: stats.percentileofscore(entropy_values,
                                           entropy_dict[word][1]) for word in words}

    return percentile_dict


if __name__ == "__main__":
    with open(f"{ROOT_DIR}/Data/subsets/entropy/entropy_s=7.pkl", "rb") as f:
        entropy_dict = pickle.load(f)

    print(get_entropy_percentiles(entropy_dict))
