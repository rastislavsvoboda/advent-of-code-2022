from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('4.in').read()
text_sample = open('4.ex1').read()


def is_range_contained(i1s, i1e, i2s, i2e):
    return i1s <= i2s and i2e <= i1e


def is_range_overlapped(i1s, i1e, i2s, i2e):
    os = max(i1s, i2s)
    oe = min(i1e, i2e)
    return os <= oe


def solve1(text):
    res = 0
    for line in text.split("\n"):
        i1s, i1e, i2s, i2e = get_all_nums(line.replace("-", ","))
        if is_range_contained(i1s, i1e, i2s, i2e) or is_range_contained(i2s, i2e, i1s, i1e):
            res += 1

    return res


def solve2(text):
    res = 0
    for line in text.split("\n"):
        i1s, i1e, i2s, i2e = get_all_nums(line.replace("-", ","))
        if is_range_overlapped(i1s, i1e, i2s, i2e):
            res += 1

    return res


print(CRED + "sample:", solve1(text_sample), CEND)  # 2
print(CGRN + "puzzle:", solve1(text_puzzle), CEND)  # 487

print(CRED + "sample:", solve2(text_sample), CEND)  # 4
print(CGRN + "puzzle:", solve2(text_puzzle), CEND)  # 849

stop = datetime.now()
print("duration:", stop - start)
