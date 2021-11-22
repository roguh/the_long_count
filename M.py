"""Behold, the group M.

A Mesoamerican notation for writing integers in base 20 with an 18 in the
third position, where 20^3 would go.
"""

from collections import OrderedDict, namedtuple
from functools import reduce
from operator import imul

import numpy as np
import math

days_to_names = OrderedDict(
    {
        1: "K'in",
        20: "Winal",  # 2^2 * 5
        360: "Tun",  # 2^3 * 3^2 * 5, 18 * 20, 6 * 60, 30 * 12
        7_200: "K'atun",
        144_000: "B'ak'tun",
        2_880_000: "Piktun",
        57_600_000: "Kalabtun",
        1_152_000_000: "K'inchiltun",
        23_040_000_000: "Alautun",
    }
)

names = list(days_to_names.values())

long_count = [1, 20, 18] + [20] * 6

# Because m is odd, -x == -to_integer(x) for all x in M.
m = len(long_count)

# days = [reduce(imul, long_count[:i]) for i in range(1, m + 1)]
days = sorted(list(days_to_names.keys()))

# A number is represented as a numpy array with 9 elements.
powers_of_20ish = [np.array([0] * i + [1] + [0] * (m - i - 1)) for i in range(m)]

names_to_days = OrderedDict(zip(days, names))

zero = np.zeros(m, dtype="int64")

unity = np.array([1] + [0] * (m - 1))

examples = np.diag([1] * m)

for a in [zero, unity, examples]:
    a.flags.writeable = False


def log20(value):
    return math.log(value) / math.log(20)


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
    return sum(n * days)


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
            x[i] = n % days[-1]
        else:
            d = n % days[i + 1]
            x[i] = d // days[i]
            n -= d
    return x


def shift(a):
    """Shift up, increasing the number's magnitude by powers of 20 or 18.

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
    days_ = [20] + days[1:]
    while (a // days_ > zero).any():
        a = shift(a // days_) + (a % days_)
    return a


def add(a, b):
    """Add two long count numbers.

    >>> to_integer(add(unity, unity))
    2

    >>> to_integer(add(powers_of_20ish[1], powers_of_20ish[2]))
    380

    >>> to_integer(add(from_integer(122), from_integer(34))) == 122 + 34
    True

    >>> to_integer(add(from_integer(41539832), from_integer(154124))) == 41539832 + 154124
    True
    """
    carry = 0
    c = np.array(zero)
    days_ = days[1:] + [days[-1] + 1]
    for i, (ai, bi) in enumerate(zip(a, b)):
        s = ai + bi + carry
        carry = s // days_[i]
        c[i] = s % days_[i]
    return c


def repeat(f, n, x):
    """Apply the function f to x, n times.

    >>> to_integer(repeat(increment, 21, unity))
    22

    >>> to_integer(repeat(increment, 21, powers_of_20ish[3]))
    7221

    >>> to_integer(repeat(shift, 5, from_integer(222)))
    639360000
    """
    while n:
        x = f(x)
        n -= 1
    return x
