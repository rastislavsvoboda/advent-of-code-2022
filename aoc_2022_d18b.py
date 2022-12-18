from datetime import datetime
from collections import deque
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('18.ex1').readlines()
lines_puzzle = open('18.in').readlines()


def count_area(cubes):
    res = 0
    for (x, y, z) in cubes:
        for d in [-1, 1]:
            if (x+d, y, z) not in cubes:
                res += 1
            if (x, y+d, z) not in cubes:
                res += 1
            if (x, y, z+d) not in cubes:
                res += 1
    return res


def get_expanding_points(p):
    (x, y, z) = p
    res = []
    for d in [-1, 1]:
        res.append((x+d, y, z))
        res.append((x, y+d, z))
        res.append((x, y, z+d))
    return res


def solve(lines):
    C = set()

    xMin = None
    xMax = None
    yMin = None
    yMax = None
    zMin = None
    zMax = None

    for line in lines:
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line.strip())]
        x, y, z = nums
        C.add((x, y, z))
        if xMin == None or x < xMin:
            xMin = x
        if xMax == None or x > xMax:
            xMax = x
        if yMin == None or y < yMin:
            yMin = y
        if yMax == None or y > yMax:
            yMax = y
        if zMin == None or z < zMin:
            zMin = z
        if zMax == None or z > zMax:
            zMax = z

    
    # extend 1 cube around all directions
    X1, X2 = xMin - 1, xMax + 1
    Y1, Y2 = yMin - 1, yMax + 1
    Z1, Z2 = zMin - 1, zMax + 1

    # bounded box without cubes
    B = set()
    for x in range(X1, X2+1):
        for y in range(Y1, Y2+1):
            for z in range(Z1, Z2+1):
                p = (x, y, z)
                if p not in C:
                    B.add(p)

    # steam start
    p = (X1, Y1, Z1)
    q = deque()
    SEEN = set()
    q.append(p)

    while len(q):
        p = q.popleft()

        if p in SEEN:
            continue

        SEEN.add(p)

        for expand_p in get_expanding_points(p):
            (x, y, z) = expand_p
            if X1 <= x <= X2 and Y1 <= y <= Y2 and Z1 <= z <= Z2:
                if expand_p not in C:
                    q.append(expand_p)

    # air
    A = B - SEEN
    all_area = count_area(C)
    air_area = count_area(A)

    res1 = all_area
    res2 = all_area - air_area

    return res1, res2


print(CRED + "sample:", solve(lines_sample), CEND)  # 64, 58
print(CGRN + "puzzle:", solve(lines_puzzle), CEND)  # 4192, 2520


stop = datetime.now()
print("duration:", stop - start)
