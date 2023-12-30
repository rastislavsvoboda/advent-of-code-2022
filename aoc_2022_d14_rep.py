from datetime import datetime
from aoc_tools import *
from functools import cmp_to_key

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('14.in').read()
text_sample = open('14.ex1').read()


def fall1(x, y, W, S, limit):
    xx = x
    yy = y
    while True:
        if yy == limit:
            break

        if not ((xx, yy + 1) in W or (xx, yy + 1) in S):
            yy += 1
            continue
        if not ((xx - 1, yy + 1) in W or (xx - 1, yy + 1) in S):
            xx -= 1
            yy += 1
            continue
        if not ((xx + 1, yy + 1) in W or (xx + 1, yy + 1) in S):
            xx += 1
            yy += 1
            continue
        break

    return (xx, yy)


def fall2(x, y, W, S, floor):
    xx = x
    yy = y
    while True:
        if not ((xx, yy + 1) in W or (xx, yy + 1) in S) and (yy + 1 < floor):
            yy += 1
            continue
        if not ((xx - 1, yy + 1) in W or (xx - 1, yy + 1) in S) and (yy + 1 < floor):
            xx -= 1
            yy += 1
            continue
        if not ((xx + 1, yy + 1) in W or (xx + 1, yy + 1) in S) and (yy + 1 < floor):
            xx += 1
            yy += 1
            continue
        break

    return (xx, yy)


def solve(text, part):
    res = None

    # start location
    sx, sy = (500, 0)

    # walls
    W = set()
    # sands
    S = set()
    for line in text.split("\n"):
        parts = line.split(" -> ")
        segments = [get_all_nums(p) for p in parts]
        # print(segments)
        for (x1, y1), (x2, y2) in zip(segments, segments[1:]):
            # print(f"-> {x1} {y1} -> {x2} {y2}")
            dx = x2 - x1
            dy = y2 - y1
            if dx == 0:
                x = x1
                if dy > 0:
                    for y in range(y1, y2 + 1):
                        W.add((x, y))
                elif dy < 0:
                    for y in range(y1, y2 - 1, -1):
                        W.add((x, y))
                else:
                    assert False
            elif dy == 0:
                y = y1
                if dx > 0:
                    for x in range(x1, x2 + 1):
                        W.add((x, y))
                elif dx < 0:
                    for x in range(x1, x2 - 1, -1):
                        W.add((x, y))
                else:
                    assert False
            else:
                assert False

    if part == 1:
        maxy = max([y for (x, y) in W])
        is_max_y = False
        while not is_max_y:
            is_falling = True
            while is_falling:
                x, y = sx, sy
                xx, yy = fall1(x, y, W, S, maxy)
                if yy == maxy:
                    is_max_y = True
                    break
                S.add((xx, yy))
                if (x, y) == (xx, yy):
                    is_falling = False

        res = len(S)

    elif part == 2:
        maxy = max([y for (x, y) in W])
        while True:
            x, y = sx, sy
            xx, yy = fall2(x, y, W, S, maxy + 2)
            S.add((xx, yy))
            if (x, y) == (xx, yy):
                break

        res = len(S)

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 24
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 897

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 93
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 26683

stop = datetime.now()
print("duration:", stop - start)
