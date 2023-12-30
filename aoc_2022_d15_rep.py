from datetime import datetime
from aoc_tools import *
from functools import cmp_to_key

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('15.in').read()
text_sample = open('15.ex1').read()


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def solve1(text, ty):
    S = []
    B = []
    for line in text.split("\n"):
        sx, sy, bx, by = get_all_nums(line)
        S.append((sx, sy))
        B.append((bx, by))

    N = len(B)
    assert N == len(S)

    not_allowed = set()
    b_on_target_row = set()
    for i in range(N):
        sx, sy = S[i]
        bx, by = B[i]
        dst = manhattan_dist(sx, sy, bx, by)
        dy = abs(sy - ty)
        if dy <= dst:
            dx = dst - dy
            if by == ty:
                b_on_target_row.add(bx)

            for x in range(sx - dx, sx + dx + 1):
                not_allowed.add(x)

    res = len(not_allowed.difference(b_on_target_row))

    return res


def compact(intervals, new):
    s2, e2 = new

    for i, (s1, e1) in enumerate(intervals):
        if s2 == e1 + 1:
            new2 = (s1, e2)
            intervals.pop(i)
            return compact(intervals, new2)
        elif s1 == e2 + 1:
            new2 = (s2, e1)
            intervals.pop(i)
            return compact(intervals, new2)
        else:
            so = max(s1, s2)
            eo = min(e1, e2)
            if so <= eo:
                new2 = (min(s1, s2), max(e1, e2))
                intervals.pop(i)
                return compact(intervals, new2)

    return list(sorted(intervals + [new]))


def solve2(text, limit):
    S = []
    B = []
    for line in text.split("\n"):
        sx, sy, bx, by = get_all_nums(line)
        S.append((sx, sy))
        B.append((bx, by))

    N = len(B)
    assert N == len(S)

    # not allowed
    NA = defaultdict(list)
    for i in range(N):
        # signal
        sx, sy = S[i]
        # bacon
        bx, by = B[i]
        dst = manhattan_dist(sx, sy, bx, by)

        # fill intervals (x1,x2) on appropriate y row clamped within 0-limit area
        # when adding a new interval compact with existing intervals for given y row
        x1 = sx - dst
        x2 = sx + dst

        if 0 <= sy <= limit:
            NA[sy] = compact(NA[sy], (max(0, x1), min(limit, x2)))

        y1 = sy
        y2 = sy
        for dy in range(dst):
            x1 += 1
            x2 -= 1
            y1 -= 1
            y2 += 1
            assert x2 - x1 >= 0
            if 0 <= y1 <= limit:
                NA[y1] = compact(NA[y1], (max(0, x1), min(limit, x2)))
            if 0 <= y2 <= limit:
                NA[y2] = compact(NA[y2], (max(0, x1), min(limit, x2)))

    for y in range(0, limit + 1):
        if NA[y] != [(0, limit)]:
            # there should be 1 result (0,b) (c,<limit>)
            # where there is a gap of 1 number between b and c
            intervals = NA[y]
            assert len(intervals) == 2
            (a, b), (c, d) = intervals
            assert a == 0
            assert b + 1 == c - 1
            assert d == limit
            distress_bx = b + 1
            distress_by = y
            break

    frq = distress_bx * 4000000 + distress_by
    return frq


print(CRED + "sample:", solve1(text_sample, 10), CEND)  # 26
print(CGRN + "puzzle:", solve1(text_puzzle, 2000000), CEND)  # 5525990

print(CRED + "sample:", solve2(text_sample, 20), CEND)  # 56000011
print(CGRN + "puzzle:", solve2(text_puzzle, 4000000), CEND)  # 11756174628223

stop = datetime.now()
print("duration:", stop - start)
