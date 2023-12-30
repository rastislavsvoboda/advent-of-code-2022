from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('6.in').read()
text_sample = open('6.ex1').read()


def solve(text, part):
    n = 4 if part == 1 else 14

    line = text.strip()
    for i in range(len(line) - n):
        if len(set(line[i:i + n])) == n:
            return i + n

    return None


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 7
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 1109

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 19
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 3965

stop = datetime.now()
print("duration:", stop - start)
