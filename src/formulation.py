import numpy as np
import sympy as sym


def expected_distribution_opening_round(player, opponent):
    """
    Returns


    the first state of two strategies given that they are written as vectors and the first element
    is the probability of cooperating in the opening move.

    For example:
    s_1 = (y_1, p_1, q_1)

    or

    s_1 = (y_1, p_1, p_2, p_3, p_4)
    """

    cc_probability = player[0] * opponent[0]
    cd_probability = player[0] * (1 - opponent[0])
    dc_probability = (1 - player[0]) * opponent[0]
    dd_probability = (1 - player[0]) * (1 - opponent[0])

    return (cc_probability, cd_probability, dc_probability, dd_probability)


def markov_chain_for_reactive_strategies(player, opponent):
    """
    Returns a Markov transition matrix for a game of reactive strategies.
    """
    return np.array(
        [
            [
                player[1] * opponent[1],
                player[1] * (1 - opponent[1]),
                opponent[1] * (1 - player[1]),
                (1 - player[1]) * (1 - opponent[1]),
            ],
            [
                opponent[1] * player[2],
                player[2] * (1 - opponent[1]),
                opponent[1] * (1 - player[2]),
                (1 - opponent[1]) * (1 - player[2]),
            ],
            [
                player[1] * opponent[2],
                player[1] * (1 - opponent[2]),
                opponent[2] * (1 - player[1]),
                (1 - player[1]) * (1 - opponent[2]),
            ],
            [
                player[2] * opponent[2],
                player[2] * (1 - opponent[2]),
                opponent[2] * (1 - player[2]),
                (1 - player[2]) * (1 - opponent[2]),
            ],
        ],
    )


def probability_being_in_state_R(player, opponent, delta):

    r_1 = player[1] - player[2]
    r_2 = opponent[1] - opponent[2]

    first_term = (1 - delta) * (
        (player[0] * opponent[0]) / (1 - delta ** 2 * r_1 * r_2)
    )

    second_term_numerator = (
        player[2] + r_1 * ((1 - delta) * opponent[0] + delta * opponent[2])
    ) * (opponent[2] + r_2 * ((1 - delta) * player[0] + delta * player[2]))
    second_term_denominator = (1 - delta * r_1 * r_2) * (
        1 - delta ** 2 * r_1 * r_2
    )

    return first_term + delta * (
        second_term_numerator / second_term_denominator
    )


def probability_being_in_state_S(player, opponent, delta):

    r_1 = player[1] - player[2]
    r_2 = opponent[1] - opponent[2]

    first_term = (1 - delta) * (
        (player[0] * (1 - opponent[0])) / (1 - delta ** 2 * r_1 * r_2)
    )

    second_term_numerator = (
        player[2] + r_1 * ((1 - delta) * opponent[0] + delta * opponent[2])
    ) * (
        (1 - opponent[2])
        + (-r_2) * ((1 - delta) * player[0] + delta * player[1])
    )
    second_term_denominator = (1 - delta * r_1 * r_2) * (
        1 - delta ** 2 * r_1 * r_2
    )

    return first_term + delta * (
        second_term_numerator / second_term_denominator
    )


def probability_being_in_state_T(player, opponent, delta):

    r_1 = player[1] - player[2]
    r_2 = opponent[1] - opponent[2]

    first_term = (1 - delta) * (
        ((1 - player[0]) * opponent[0]) / (1 - delta ** 2 * r_1 * r_2)
    )

    second_term_numerator = (
        (1 - player[2])
        + (-r_1) * ((1 - delta) * opponent[0] + delta * opponent[1])
    ) * (opponent[2] + r_2 * ((1 - delta) * player[0] + delta * player[2]))
    second_term_denominator = (1 - delta * r_1 * r_2) * (
        1 - delta ** 2 * r_1 * r_2
    )

    return first_term + delta * (
        second_term_numerator / second_term_denominator
    )


def probability_being_in_state_P(player, opponent, delta):

    r_1 = player[1] - player[2]
    r_2 = opponent[1] - opponent[2]

    first_term = (1 - delta) * (
        ((1 - player[0]) * (1 - opponent[0])) / (1 - delta ** 2 * r_1 * r_2)
    )

    second_term_numerator = (
        (1 - player[2])
        + (-r_1) * ((1 - delta) * opponent[0] + delta * opponent[1])
    ) * (
        (1 - opponent[2])
        + (-r_2) * ((1 - delta) * player[0] + delta * player[1])
    )
    second_term_denominator = (1 - delta * r_1 * r_2) * (
        1 - delta ** 2 * r_1 * r_2
    )

    return first_term + delta * (
        second_term_numerator / second_term_denominator
    )


def probability_of_receiving_payoffs(
    player, opponent, player_state, opponent_state, N, k, delta
):

    if (player_state, opponent_state) in [
        (probability_being_in_state_R, probability_being_in_state_R),
        (probability_being_in_state_T, probability_being_in_state_S),
        (probability_being_in_state_S, probability_being_in_state_T),
        (probability_being_in_state_P, probability_being_in_state_P),
    ]:
        first_term = (1 / (N - 1)) * player_state(player, opponent, delta)
    else:
        first_term = 0

    second_term_case_one = (
        ((k - 1) / (N - 2))
        * ((k - 2) / (N - 3))
        * player_state(player, opponent, delta)
        * opponent_state(opponent, opponent, delta)
    )
    second_term_case_two = (
        ((k - 1) / (N - 2))
        * ((N - k - 1) / (N - 3))
        * player_state(player, opponent, delta)
        * opponent_state(opponent, player, delta)
    )
    second_term_case_three = (
        ((N - k - 1) / (N - 2))
        * ((k - 1) / (N - 3))
        * player_state(player, player, delta)
        * opponent_state(opponent, opponent, delta)
    )
    second_term_case_four = (
        ((N - k - 1) / (N - 2))
        * ((N - k - 2) / (N - 3))
        * player_state(player, player, delta)
        * opponent_state(opponent, player, delta)
    )

    return first_term + (1 - 1 / (N - 1)) * (
        second_term_case_one
        + second_term_case_two
        + second_term_case_three
        + second_term_case_four
    )
