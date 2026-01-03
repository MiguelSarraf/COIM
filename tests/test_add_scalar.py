"""Implements the unitary test for AddScalar rule."""


import logging as lg
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(1, '../src')
from COIM.constraints import AddScalar
from COIM.operator import ConstrainOperator

lg.getLogger().setLevel(lg.DEBUG)


def test_add_scalar(verbose=False):
    """
    Test the usage of the AddScalar constraint.

    Args:
        verbose (bool): Whether or not the test should be verbose
    """
    precision = os.environ.get("PRECISION", 10)
    lg.info("test_add_scalar tests a 100 rows, 2 columns DataFrame where b=a+10")
    df = np.random.uniform(low=0, high=10, size=(1, 100)).astype("int")
    df = pd.DataFrame(df.T, columns=["a"])
    df["b"] = df["a"] + 10
    if verbose:
        print("Orginal dataset")
        print(df.head())

    operator = ConstrainOperator()
    constraint_add_scalar = AddScalar(base_variable="a", target_variable="b", constant=10)
    operator.add_rule(constraint_add_scalar)

    new_df = operator.encode_dataframe(df)
    if verbose:
        print("Encoded dataset")
        print(new_df.head())

    errors = pd.DataFrame([[0.0005]], columns=["a"])
    if verbose:
        print("Errors")
        print(errors.head())

    new_df, errors = operator.decode_dataframe(new_df, errors)
    if verbose:
        print("Decoded dataset")
        print(new_df.head())
        print("Decoded errors")
        print(errors.head())

    if verbose:
        operator.summary()

    df = df.round(precision)
    new_df = new_df.round(precision)

    diff = df.compare(new_df)
    if len(diff) > 0:
        lg.error("Decoded DataFrame does not match original one.")
        lg.debug(diff.head())

    assert len(diff) == 0


if __name__ == "__main__":
    test_add_scalar(True)
