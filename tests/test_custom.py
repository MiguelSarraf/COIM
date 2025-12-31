"""Implements the unitary test for Custom rule."""


import logging as lg
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(1, '../src')
from COIM.constraints import Custom
from COIM.operator import ConstrainOperator

lg.getLogger().setLevel(lg.DEBUG)
k = 3


def validate(df, variables, labels, precision, position):
    """
    Validate according to custom function.

    Args:
        df (pd.DataFrame): Refer to the base constraint module
        variables (list[str]): Refer to the base constraint module
        labels (list[str]): Refer to the base constraint module
        precision (float): Refer to the base constraint module
        position (int): Refer to the base constraint module

    Returns:
        df (pd.DataFrame): Refer to the base constraint module
    """
    df[labels[0]] = k * df[variables[0]]
    df_filter = df[df["nk"] - df["kn"] > precision]
    assert len(df_filter) == 0, f"Does not conform to rule {position}"
    df.drop(columns=labels[0], inplace=True)
    return df


def get_format(variables, labels):
    """
    Format according to custom function.

    Args:
        variables (list[str]): Refer to the base constraint module
        labels (list[str]): Refer to the base constraint module

    Returns:
        message (str): Refer to the base constraint module
    """
    return f"{labels[0]}={k}*{variables[0]}"


def encode(df, variables, labels):
    """
    Encode according to custom function.

    Args:
        df (pd.DataFrame): Refer to the base constraint module
        variables (list[str]): Refer to the base constraint module
        labels (list[str]): Refer to the base constraint module

    Returns:
        df (pd.DataFrame): Refer to the base constraint module
    """
    df.drop(columns=[variables[1]], inplace=True)
    return df


def decode(df, variables, labels, errors):
    """
    Decode according to custom function.

    Args:
        df (pd.DataFrame): Refer to the base constraint module
        variables (list[str]): Refer to the base constraint module
        labels (list[str]): Refer to the base constraint module
        errors (pd.DataFrame): Refer to the base constraint module

    Returns:
        df (pd.DataFrame): Refer to the base constraint module
        errors (pd.DataFrame): Refer to the base constraint module
    """
    df[labels[0]] = k * df[variables[0]]
    errors[labels[0]] = k * errors[variables[0]]
    return df, errors


def test_custom(verbose=False):
    """
    Test the usage of the Custom constraint.

    Args:
        verbose (bool): Whether or not the test should
    """
    precision = os.environ.get("PRECISION", 10)
    lg.info("test_custom tests a 100 rows, 2 columns DataFrame where nk=%d*n", k)
    df = np.random.uniform(low=0, high=10, size=(1, 100)).astype("int")
    df = pd.DataFrame(df.T, columns=["n"])
    df["nk"] = k * df["n"]
    if verbose:
        print("Orginal dataset")
        print(df.head())

    operator = ConstrainOperator()
    constraint_custom = Custom(["n", "nk"], validate, get_format, encode, decode, labels=["kn"])
    operator.add_rule(constraint_custom)

    new_df = operator.encode_dataframe(df)
    if verbose:
        print("Encoded dataset")
        print(new_df.head())

    errors = pd.DataFrame([[0.01]], columns=["n"])
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

    new_df.rename(columns={"kn": "nk"}, inplace=True)

    diff = df.compare(new_df)
    if len(diff) > 0:
        lg.error("Decoded DataFrame does not match original one.")
        lg.debug(diff.head())

    assert len(diff) == 0


if __name__ == "__main__":
    test_custom(True)
