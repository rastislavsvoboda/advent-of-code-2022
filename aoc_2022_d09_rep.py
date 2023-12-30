from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('9.in').read()
text_sample1 = open('9.ex1').read()
text_sample2 = open('9.ex2').read()

D = {"U": (-1, 0), "R": (0, 1), "D": (1, 0), "L": (0, -1)}


def follow(prev_node, curr_node):
    r, c = prev_node
    rr, cc = curr_node
    dr = r - rr
    dc = c - cc
    if abs(dr) > 1 or abs(dc) > 1:
        cc += sign(dc)
        rr += sign(dr)
    return (rr, cc)


def move(d, cnt, n, L):
    positions = set()
    for i in range(cnt):
        # move head
        r, c = L[0]
        dr, dc = D[d]
        r += dr
        c += dc
        L[0] = (r, c)
        # follow all tails
        for j in range(1, n + 1):
            prev_node = L[j - 1]
            curr_node = L[j]
            new_pos = follow(prev_node, curr_node)
            L[j] = new_pos
            if j == n:
                # store new_pos of last tail
                positions.add(new_pos)
    return positions


def solve(text, part):
    n = 1 if part == 1 else 9

    positions = set()
    st = (0, 0)
    L = {}
    for i in range(n + 1):
        L[i] = st

    positions.add(st)

    for line in text.split("\n"):
        dir_, cnt = line.split()
        cnt = int(cnt)
        visited = move(dir_, cnt, n, L)
        positions = positions.union(visited)

    res = len(positions)

    return res


print(CRED + "sample:", solve(text_sample1, 1), CEND)  # 13
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 6236

print(CRED + "sample:", solve(text_sample2, 2), CEND)  # 36
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 2449

stop = datetime.now()
print("duration:", stop - start)
