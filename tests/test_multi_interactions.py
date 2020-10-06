from importlib.machinery import SourceFileLoader

import numpy as np

mutli = SourceFileLoader("mutli", "src/multi_interactions.py").load_module()


def test_introduce_mutant():
    N = 10
    resident = (1, 1, 1)
    population = {resident: N}
    random_ = np.random.RandomState(0)

    mutant, population = mutli.introduce_mutant(population, resident, random_)
    expected_mutant = [
        0.5488135039273248,
        0.7151893663724195,
        0.6027633760716439,
    ]

    assert len(population) == 2
    assert population[resident] == 9
    assert set(expected_mutant) == set(mutant)
    assert population[mutant] == 1


# def test_get_score_for_last_n_rounds():
