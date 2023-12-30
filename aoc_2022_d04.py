from datetime import datetime
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
lines_puzzle = open('4.in').readlines()
lines_sample = open('4.ex1').readlines()


def in_range(s1, e1, s2, e2):
    # s2-e2 in range of s1-e2
    return s1 <= s2 <= e1 and s1 <= e2 <= e1


def overlap(s1, e1, s2, e2):
    # s2-e2 overlap s1-e2
    return s1 <= s2 <= e1 or s1 <= e2 <= e1


def solve(lines):
    res1 = 0
    res2 = 0

    for line in lines:
        line = line.strip()
        nums = re.findall(r"\d+", line)
        N = [int(n) for n in nums]
        a, b, c, d = N
        # print(N)

        if in_range(a, b, c, d) or in_range(c, d, a, b):
            res1 += 1

        if overlap(a, b, c, d) or overlap(c, d, a, b):
            res2 += 1

    return res1, res2


print(CRED + "sample:", solve(lines_sample), CEND)  # 2, 4
print(CGRN + "puzzle:", solve(lines_puzzle), CEND)  # 487, 849


stop = datetime.now()
print("duration:", stop - start)
