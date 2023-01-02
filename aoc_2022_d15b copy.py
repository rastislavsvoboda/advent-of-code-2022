from datetime import datetime
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('15.ex1').readlines()
lines_puzzle = open('15.in').readlines()

Y_sample = 10
Y_puzzle = 2000000
L_sample = 20
L_puzzle = 4000000


def manh_dist(s, b):
    sx, sy = s
    bx, by = b
    return abs(sx-bx) + abs(sy-by)


def solve1(lines, Y):
    G = set()
    S = []
    D = []
    minX = None
    maxX = None

    for line in lines:
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line.strip())]
        s = (nums[0], nums[1])
        b = (nums[2], nums[3])
        d = manh_dist(s, b)
        if s[1] == Y:
            G.add(s[0])
        if b[1] == Y:
            G.add(b[0])
        dy = abs(s[1] - Y)
        dx = d - dy
        if minX == None or (s[0]-dx) < minX:
            minX = s[0]-dx
        if maxX == None or (s[0]+dx) > maxX:            
            maxX = s[0]+dx
        S.append(s)
        D.append(d)

    assert minX != None and maxX != None
    res = 0
    for x in range(minX, maxX+1):
        for (i, s) in enumerate(S):
            if x not in G:
                d = manh_dist(s, (x, Y))
                if d <= D[i]:
                    G.add(x)
                    res += 1

    return res


def collapse(a, b):
    a_s, a_e = a
    b_s, b_e = b
    if a_s <= b_s:
        if b_s <= a_e+1:
            return (a_s, max(a_e, b_e)), None
    else:
        if a_s <= b_e+1:
            return (b_s, max(a_e, b_e)), None

    return a, b


def solve2(lines, limit):
    G = {}
    S = []  # signals
    D = []  # distances
    for line in lines:
        line = line.strip()
        nums = [int(n) for n in re.findall(r"[+-]?\d+", line)]
        s = (nums[0], nums[1])
        b = (nums[2], nums[3])
        d = manh_dist(s, b)
        G[s] = "S"
        G[b] = "B"
        S.append(s)
        D.append(d)

    X1 = 0
    Y1 = 0
    X2 = limit
    Y2 = limit

    for x in range(X1, X2+1):
        # if x % 10000 == 0:
        #     print(x)

        R = []  # ranges where S is in reach od line x
        for i, s in enumerate(S):
            d = D[i]
            dx = abs(s[0] - x)
            dy = d - dx
            if (dy >= 0):
                # S is in range of line x, compute boundaries
                r1 = max(s[1] - dy, Y1)
                r2 = min(s[1] + dy, Y2)
                R.append((r1, r2))

        R.sort()
        while len(R) != 1:
            collapsed = 0
            i = 0
            while i < len(R)-1:
                for j in range(i+1, len(R)):
                    first, second = collapse(R[i], R[j])
                    if second == None:
                        collapsed += 1
                        R[i+1] = first
                        R[i] = None
                        i += 1
                        continue
                i += 1

            if collapsed != 0:
                R = sorted([r for r in R if r != None])
                continue

            # print(R)
            # should be only 1 missing, so R should have 2 ranges
            # where end of first and start of second differ by 2
            assert len(R) == 2
            R.sort()
            assert R[0][1] + 2 == R[1][0]
            y = R[0][1] + 1
            # compute frequency by given formula
            res = x * 4000000 + y
            return res

    return None


print(CRED + "sample:", solve1(lines_sample, Y_sample), CEND)  # 26
print(CGRN + "puzzle:", solve1(lines_puzzle, Y_puzzle), CEND)  # 5525990
print(CRED + "sample:", solve2(lines_sample, L_sample), CEND)  # 56000011
print(CGRN + "puzzle:", solve2(lines_puzzle, L_puzzle), CEND)  # 11756174628223

stop = datetime.now()
print("duration:", stop - start)
