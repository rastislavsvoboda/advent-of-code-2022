from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('1.in').read()
text_sample = open('1.ex1').read()


def solve1(text):
    C = [sum(map(int, g.split("\n"))) for g in text.split("\n\n")]
    return max(C)


def solve2(text):
    C = []
    for g in text.split("\n\n"):
        C.append(sum(map(int, g.split("\n"))))

    cals_sorted = list(sorted(C, reverse=True))
    return sum(cals_sorted[:3])


print(CRED + "sample:", solve1(text_sample), CEND)  # 24000
print(CGRN + "puzzle:", solve1(text_puzzle), CEND)  # 70509

print(CRED + "sample:", solve2(text_sample), CEND)  # 45000
print(CGRN + "puzzle:", solve2(text_puzzle), CEND)  # 208567

stop = datetime.now()
print("duration:", stop - start)
