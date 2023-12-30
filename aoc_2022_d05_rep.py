from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('5.in').read()
text_sample = open('5.ex1').read()


def move1(cnt, src, dst, C):
    for _ in range(cnt):
        x = C[src - 1].pop()
        C[dst - 1].append(x)


def move2(cnt, src, dst, C):
    temp = []

    for _ in range(cnt):
        x = C[src - 1].pop()
        temp.append(x)

    for _ in range(cnt):
        x = temp.pop()
        C[dst - 1].append(x)


def solve(text, part):
    setup, instrs = text.split("\n\n")
    setup = setup.split("\n")
    # last row are crane id's
    ids = get_all_nums(setup[-1])
    N = max(ids)
    assert len(ids) == N

    C = [[] for _ in range(N)]
    data = setup[:-1][::-1]

    for line in data:
        indx = 0
        for i in range(1, 4 * N, 4):
            if line[i] != " ":
                c = line[i]
                assert c.isupper()
                C[indx].append(c)
            indx += 1

    move = move1 if part == 1 else move2

    for instr in instrs.split("\n"):
        cnt, src, dst = get_all_nums(instr)
        move(cnt, src, dst, C)

    res = ""
    for c in C:
        res += c.pop()

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # CMZ
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # TLNGFGMFN

print(CRED + "sample:", solve(text_sample, 2), CEND)  # MCD
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # FGLQJCMBD

stop = datetime.now()
print("duration:", stop - start)
