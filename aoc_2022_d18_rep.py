from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('18.in').read()
text_sample = open('18.ex1').read()


def solve(text, part):
    C = set()
    D = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]

    for line in text.split("\n"):
        c = tuple(get_all_nums(line))
        C.add(c)

    if part == 1:
        res = 0
        for (x, y, z) in C:
            for (dx, dy, dz) in D:
                if not (x + dx, y + dy, z + dz) in C:
                    res += 1

    elif part == 2:
        res = 0
        min_x = min(x for (x, y, z) in C)
        max_x = max(x for (x, y, z) in C)
        min_y = min(y for (x, y, z) in C)
        max_y = max(y for (x, y, z) in C)
        min_z = min(z for (x, y, z) in C)
        max_z = max(z for (x, y, z) in C)

        RX = range(min_x - 1, max_x + 2)
        RY = range(min_y - 1, max_y + 2)
        RZ = range(min_z - 1, max_z + 2)

        # flood fill from outside
        SEEN = set()
        q = deque()
        q.append((min_x - 1, min_y - 1, min_z - 1))
        while len(q) > 0:
            c = q.popleft()
            x, y, z = c

            if not (x in RX and y in RY and z in RZ):
                continue

            if c in C or c in SEEN:
                continue

            SEEN.add(c)

            for (dx, dy, dz) in D:
                q.append((x + dx, y + dy, z + dz))

        # count how many of original cubes has neighbour that was seen during flood fill
        for (x, y, z) in C:
            for (dx, dy, dz) in D:
                if (x + dx, y + dy, z + dz) in SEEN:
                    res += 1


    return res

print(CRED + "sample:", solve(text_sample, 1), CEND)  # 64
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 4192

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 58
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 2520

stop = datetime.now()
print("duration:", stop - start)
