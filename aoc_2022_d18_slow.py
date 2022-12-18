from datetime import datetime
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('18.ex1').readlines()
lines_puzzle = open('18.in').readlines()


def get_points(c):
    (x1, y1, z1) = c
    P1 = set()
    P1.add((x1+1, y1+1, z1+1))
    P1.add((x1+1, y1+1, z1))
    P1.add((x1+1, y1, z1+1))
    P1.add((x1+1, y1, z1))
    P1.add((x1, y1+1, z1+1))
    P1.add((x1, y1+1, z1))
    P1.add((x1, y1, z1+1))
    P1.add((x1, y1, z1))
    return P1


def is_touch(c1, c2):
    P1 = get_points(c1)
    P2 = get_points(c2)
    O = P1 & P2
    if (len(O) >= 4):
        return True
    return False


def count_area(cubes):
    c = 0
    Xs = set()
    Ys = set()
    Zs = set()

    for cub in cubes:
        x, y, z = cub
        c += 1
        Xs.add((x, y, z))
        Xs.add((x+1, y, z))
        Ys.add((x, y, z))
        Ys.add((x, y+1, z))
        Zs.add((x, y, z))
        Zs.add((x, y, z+1))

    total = 6 * c
    ove_x = 2 * c - len(Xs)
    ove_y = 2 * c - len(Ys)
    ove_z = 2 * c - len(Zs)

    res = total - 2*(ove_x+ove_y+ove_z)
    return res


def solve1(lines):
    C = set()
    for line in lines:
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line.strip())]
        x, y, z = nums
        C.add((x, y, z))

    res = count_area(C)

    return res


def solve2(lines):
    C = set()

    for line in lines:
        line = line.strip()
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line)]
        x, y, z = nums
        C.add((x, y, z))

    xMin = min([x for (x, y, z) in C])
    xMax = max([x for (x, y, z) in C])
    yMin = min([y for (x, y, z) in C])
    yMax = max([y for (x, y, z) in C])
    zMin = min([z for (x, y, z) in C])
    zMax = max([z for (x, y, z) in C])

    A = set()
    for x in range(xMin-1, xMax+2):
        for y in range(yMin-1, yMax+2):
            for z in range(zMin-1, zMax+2):
                if (x, y, z) not in C:
                    A.add((x, y, z))

    Xs = set()
    Ys = set()
    Zs = set()

    M = A
    for m in M:
        (x, y, z) = m
        Xs.add((x, x+1))
        Ys.add((y, y+1))
        Zs.add((z, z+1))

    O = set()
    O.add((xMin, yMin, zMin))

    added = True
    while added:
        added = False
        to_move = set()
        for m in M:
            for o in O:
                if is_touch(o, m):
                    to_move.add(m)

        if len(to_move) > 0:
            added = True
            M = M-to_move
            O |= to_move
            # print(len(O), len(M))

    all_surf = count_area(C)
    internal_surf = count_area(M)

    return all_surf - internal_surf


print(CRED + "sample:", solve1(lines_sample), CEND)  # 64
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 4192

print(CRED + "sample:", solve2(lines_sample), CEND)  # 58
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 2520

stop = datetime.now()
print("duration:", stop - start)
