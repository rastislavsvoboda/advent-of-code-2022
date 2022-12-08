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

    up = True
    for i in range(0, r):
        if D[i][c] >= tree:
            up = False
            break

    down = True
    for i in range(r+1, R):
        if D[i][c] >= tree:
            down = False
            break

    left = True
    for i in range(0, c):
        if D[r][i] >= tree:
            left = False
            break

    right = True
    for i in range(c+1, C):
        if D[r][i] >= tree:
            right = False
            break

    return up or down or left or right


def score(D, r, c):
    R = len(D)
    C = len(D[0])
    tree = D[r][c]

    up = 0
    for rr in range(r-1, -1, -1):
        up += 1
        if tree <= D[rr][c]:
            break

    down = 0
    for rr in range(r+1, R):
        down += 1
        if tree <= D[rr][c]:
            break

    left = 0
    for cc in range(c-1, -1, -1):
        left += 1
        if tree <= D[r][cc]:
            break

    right = 0
    for cc in range(c+1, C):
        right += 1
        if tree <= D[r][cc]:
            break

    return up * down * left *  right


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
