from numpy import *
import time

import tqdm


def stationary_reactive(p1, p2, delta):
    M = array(
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

    v0 = array(
        [
            p1[0] * p2[0],
            p1[0] * (1 - p2[0]),
            (1 - p1[0]) * p2[0],
            (1 - p1[0]) * (1 - p2[0]),
        ]
    )

    return (1 - delta) * v0 @ linalg.inv((eye(4) - delta * M))


def payoffsLastRound(res, mut, population, u, N, delta):

    payoffs = zeros((2))

    indices = [res, mut]
    for i, me in enumerate(indices):
        id = random.choice(list(set(range(N)) - set(indices[:i])))
        v = stationary_reactive(population[me, :], population[id, :], delta)
        payoffs[i] = random.choice(u, p=v.round(15))

    return payoffs


def cooperation(population, delta, N):
    Mu, counts = unique(population, axis=0, return_counts=True)
    unique_rows = len(counts)
    coop = zeros(unique_rows)
    for i, me in enumerate(Mu):
        player_coop = zeros(unique_rows)
        for other in Mu:
            v = stationary_reactive(me, other, delta)
            player_coop[i] = v[0] + v[1]

        coop[i] = sum(player_coop * counts / sum(counts))
    return mean(coop)

if __name__ == "__main__":  # pragma: no cover

    N = 100
    delta = 0.999
    beta = 1
    mutation = 10 ** 0
    number_of_steps = 10 ** 4
    payoffs = array([2, -1, 3, 0])
    filename = "mutation_expected.csv"
    seed = 10
    starting_resident = (0, 0, 0)
    sdim = 3
    av_player = zeros((3))
    coop = 0
    start_time = time.time()

    population = starting_resident * ones((N, sdim))

    for t in tqdm.tqdm(range(number_of_steps)):

        if random.random() < mutation:
            idx = random.randint(N, size=1)
            population[idx, :] = random.random((1, 3))
        else:
            res, mut = random.randint(0, N, 2)

            if res != mut:

                if random.random() < 1 / N:

                    id = random.choice(
                        list(range(res)) + list(range(res + 1, N))
                    )
                    v = stationary_reactive(
                        population[res, :], population[mut, :], delta
                    )
                    res_payoff = random.choice(payoffs, p=v.round(15))
                    mut_payoff = array(
                        [payoffs[0], payoffs[2], payoffs[1], payoffs[3]]
                    )[res_payoff == payoffs]

                else:

                    res_payoff, mut_payoff = payoffsLastRound(
                        res, mut, population, payoffs, N, delta
                    )

                fermi = 1 / (1 + exp(-beta * (mut_payoff - res_payoff)))
                if random.random() < fermi:

                    population[res, :] = population[mut, :]

        # av_player += population.mean(0)
        coop += cooperation(population, delta, N)
        # savetxt(f"python/population_{t}.csv", population, delimiter=",")
    print("--- %s seconds ---" % (time.time() - start_time))
