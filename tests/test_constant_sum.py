"""Implements the unitary test for ConstantSum rule."""


import logging as lg
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(1, '../src')
from COIM.constraints import ConstantSum
from COIM.operator import ConstrainOperator

lg.getLogger().setLevel(lg.DEBUG)


def test_constant_sum(verbose=False):
    """
    Test the usage of the ConstantSum constraint.

    Args:
        verbose (bool): Whether or not the test should be verbose
    """
    precision = os.environ.get("PRECISION", 10)
    lg.info("test_constant_sum tests a 100 rows, 3 columns DataFrame where a0+a1+2*a2=1")
    df = np.random.uniform(low=.25, high=.38, size=(2, 100))
    df = pd.DataFrame(df.T, columns=["a0", "a1"])
    df["a2"] = (1 - df["a0"] - df["a1"]) / 2
    if verbose:
        print("Orginal dataset")
        print(df.head())

    operator = ConstrainOperator()
    constraint_constant_sum = ConstantSum(
        variables=["a0", "a1", "a2"],
        reference_variable="a0",
        constant_sum=1,
        weights=[1, 1, 2],
        labels=["new_a1", "new_a2"],
    )
    operator.add_rule(constraint_constant_sum)

    new_df = operator.encode_dataframe(df)
    if verbose:
        print("Encoded dataset")
        print(new_df.head())

    errors = pd.DataFrame([[0.0005, 0.0003]], columns=["new_a1", "new_a2"])
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
    test_constant_sum(True)
