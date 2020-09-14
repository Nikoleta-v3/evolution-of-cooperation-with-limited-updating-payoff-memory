from importlib.machinery import SourceFileLoader

import numpy as np
import pandas as pd
import sympy as sym

simulation = SourceFileLoader("simulation", "src/simulation.py").load_module()


def test_donation_game():
    c, b = sym.symbols("c, b")
    assert (b - c, -c, b, 0) == simulation.donation_game(c, b)
    assert (2, -1, 3, 0) == simulation.donation_game(1, 3)


def test_reshape_data():
    df = pd.DataFrame(np.random.random(size=(10, 3)), columns=list("ypq"))

    ps, qs = simulation._reshape_data(df)

    assert type(ps) == tuple
    assert type(qs) == tuple
    assert len(qs) <= 10
    assert len(ps) <= 10
