from datetime import datetime
from aoc_tools import *
from functools import cmp_to_key

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('13.in').read()
text_sample = open('13.ex1').read()


def compare_nums(a, b):
    return -1 if a < b else 0 if a == b else 1


def compare(a, b):
    if type(a) == int and type(b) == int:
        return compare_nums(a, b)

    if type(a) == int and type(b) == list:
        return compare([a], b)

    if type(a) == list and type(b) == int:
        return compare(a, [b])

    for aa, bb in zip(a, b):
        r = compare(aa, bb)
        if r != 0:
            return r

    return compare_nums(len(a), len(b))


def solve(text, part):
    res = None

    PAIRS = []
    groups = text.split("\n\n")
    for group in groups:
        a, b = group.split("\n")
        PAIRS.append((eval(a), eval(b)))

    if part == 1:
        res = 0
        for i, (a, b) in enumerate(PAIRS):
            if compare(a, b) == -1:
                res += i + 1
    elif part == 2:
        LST = []
        for a, b in PAIRS:
            LST.append(a)
            LST.append(b)
        divider2 = [[2]]
        LST.append(divider2)
        divider6 = [[6]]
        LST.append(divider6)
        LST.sort(key=cmp_to_key(compare))
        i2 = LST.index(divider2) + 1
        i6 = LST.index(divider6) + 1
        res = i2 * i6

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 13
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 5393

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 140
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 26712

stop = datetime.now()
print("duration:", stop - start)
