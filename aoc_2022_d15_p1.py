from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('15.ex1').readlines()
lines_puzzle = open('15.in').readlines()


def manh(s, b):
    sx, sy = s
    bx, by = b
    return abs(sx-bx) + abs(sy-by)


def solve1(lines, rowY):
    res = 0
    Y = rowY
    G = {}
    S = []
    B = []
    D = []
    for line in lines:
        line = line.strip()
        words = line.split()
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line)]
        # print(nums)
        s = (nums[0], nums[1])
        b = (nums[2], nums[3])
        d = manh(s, b)
        # print(s,b,d)
        G[s] = "S"
        G[b] = "B"
        S.append(s)
        B.append(b)
        D.append(d)

    res = 0
    for xx in range(-10000000, 10000000):
        p = (xx, Y)
        for (i, s) in enumerate(S):
            if (p) not in G:
                d = manh(s, p)
                if d <= D[i]:
                    G[p] = "#"
                    res += 1

    return res


def solve2(lines, limit):
    res = 0

    G = {}
    S = []
    B = []
    D = []
    for line in lines:
        line = line.strip()
        words = line.split()
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line)]
        # print(nums)
        s = (nums[0], nums[1])
        b = (nums[2], nums[3])
        d = manh(s, b)
        # print(s,b,d)
        G[s] = "S"
        G[b] = "B"
        S.append(s)
        B.append(b)
        D.append(d)

    Y1 = 0
    Y2 = limit
    X1 = 0
    X2 = limit

    found = None
    for xx in range(X1, X2+1):
        for yy in range(Y1, Y2+1):
            p = (xx, yy)
            ff = True
            for (i, s) in enumerate(S):
                d = manh(s, p)
                if d <= D[i]:
                    ff = False
                    break
            if ff:
                found = p
                res = found[0] * 4000000 + found[1]
                return res
    return None


print(CRED + "sample:", solve1(lines_sample, 10), CEND)  # 26
print(CGRN + "puzzle:", solve1(lines_puzzle, 2000000), CEND)  # 5525990
print(CRED + "sample:", solve2(lines_sample, 20), CEND)  # 56000011
# print(CGRN + "puzzle:", solve2(lines_puzzle, 4000000), CEND)  #

stop = datetime.now()
print("duration:", stop - start)
