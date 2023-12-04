"""
Module for dummy functions to test graph things with.
"""


def A(b: int, c: int) -> int:
    """Function that should become part of the graph - A"""
    return b + c * c


def B(A: int) -> int:
    """Function that should become part of the graph - B"""
    return A * A


def C(D: int):  # empty string doc on purpose.
    return D * 2
