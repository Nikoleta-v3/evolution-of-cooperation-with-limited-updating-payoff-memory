import itertools
import os.path
import sys
from importlib.machinery import SourceFileLoader

import dask
import numpy as np
from tqdm import tqdm

evolution = SourceFileLoader("evolution", "src/evolution.py").load_module()
simulation = SourceFileLoader("simulation", "src/simulation.py").load_module()


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
            ) = evolution.fixation_probability_for_expected_payoffs(
                resident, mutant, N, delta, beta, payoffs
            )
        if mode == "stochastic":
            (
                fixation_probability,
                cooperation,
                score,
            ) = evolution.fixation_probability_for_stochastic_payoffs(
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
    num_of_cores = sys.argv[3]
    folders = ["invade_GTFT", "invade_ALLD"]
    max_seed = 1000
    N_val = 100
    delta = 1 - (10 ** -3)
    beta = 1

    list_of_games = {
        "donation": simulation.donation_game(1, 3),
        "snowdrift": simulation.snowdrift_game(1, 3),
        "stag": simulation.stag_hunt_game(),
        "harmony": simulation.harmony_game(),
    }

    payoffs = list_of_games[game]

    parameters = itertools.product(folders, range(max_seed))
    jobs = []
    for folder, seed in parameters:
        if folder == "invade_GTFT":
            starting_resident = (1, 1, 1 / 3)
        else:
            starting_resident = (0, 0, 0)
        jobs.append(
            dask.delayed(simulate_until_invasion)(
                N_val,
                delta,
                beta,
                payoffs,
                mode,
                "data/{}/{}/{}_seed_{}.csv".format(folder, game, mode, seed),
                seed=seed,
                starting_resident=starting_resident,
            )
        )
    _ = dask.compute(*jobs, num_of_workers=num_of_cores)
