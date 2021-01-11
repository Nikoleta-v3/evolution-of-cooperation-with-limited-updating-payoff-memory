import itertools
import multiprocessing
import os.path
import sys

import numpy as np
from tqdm import tqdm

import evol_dynamics


def simulate_until_invasion(
    N,
    delta,
    beta,
    payoffs,
    mode,
    filename,
    seed=0,
    starting_resident=(0, 0, 0),
):
    data = [*payoffs, N, delta, beta, mode, 0, 0, 0, *starting_resident]
    resident = starting_resident

    with open(filename, "w") as textfile:
        textfile.write(",".join([str(elem) for elem in data]) + "\n")
    textfile.close()

    random_ = np.random.RandomState(seed)
    time_step = 0
    while resident == starting_resident:
        mutant = [random_.random() for _ in range(3)]

        if mode == "expected":
            (
                fixation_probability,
                cooperation,
                score,
            ) = evol_dynamics.fixation_probability_for_expected_payoffs(
                resident, mutant, N, delta, beta, payoffs
            )
        if mode == "stochastic":
            (
                fixation_probability,
                cooperation,
                score,
            ) = evol_dynamics.fixation_probability_for_stochastic_payoffs(
                resident, mutant, N, delta, beta, payoffs
            )

        if random_.random() < fixation_probability:
            resident = mutant
            data[-3:] = resident
            data[-4] = score
            data[-5] = cooperation
            data[-6] = time_step

            with open(filename, "a") as textfile:
                textfile.write(",".join([str(elem) for elem in data]) + "\n")
            textfile.close()

            return resident, time_step
        time_step += 1


if __name__ == "__main__":  # pragma: no cover

    mode = sys.argv[1]
    game = sys.argv[2]
    number_of_process = sys.argv[3]

    if number_of_process == "None":
        number_of_process = multiprocessing.cpu_count()
    p = multiprocessing.Pool(int(number_of_process))

    resident_parameters = [
        ("invade_GTFT", (1, 1, 1 / 3)),
        ("invade_ALLD", (0, 0, 0)),
    ]
    max_seed = 1000
    N_val = 100
    delta = 1 - (10 ** -3)
    beta = 1

    list_of_games = {
        "donation": evol_dynamics.donation_game(1, 3),
        "snowdrift": evol_dynamics.snowdrift_game(1, 3),
        "stag": evol_dynamics.stag_hunt_game(),
        "harmony": evol_dynamics.harmony_game(),
    }
    payoffs = list_of_games[game]
    parameters = itertools.product(resident_parameters, range(max_seed))

    _ = p.starmap(
        simulate_until_invasion,
        [
            (
                N_val,
                delta,
                beta,
                payoffs,
                mode,
                f"data/{opponent_meta[0]}/{game}/{mode}_seed_{seed}.csv",
                seed,
                opponent_meta[1],
            )
            for opponent_meta, seed in parameters
        ],
    )
