import sys
import numpy as np
import evol_dynamics

import tqdm


if __name__ == "__main__":  # pragma: no cover
    filename = "data/soup_for_rounds_probabilities.csv"
    number_of_checks = 10000
    delta = 0.999

    seed = int(sys.argv[1])
    number_of_repetitions = int(sys.argv[2])
    random_state = np.random.RandomState(seed)

    for i in tqdm.tqdm(range(number_of_checks)):
        mutant = [np.random.random() for _ in range(3)]
        resident = [np.random.random() for _ in range(3)]

        population_size = 2 * (np.random.randint(5, 100) // 2)
        number_of_mutants = np.random.randint(1, population_size)

        stochastic_scores = evol_dynamics.StochasticScores(
            resident,
            mutant,
            delta,
            population_size,
            number_of_mutants,
            number_of_repetitions,
            random_state,
        )

        population = stochastic_scores.create_population()
        simulation_scores = stochastic_scores.get_scores(population)
        theoretical_scores = evol_dynamics.theoretical_utility(
            mutant, resident, delta, number_of_mutants, population_size
        )

        data = [
            i,
            number_of_repetitions,
            *mutant,
            *resident,
            population_size,
            number_of_mutants,
            delta,
            *simulation_scores.values(),
            *theoretical_scores,
        ]

        with open(filename, "a") as textfile:
            textfile.write(",".join([str(elem) for elem in data]) + "\n")
        textfile.close()
