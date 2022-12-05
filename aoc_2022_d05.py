from datetime import datetime
import re

start = datetime.now()
lines = open('5-modified.in').readlines()
# lines = open('5-modified.ex1').readlines()

# modified contains just moves
# stack are manually parsed to strings


#             [M] [S] [S]
#         [M] [N] [L] [T] [Q]
# [G]     [P] [C] [F] [G] [T]
# [B]     [J] [D] [P] [V] [F] [F]
# [D]     [D] [G] [C] [Z] [H] [B] [G]
# [C] [G] [Q] [L] [N] [D] [M] [D] [Q]
# [P] [V] [S] [S] [B] [B] [Z] [M] [C]
# [R] [H] [N] [P] [J] [Q] [B] [C] [F]
#  1   2   3   4   5   6   7   8   9


STACKS = [
    "RPCDBG",
    "HVG",
    "NSQDJPM",
    "PSLGDCNM",
    "JBNCPFLS",
    "QBDZVGTS",
    "BZMHFTQ",
    "CMDBF",
    "FCQG"
]

# SAMPLE:

#     [D]
# [N] [C]
# [Z] [M] [P]
#  1   2   3

# STACKS = [
#     "ZN",
#     "MCD",
#     "P"
# ]

S1 = []
S2 = []

for i in range(len(STACKS)):
    S1.append(list(STACKS[i]))
    S2.append(list(STACKS[i]))


def move1(c, f, t):
    for i in range(c):
        S1[t-1].append(S1[f-1].pop())


def move2(c, f, t):
    X = []
    for i in range(c):
        X.append(S2[f-1].pop())

    for i in range(c):
        S2[t-1].append(X.pop())


def solve(lines, part):
    for line in lines:
        line = line.strip()
        nums = re.findall(r"\d+", line)
        N = [int(x) for x in nums]
        # count, from, to
        c, f, t = N
        if part == 1:
            move1(c, f, t)
        else:
            move2(c, f, t)

    if part == 1:
        S = S1
    else:
        S = S2
    
    res = []
    for s in S:
        res.append(list(s)[-1])

    return "".join(res)


print(solve(lines, 1))  # TLNGFGMFN
print(solve(lines, 2))  # FGLQJCMBD

stop = datetime.now()
print("duration:", stop - start)
