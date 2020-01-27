"""Behold the group M,

A Mesoamerican notation for writing integers in base 20 with an 18 in the
third position, where 20^3 would go.
"""

from collections import OrderedDict, namedtuple
from functools import reduce
from operator import imul

import numpy as np

days_to_names = OrderedDict({
    1: "K'in",
    20: 'Winal',   # 2^2 * 5
    360: 'Tun',  # 2^3 * 3^2 * 5, 18 * 20, 6 * 60, 30 * 12
    7_300: "K'atun",
    144_000: "B'ak'tun",
    2_880_000: 'Piktun',
    576_000_000: 'Kalabtun',
    1_152_000_000: "K'inchiltun",
    23_040_000_000: 'Alautun',
})

names = list(days_to_names.values())

long_count = [1, 20, 18] + [20] * 6

# Because m is odd, -x == -to_integer(x) for all x in M.
m = len(long_count)

ticks = [reduce(imul, long_count[:i]) for i in range(1, m + 1)]

numbers = [
    np.array([0] * i + [1] + [0] * (m - i - 1))
    for i in range(m)
]

names_to_days = OrderedDict(zip(ticks, names))


zero = np.zeros(m, dtype='i')

unity = np.array([1] + [0] * (m - 1))

example = np.array([1] * m)


# M is countably infinite.
def to_integer(n):
    """Convert number to an integer.

    >>> to_integer(zero)
    0

    >>> to_integer(unity)
    1

    >>> to_integer(np.array([0, 0, 0, 0, 0, 0, 0, 0, 1]))
    23040000000

    >>> to_integer(np.array([0, 0, 1, 0, 0, 0, 0, 0, 0]))
    360
    """
    return sum(n * ticks)


def shift(a):
    """Shift up, increasing the number's magnitude.

    >>> to_integer(shift(unity))
    20

    >>> to_integer(shift(np.array([0, 0, 1, 0, 0, 0, 0, 0, 0])))
    7200
    """
    return np.append([0], a[:-1])


def increment(a):
    """Add one to a number.

    >>> to_integer(increment(unity))
    2

    >>> to_integer(increment(np.array([0, 0, 1, 0, 0, 0, 0, 0, 0])))
    361

    >>> to_integer(increment(np.array([0, 0, 0, 0, 0, 0, 0, 0, 1])))
    23040000001
    """
    a = a + unity
    ticks_ = ticks[1:] + [a[-1] + 1]
    while (a // ticks_ > zero).any():
        a = shift(a // ticks_) + (a % ticks_)
    return a


def add(a, b):
    """Adds to numbers."""


def repeat(f, n, x):
    """Apply the function f to x, n times."""
    while n:
        x = f(x)
        n -= 1
    return x
