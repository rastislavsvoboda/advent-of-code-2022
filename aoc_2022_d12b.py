from datetime import datetime
from collections import deque

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('12.ex1').readlines()
lines_puzzle = open('12.in').readlines()

DR = [1, 0, -1, 0]
DC = [0, 1, 0, -1]


def solve(lines, part):
    res = None
    G = []
    S = []
    e = (None, None)

    r = 0
    for line in lines:
        line = line.strip()
        row = []
        for c in range(len(line)):
            x = line[c]
            if x == "S":
                x = "a"
                if part == 1:
                    # add only "S" as starting point
                    S.append((r, c))    
            elif x == "E":
                e = (r, c)
                x = "z"
            
            if part == 2 and x == "a":
                # add all "a" as starting point
                S.append((r, c))
            row.append(x)
        G.append(row)
        r += 1

    R = len(G)
    C = len(G[0])

    q = deque()
    for s in S:
        q.append((0, s))
    seen = set()
    while len(q):
        l, pos = q.popleft()

        if pos == e:
            res = l
            break

        if pos in seen:
            continue

        seen.add(pos)
        r, c = pos
        elev = G[r][c]
        for i in range(4):
            rr = r + DR[i]
            cc = c + DC[i]
            if 0 <= rr < R and 0 <= cc < C:
                if ord(G[rr][cc]) - ord(elev) <= 1:
                    q.append((l+1, (rr, cc)))

    return res


print(CRED + "sample:", solve(lines_sample, 1), CEND)  # 31
print(CGRN + "puzzle:", solve(lines_puzzle, 1), CEND)  # 517
print(CRED + "sample:", solve(lines_sample, 2), CEND)  # 29
print(CGRN + "puzzle:", solve(lines_puzzle, 2), CEND)  # 512

stop = datetime.now()
print("duration:", stop - start)
