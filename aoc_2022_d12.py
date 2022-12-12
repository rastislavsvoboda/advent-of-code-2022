from datetime import datetime
import heapq

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('12.ex1').readlines()
lines_puzzle = open('12.in').readlines()

DR = [1, 0, -1, 0]
DC = [0, 1, 0, -1]


def get_possible(G, p):
    R = len(G)
    C = len(G[0])

    pos = []
    r, c = p
    elev = G[r][c]
    for i in range(4):
        rr = r + DR[i]
        cc = c + DC[i]
        if 0 <= rr < R and 0 <= cc < C:
            elev_new = G[rr][cc]
            if ord(elev_new) - ord(elev) <= 1:
                pos.append((rr, cc))

    return pos


def solve1(lines):
    res = 0
    G = []
    s = (None, None)
    e = (None, None)

    r = 0
    for line in lines:
        line = line.strip()
        row = []
        for c in range(len(line)):
            x = line[c]
            if x == "S":
                s = (r, c)
                x = "a"
            elif x == "E":
                e = (r, c)
                x = "z"
            row.append(x)
        G.append(row)
        r += 1

    heap = []
    heapq.heappush(heap, (0, s))
    seen = set()
    while len(heap):
        l, pos = heapq.heappop(heap)

        if pos == e:
            res = l
            break

        if pos in seen:
            continue
        seen.add(pos)

        possible = get_possible(G, pos)
        for p in possible:
            heapq.heappush(heap, ((l+1), p))

    return res


def solve2(lines):
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
            elif x == "E":
                e = (r, c)
                x = "z"
            if x == "a":
                S.append((r, c))
            row.append(x)
        G.append(row)
        r += 1

    RES = []
    for s in S:
        heap = []
        heapq.heappush(heap, (0, s))
        seen = set()
        while len(heap):
            l, pos = heapq.heappop(heap)

            if pos == e:
                RES.append(l)
                break

            if pos in seen:
                continue
            seen.add(pos)

            possible = get_possible(G, pos)
            for p in possible:
                heapq.heappush(heap, ((l+1), p))

    res = sorted(RES)[0]
    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 31
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 517
print(CRED + "sample:", solve2(lines_sample), CEND)  # 29
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 512

stop = datetime.now()
print("duration:", stop - start)
