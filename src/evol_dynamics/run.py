import evol_dynamics

import numpy as np

from tqdm import tqdm

def main(
    N,
    delta,
    beta,
    number_of_steps,
    payoffs,
    mode,
    seed=10,
    starting_resident=(0, 0, 0),
):
    data = [*payoffs, N, delta, beta, 0, 0, *starting_resident]
    resident = starting_resident
    history = np.zeros((number_of_steps + 1, 12))
    history[0] = data
    random_ = np.random.RandomState(seed)

    for t in tqdm(range(number_of_steps)):
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


        history[t + 1] = data

    return history


if __name__ == "__main__":  # pragma: no cover

    number_of_steps = 10 ** 7
    payoffs = [3, 0, 5, 1]
    mode = "expected"
    seed = 1

    filename = "test.csv"

    history = main(
        N=100,
        delta=1 - (10 ** -3),
        beta=1,
        number_of_steps=number_of_steps,
        payoffs=payoffs,
        mode=mode,
        seed=seed,
    )

    np.savetxt(filename, history, delimiter=",")