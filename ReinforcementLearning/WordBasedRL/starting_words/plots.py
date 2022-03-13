from matplotlib import pyplot as plt

from root import ROOT_DIR

if __name__ == "__main__":
    with open(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/starting_words/percentiles.txt", "r") as f:
        percentiles = f.read().splitlines()

    with open(f"{ROOT_DIR}/ReinforcementLearning/WordBasedRL/starting_words/sizes.txt", "r") as f:
        k = f.read().splitlines()

    plt.style.use("seaborn-bright")
    percentiles = [float(p) for p in percentiles]
    plt.bar(range(len(percentiles)), percentiles)
    plt.ylabel("Starting Word Entropy Percentile")
    plt.xlabel("Number of Words")
    plt.xticks(range(len(percentiles)), [str(_) for _ in k])
    plt.show()
