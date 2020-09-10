from collections import Counter
from importlib.machinery import SourceFileLoader

import numpy as np
import pandas as pd
from tqdm import tqdm

import os.path

evolution = SourceFileLoader("evolution", "src/evolution.py").load_module()
formulation = SourceFileLoader(
    "formulation", "src/formulation.py"
).load_module()


def main(
    N_val,
    d_val,
    b_val,
    number_of_steps,
    payoffs,
    mode,
    seed=0,
    starting_resident=(0, 0, 0),
    filename="expected_payoff_data.csv",
):

    if os.path.isfile(filename):
        df = pd.read_csv(filename, header=None)
        resident = df.iloc[-1].values
        seed = len(df)
    else:
        resident = starting_resident

    history = [resident]
    random_ = np.random.RandomState(seed)

    for _ in tqdm(range(number_of_steps)):
        mutant = [random_.random() for _ in range(3)]

        phi = fixation_probability(
            resident, mutant, N_val, d_val, b_val, payoffs, mode
        )

        if random_.random() < phi:
            resident = mutant

        with open(filename, "a") as textfile:
            textfile.write(
                ",".join([str(elem) for elem in resident]) + "\n"
            )
        textfile.close()
        history.append(resident)
    return history


def _reshape_history(history):
    points = [(i, j) for _, i, j in history]
    x, y, weights = zip(
        *[
            (point[0], point[1], weight)
            for point, weight in Counter(points).items()
        ]
    )
    return x, y, weights


def donation_game(c, b):
    return (b - c, -c, b, 0)


def ratio_of_mutant_fixation(resident, mutant, N, k, delta, beta, payoffs):

    return evolution.probability_mutant_descreases(
        resident, mutant, N, k, delta, beta, payoffs
    ) / evolution.probability_mutant_increases(
        resident, mutant, N, k, delta, beta, payoffs
    )


def fixation_probability(resident, mutant, N, delta, beta, payoffs, mode):
    if mode == "s":
        ratio = ratio_of_mutant_fixation
    if mode == "e":
        ratio = evolution.ratio_of_expected_payoffs
    if mode not in ["s", "e"]:
        print("Chose a feasible mode.")
        exit()

    gammas = [
        ratio(resident, mutant, N, k, delta, beta, payoffs) for k in range(1, N)
    ]

    return 1 / (1 + np.sum(np.cumprod(gammas)))


if __name__ == "__main__":

    N_val = 100
    d_val = 1 - (10 ** -3)
    b_val = 1
    number_of_steps = 50
    payoffs = donation_game(1, 3)

    _ = main(
        N_val,
        d_val,
        b_val,
        number_of_steps,
        payoffs,
        "e",
    )
