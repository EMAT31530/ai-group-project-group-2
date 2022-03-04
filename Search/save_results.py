from root import ROOT_DIR


def save_results(method_name, guesses, win_rates):
    with open(f"{ROOT_DIR}/Search/{method_name}/guesses.txt", "w+") as f:
        for guess in guesses:
            f.write(f"{guess}\n")

    with open(f"{ROOT_DIR}/Search/{method_name}/win_rates.txt", "w+") as f:
        for rate in win_rates:
            f.write(f"{rate}\n")


def get_results(method_name):
    with open(f"{ROOT_DIR}/Search/{method_name}/guesses.txt", "r") as f:
        guesses = f.read().splitlines()
        guesses = [int(g) for g in guesses]

    with open(f"{ROOT_DIR}/Search/{method_name}/win_rates.txt", "r") as f:
        win_rates = f.read().splitlines()
        win_rates = [float(r) for r in win_rates]

    return guesses, win_rates
