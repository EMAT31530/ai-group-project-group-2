from Search.EntropySearch.calculate_entropy import get_dictionary, filter_uncommon_letters, calculate_entropy, \
    save_dictionary, get_aggregate_distribution
from root import ROOT_DIR

if __name__ == "__main__":
    subset_sizes = [7, 8, 9, 10, 13, 16, 19, 23, 30, 40, 50, 60, 70, 80, 90, 100, 300]

    for size in subset_sizes:
        print(f"s = {size}")
        with open(f"{ROOT_DIR}/Data/subsets/{size}_5_letter_words.txt", "r") as f:
            word_list = f.read().splitlines()
        file_name = f"{ROOT_DIR}/Data/subsets/entropy/entropy_s={size}.pkl"
        print(f"Getting word list ... (s={size}) ")

        entropy_dict = get_dictionary(file_name, word_list)

        for word in entropy_dict.keys():
            if entropy_dict[word][0] is False:
                print(f"Word: {word}")
                entropy = calculate_entropy(get_aggregate_distribution(word, word_list))
                entropy_dict[word] = (True, entropy)
                print(f"Entropy = {entropy}")
                save_dictionary(file_name, entropy_dict)
