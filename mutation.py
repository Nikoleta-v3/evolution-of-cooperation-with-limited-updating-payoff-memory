import numpy as np
import time

import tqdm


def stationary_reactive(p1, p2, delta):
    M = np.array(
        [
            [
                p1[1] * p2[1],
                p1[1] * (1 - p2[1]),
                (1 - p1[1]) * p2[1],
                (1 - p1[1]) * (1 - p2[1]),
            ],
            [
                p1[2] * p2[1],
                p1[2] * (1 - p2[1]),
                (1 - p1[2]) * p2[1],
                (1 - p1[2]) * (1 - p2[1]),
            ],
            [
                p1[1] * p2[2],
                p1[1] * (1 - p2[2]),
                (1 - p1[1]) * p2[2],
                (1 - p1[1]) * (1 - p2[2]),
            ],
            [
                p1[2] * p2[2],
                p1[2] * (1 - p2[2]),
                (1 - p1[2]) * p2[2],
                (1 - p1[2]) * (1 - p2[2]),
            ],
        ]
    )

    v0 = np.array(
        [
            p1[0] * p2[0],
            p1[0] * (1 - p2[0]),
            (1 - p1[0]) * p2[0],
            (1 - p1[0]) * (1 - p2[0]),
        ]
    )

    return (1 - delta) * v0 @ np.linalg.inv((np.eye(4) - delta * M))


def payoffsExpected(res, mut, population, u, N, delta):

    payoffs = np.zeros((N, 2))
    indices = [res, mut]

    for i, mbr in enumerate(population):
        for j, idx in enumerate(indices):

            if i != j:
                v = stationary_reactive(population[idx, :], mbr, delta)
                payoffs[i, j] = v @ u

    return sum(payoffs) / (N - 1)


def payoffsLastRound(res, mut, population, u, N, delta):

    payoffs = np.zeros((1, 2))
    exclude = [res]

    mbr_id = np.random.choice(list(set(range(N)) - set(exclude)))
    v = stationary_reactive(population[res, :], population[mbr_id, :], delta)
    payoffs[0, 0] = np.random.choice(u, p=v.round(15))

    if mbr_id == mut:

        payoffs[0, 1] = np.array([u[0], u[2], u[1], u[3]])[payoffs[0, 0] == u]

        return payoffs[0]

    exclude.append(mbr_id)

    mbr_id = np.random.choice(list(set(range(N)) - set(exclude)))
    v = stationary_reactive(population[mut, :], population[mbr_id, :], delta)
    payoffs[0, 1] = np.random.choice(u, p=v.round(15))

    return payoffs[0]


if __name__ == "__main__":  # pragma: no cover

    N = 100
    delta = 0.999
    beta = 1
    mutation = 0.1
    number_of_steps = 10 ** 5
    payoffs = np.array([2, -1, 3, 0])
    payoff_type = "stochastic"
    filename = "mutation_expected.csv"
    seed = 10
    starting_resident = (0, 0, 0)
    sdim = 3
    start_time = time.time()

    population = starting_resident * np.ones((N, sdim))

    for t in tqdm.tqdm(range(number_of_steps)):
        if np.random.random() < mutation:

            idx = np.random.randint(N, size=1)
            population[idx, :] = np.random.random((1, 3))

        else:
            res, mut = np.random.randint(0, N, 2)

            if res != mut:
                if payoff_type == "expected":
                    res_payoff, mut_payoff = payoffsExpected(
                        res, mut, population, payoffs, N, delta
                    )

                if payoff_type == "stochastic":
                    res_payoff, mut_payoff = payoffsLastRound(
                        res, mut, population, payoffs, N, delta
                    )

                fermi = 1 / (1 + np.exp(-beta * (mut_payoff - res_payoff)))
                if np.random.random() < fermi:

                    population[res, :] = population[mut, :]
    print("--- %s seconds ---" % (time.time() - start_time))