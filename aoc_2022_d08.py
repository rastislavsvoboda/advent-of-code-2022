from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('8.ex1').readlines()
lines_puzzle = open('8.in').readlines()


def is_visible(D, r, c):
    R = len(D)
    C = len(D[0])
    tree = D[r][c]
    if r == 0 or r == R-1:
        return True
    if c == 0 or c == C-1:
        return True

    not_v = 0
    for i in range(0, r):
        if D[i][c] >= tree:
            not_v += 1
            break

    for i in range(r+1, R):
        if D[i][c] >= tree:
            not_v += 1
            break

    for i in range(0, c):
        if D[r][i] >= tree:
            not_v += 1
            break

    for i in range(c+1, C):
        if D[r][i] >= tree:
            not_v += 1
            break

    return not_v < 4


def score(D, r, c):
    R = len(D)
    C = len(D[0])
    tree = D[r][c]
    if r == 0 or r == R-1:
        return 0
    if c == 0 or c == C-1:
        return 0

    up = 1
    rr = r-1
    while rr > 0 and tree > D[rr][c]:
        rr -= 1
        up += 1

    down = 1
    rr = r+1
    while rr < R-1 and tree > D[rr][c]:
        rr += 1
        down += 1

    left = 1
    cc = c-1
    while cc > 0 and tree > D[r][cc]:
        cc -= 1
        left += 1

    right = 1
    cc = c+1
    while cc < C-1 and tree > D[r][cc]:
        cc += 1
        right += 1

    return up * left * down * right


def solve1(lines):
    D = []
    for line in lines:
        D.append([int(n) for n in line.strip()])

    # print(D)
    R = len(D)
    C = len(D[0])

    res1 = 0
    res2 = 0
    for r in range(R):
        for c in range(C):
            vis = is_visible(D, r, c)
            # print(D[r][c], vis)
            if vis:
                res1 += 1

            sco = score(D, r, c)
            if sco > res2:
                res2 = sco

    return res1, res2


print(CRED + "sample:", solve1(lines_sample), CEND)  # 21, 8
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 1812, 315495

stop = datetime.now()
print("duration:", stop - start)
