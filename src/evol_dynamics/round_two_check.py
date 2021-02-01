import evol_dynamics

import numpy as np

import axelrod as axl
from collections import Counter

import tqdm

import sys


def steady_state_for_16_states(player, opponent, delta):
    """
    The probability of being at each state in steady state.
    """
    v_zero = np.array(
        evol_dynamics.expected_distribution_opening_round(player, opponent)
    )
    M = evol_dynamics.markov_chain_for_reactive_strategies(player, opponent)
    rhs = np.dot(v_zero, np.linalg.pinv((np.eye(4) - delta * M)))

    ss = []
    for i, row in enumerate(M):
        for m in row:
            ss.append((1 - delta) * m * (delta ** 2) * rhs[i])

    return np.array(ss)


def simulated_states(
    player, opponent, delta, number_of_repetitions, rounds_of_history
):
    history_to_state = {
        "CCCC": "RR",
        "CCCD": "RS",
        "CCDC": "RT",
        "CCDD": "RP",
        "CDCC": "SR",
        "CDCD": "SS",
        "CDDC": "ST",
        "CDDD": "SP",
        "DCCC": "TR",
        "DCCD": "TS",
        "DCDC": "TT",
        "DCDD": "TP",
        "DDCC": "PR",
        "DDCD": "PS",
        "DDDC": "PT",
        "DDDD": "PP",
    }
    ss = []
    for _ in range(number_of_repetitions):

        match = axl.Match(
            [
                evol_dynamics.ReactivePlayer(player, role="mutant"),
                evol_dynamics.ReactivePlayer(opponent, role="resident"),
            ],
            prob_end=(1 - delta),
        )
        _ = match.play()

        histories = match.result[-rounds_of_history:]
        histories_in_characters = "".join(
            [str(v) for history in histories for v in history]
        )
        try:
            ss.append(history_to_state[histories_in_characters])
        except KeyError:
            pass

        states = {name: 0 for name in history_to_state.values()}
        for key, value in zip(Counter(ss).keys(), Counter(ss).values()):
            states[key] = value / number_of_repetitions

    return states


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

        v = steady_state_for_16_states(mutant, resident, delta)
        v_simulated = simulated_states(
            mutant, resident, delta, number_of_repetitions, rounds_of_history=2
        )

        data = [
            i,
            number_of_repetitions,
            *mutant,
            *resident,
            delta,
            *v,
            *v_simulated.values(),
        ]

        with open(filename, "a") as textfile:
            textfile.write(",".join([str(elem) for elem in data]) + "\n")
        textfile.close()
