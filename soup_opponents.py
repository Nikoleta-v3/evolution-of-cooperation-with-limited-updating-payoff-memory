import evol_dynamics

import numpy as np

import tqdm

import sys


if __name__ == "__main__":  # pragma: no cover
    filename = "data/soup_for_opponents.csv"
    number_of_checks = 100
    delta = 0.999
    num_of_opponents = 2

    seed = int(sys.argv[1])
    number_of_repetitions = int(sys.argv[2])
    random_state = np.random.RandomState(seed)

    for i in tqdm.tqdm(range(number_of_checks)):
        population_size = 2 * (random_state.randint(50, 150) // 2)
        number_of_mutants = random_state.randint(1, population_size - 1)

        simulated_opponents = evol_dynamics.get_probabilities_for_opponents(
            number_of_repetitions,
            population_size,
            number_of_mutants,
            random_state,
            num_of_opponents,
        )
        theoretical_opponents = (
            evol_dynamics.theoretical_probabilities_for_opponents(
                population_size, number_of_mutants
            )
        )

        data = [
            i,
            number_of_repetitions,
            population_size,
            number_of_mutants,
            *simulated_opponents.values(),
            *theoretical_opponents.values(),
        ]

        with open(filename, "a") as textfile:
            textfile.write(",".join([str(elem) for elem in data]) + "\n")
        textfile.close()
