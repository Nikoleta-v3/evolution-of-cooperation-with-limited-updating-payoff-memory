import numpy as np


def expected_distribution_opening_round(player, opponent):
    """
    Returns


    the first state of two staregies gven that they are written as vectors and the first element
    is the probability of cooperating in the oppening move.

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
