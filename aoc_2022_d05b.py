from datetime import datetime
from collections import defaultdict, deque, Counter
import re
import copy

start = datetime.now()
lines = open('5.in').readlines()
# lines = open('5.ex1').readlines()


#             [M] [S] [S]
#         [M] [N] [L] [T] [Q]
# [G]     [P] [C] [F] [G] [T]
# [B]     [J] [D] [P] [V] [F] [F]
# [D]     [D] [G] [C] [Z] [H] [B] [G]
# [C] [G] [Q] [L] [N] [D] [M] [D] [Q]
# [P] [V] [S] [S] [B] [B] [Z] [M] [C]
# [R] [H] [N] [P] [J] [Q] [B] [C] [F]
#  1   2   3   4   5   6   7   8   9


STACKS = defaultdict(list)

i = 0
while True:
    line = lines[i]
    i += 1
    if '[' not in line:
        break
    for x in range(1, len(line), 4):
        c = line[x]
        if c == ' ':
            continue
        STACKS[int((x//4) + 1)].insert(0, c)

# print(STACKS)

# entry is [count, from, to]
COMMANDS = []

# skip empty line
i += 1

while i < len(lines):
    line = lines[i]
    if line == '':
        break
    COMMANDS.append([int(x) for x in re.findall(r"\d+", line)])
    i += 1

# print(COMMANDS)

S1 = copy.deepcopy(STACKS)
S2 = copy.deepcopy(STACKS)


def move1(s, c, f, t):
    x = s[f][-c:]
    s[f] = s[f][:-c]
    s[t] = s[t] + list(reversed(x))


def move2(s, c, f, t):
    x = s[f][-c:]
    s[f] = s[f][:-c]
    s[t] = s[t] + x


def solve(stack, commands, move):
    for cmd in commands:
        count_, from_, to_ = cmd
        move(stack, count_, from_, to_)

    res = []

    for k in list(sorted(stack.keys())):
        res.append(stack[k][-1])

    return "".join(res)


print(solve(S1, COMMANDS, move1))  # TLNGFGMFN
print(solve(S2, COMMANDS, move2))  # FGLQJCMBD

stop = datetime.now()
print("duration:", stop - start)
