import evol_dynamics

import numpy as np

import tqdm

import sys


if __name__ == "__main__":  # pragma: no cover
    filename = "data/soup_for_sixteen_states_stationary.csv"
    number_of_checks = 100
    delta = 0.999

    seed = int(sys.argv[1])
    number_of_repetitions = int(sys.argv[2])
    random_state = np.random.RandomState(seed)

    for i in tqdm.tqdm(range(number_of_checks)):
        mutant = [random_state.random() for _ in range(3)]
        resident = [random_state.random() for _ in range(3)]

        v_last_two_rounds = evol_dynamics.stationary_for_16_states(
            mutant, resident, delta
        )
        v_last_round = evol_dynamics.expected_distribution_last_round(
            mutant, resident, delta
        )
        v_simulated = evol_dynamics.simulated_states(
            mutant, resident, delta, number_of_repetitions, rounds_of_history=2
        )

        data = [
            i,
            number_of_repetitions,
            *mutant,
            *resident,
            delta,
            *v_last_two_rounds,
            *v_last_round,
            *v_simulated.values(),
        ]

        with open(filename, "a") as textfile:
            textfile.write(",".join([str(elem) for elem in data]) + "\n")
        textfile.close()
