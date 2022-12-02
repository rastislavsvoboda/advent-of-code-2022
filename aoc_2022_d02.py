from datetime import datetime

start = datetime.now()
lines = open('2.in').readlines()

PL1 = {'A': 1, 'B': 2, 'C': 3}
PL2 = {'X': 1, 'Y': 2, 'Z': 3}


def round_outcome(p1, p2):
    if p1 == p2:
        # draw
        res = 3
    elif p1 == 1 and p2 == 2 or p1 == 2 and p2 == 3 or p1 == 3 and p2 == 1:
        # win
        res = 6
    else:
        # loose
        res = 0

    return res


def count1(entry):
    first = entry[0]
    second = entry[1]

    p1 = PL1[first]
    p2 = PL2[second]

    score = p2 + round_outcome(p1, p2)

    return score


def count2(entry):
    first = entry[0]
    second = entry[1]

    DRAW = {1: 1, 2: 2, 3: 3}
    WIN = {1: 2, 2: 3, 3: 1}
    LOOSE = {1: 3, 2: 1, 3: 2}

    p1 = PL1[first]

    if second == 'X':
        p2 = LOOSE[p1]
    elif second == 'Y':
        p2 = DRAW[p1]
    elif second == 'Z':
        p2 = WIN[p1]

    score = p2 + round_outcome(p1, p2)

    return score


def solve1(lines):
    res = 0
    for line in lines:
        line = line.strip()
        round = line.split()
        res += count1(round)

    return res


def solve2(lines):
    res = 0
    for line in lines:
        line = line.strip()
        round = line.split()
        res += count2(round)

    return res


print(solve1(lines))  # 11150
print(solve2(lines))  # 8295

stop = datetime.now()
print("duration:", stop - start)
