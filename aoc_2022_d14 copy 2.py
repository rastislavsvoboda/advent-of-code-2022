from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('14.ex1').readlines()
lines_puzzle = open('14.in').readlines()


def print_g(G):
    for r in range(0, 11+1):
        for c in range(480, 520+1):
            if (r, c) in G.keys():
                print(G[(r, c)], end='')
            else:
                print('.', end='')
        print()


def move2(G, s, R):
    r, c = s

    if (r, c) == (0, 500):
        x0 = G.get((0, 500), ".")
        if x0 == "o":
            return None, None, True

    x = G.get((r+1, c), ".")
    if x == ".":
        return move(G, (r+1, c), R)
    xx = G.get((r+1, c-1), ".")
    if xx == ".":
        return move(G, (r+1, c-1), R)
    xxx = G.get((r+1, c+1), ".")
    if xxx == ".":
        return move(G, (r+1, c+1), R)
    G[(r, c)] = "o"
    return ((0, 500), False, False)


def move1(G, s, R):
    r, c = s
    if r > R:
        return None, None, True
    x = G.get((r+1, c), ".")
    if x == ".":
        return move(G, (r+1, c), R)
    xx = G.get((r+1, c-1), ".")
    if xx == ".":
        return move(G, (r+1, c-1), R)
    xxx = G.get((r+1, c+1), ".")
    if xxx == ".":
        return move(G, (r+1, c+1), R)
    G[(r, c)] = "o"
    return ((0, 500), False, False)


def solve1(lines):
    res = 0

    G = {}

    R = 0
    for line in lines:
        line = line.strip()
        words = line.split("->")
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line)]
        for i in range(len(words)-1):
            s_p = [int(n) for n in re.findall(r"[+-]?\d+", words[i+0])]
            e_p = [int(n) for n in re.findall(r"[+-]?\d+", words[i+1])]

            if s_p[0] == e_p[0]:
                c = s_p[0]
                if s_p[1] > e_p[1]:
                    s_p[1], e_p[1] = e_p[1], s_p[1]

                for r in range(s_p[1], e_p[1]+1):
                    G[(r, c)] = "#"
            elif s_p[1] == e_p[1]:
                r = s_p[1]
                if s_p[0] > e_p[0]:
                    s_p[0], e_p[0] = e_p[0], s_p[0]
                for c in range(s_p[0], e_p[0]+1):
                    G[(r, c)] = "#"
            else:
                assert False
            R = max(R, max(s_p[1], e_p[1]))

    for c in range(-1000, 1000+1):
        G[(R+2), c] = "#"

    finished = False
    while not finished:
        s = (0, 500)
        while True:
            s, moved, finished = move(G, s, R)
            if not moved:
                # print_g(G)
                break
            print()

    for v in G.values():
        if v == "o":
            res += 1

    return res
def solve1(lines):
    res = 0

    G = {}

    R = 0
    for line in lines:
        line = line.strip()
        words = line.split("->")
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line)]
        for i in range(len(words)-1):
            s_p = [int(n) for n in re.findall(r"[+-]?\d+", words[i+0])]
            e_p = [int(n) for n in re.findall(r"[+-]?\d+", words[i+1])]

            if s_p[0] == e_p[0]:
                c = s_p[0]
                if s_p[1] > e_p[1]:
                    s_p[1], e_p[1] = e_p[1], s_p[1]

                for r in range(s_p[1], e_p[1]+1):
                    G[(r, c)] = "#"
            elif s_p[1] == e_p[1]:
                r = s_p[1]
                if s_p[0] > e_p[0]:
                    s_p[0], e_p[0] = e_p[0], s_p[0]
                for c in range(s_p[0], e_p[0]+1):
                    G[(r, c)] = "#"
            else:
                assert False
            R = max(R, max(s_p[1], e_p[1]))

    for c in range(-1000, 1000+1):
        G[(R+2), c] = "#"

    finished = False
    while not finished:
        s = (0, 500)
        while True:
            s, moved, finished = move(G, s, R)
            if not moved:
                # print_g(G)
                break
            print()

    for v in G.values():
        if v == "o":
            res += 1

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 24
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 897
print(CRED + "sample:", solve1(lines_sample), CEND)  # 93
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 26683
# print(solve1_t(text))  #
# print(solve2(lines))  #

stop = datetime.now()
print("duration:", stop - start)
