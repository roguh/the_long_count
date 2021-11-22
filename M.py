"""Behold, the group M.

A Mesoamerican notation for writing integers in base 20 with an 18 in the
third position, where 20^3 would go.
"""

from collections import OrderedDict, namedtuple
from functools import reduce
from operator import imul

import numpy as np

days_to_names = OrderedDict(
    {
        1: "K'in",
        20: "Winal",  # 2^2 * 5
        360: "Tun",  # 2^3 * 3^2 * 5, 18 * 20, 6 * 60, 30 * 12
        7_300: "K'atun",
        144_000: "B'ak'tun",
        2_880_000: "Piktun",
        576_000_000: "Kalabtun",
        1_152_000_000: "K'inchiltun",
        23_040_000_000: "Alautun",
    }
)

names = list(days_to_names.values())

long_count = [1, 20, 18] + [20] * 6

# Because m is odd, -x == -to_integer(x) for all x in M.
m = len(long_count)

ticks = [reduce(imul, long_count[:i]) for i in range(1, m + 1)]

numbers = [np.array([0] * i + [1] + [0] * (m - i - 1)) for i in range(m)]

names_to_days = OrderedDict(zip(ticks, names))


zero = np.zeros(m, dtype="int64")

unity = np.array([1] + [0] * (m - 1))

examples = np.diag([1] * m)

for a in [zero, unity, examples]:
    a.flags.writeable = False


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


def from_integer(n):
    """Convert n to a number.

    >>> to_integer(from_integer(1)) == 1
    True

    >>> to_integer(from_integer(1441)) == 1441
    True

    >>> to_integer(from_integer(7431232)) == 7431232
    True
    """
    x = np.array(zero)
    d = 0
    for i in range(len(x)):
        if i == len(x) - 1:
            x[i] = n % ticks[-1]
        else:
            d = n % ticks[i + 1]
            x[i] = d // ticks[i]
            n -= d
    return x


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
    ticks_ = [20] + ticks[1:]
    while (a // ticks_ > zero).any():
        a = shift(a // ticks_) + (a % ticks_)
    return a


def add(a, b):
    """Add to numbers.

    >>> to_integer(add(unity, unity))
    2

    >>> to_integer(add(from_integer(41539832), from_integer(154124))) == 41539832 + 154124
    True
    """
    carry = 0
    c = np.array(zero)
    ticks_ = ticks[1:] + [ticks[-1] + 1]
    for i, (ai, bi) in enumerate(zip(a, b)):
        s = ai + bi + carry
        carry = s // ticks_[i]
        c[i] = s % ticks_[i]
    return c


def repeat(f, n, x):
    """Apply the function f to x, n times.

    >>> to_integer(repeat(increment, 21, unity))
    22
    """
    while n:
        x = f(x)
        n -= 1
    return x
