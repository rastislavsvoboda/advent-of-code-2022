from datetime import datetime
from collections import defaultdict

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('23.ex1').readlines()
# lines_sample = open('23.ex2').readlines()
lines_puzzle = open('23.in').readlines()


def propose_move(G, r, c, d):
    res = None
    if d == 0:
        # N:
        if not ((r-1, c-1) in G or (r-1, c) in G or (r-1, c+1) in G):
            return (r-1, c)
        return None
    if d == 1:
        # S
        if not ((r+1, c-1) in G or (r+1, c) in G or (r+1, c+1) in G):
            return (r+1, c)
        return None
    elif d == 2:
        # W
        if not ((r-1, c-1) in G or (r, c-1) in G or (r+1, c-1) in G):
            return (r, c-1)
        return None
    elif d == 3:
        # E
        if not ((r-1, c+1) in G or (r, c+1) in G or (r+1, c+1) in G):
            return (r, c+1)
        return None
    else:
        assert False


def consider_moves(G):
    N = defaultdict(list)
    for (r, c) in G:
        d = G[(r, c)]
        others = 0
        for rr in range(r-1, r+2):
            for cc in range(c-1, c+2):
                if rr == r and cc == c:
                    continue
                if (rr, cc) in G:
                    others += 1
        if others > 0:
            curr_d = d
            prop = None
            for dd in range(d, d+4):
                d = (dd % 4)
                prop = propose_move(G, r, c, d)
                if prop is not None:
                    N[prop].append(((r, c), curr_d))
                    break
    return N


def print_s(sug):
    for s in sug:
        print(s, sug[s])
    print()


def solve1(lines):
    G = {}
    r = 0
    for line in lines:
        line = line.strip()
        for c, ch in enumerate(line):
            if ch == "#":
                G[(r, c)] = 0
        r += 1

    t = 1
    while t <= 10:
        suggested = consider_moves(G)
        for pos in suggested.keys():
            if len(suggested[pos]) == 1:
                old_pos, d = suggested[pos][0]
                G.pop(old_pos)
                G[pos] = d

        for pos in G.keys():
            G[pos] = (G[pos]+1) % 4

        t += 1

    minR = min(r for (r, c) in G.keys())
    maxR = max(r for (r, c) in G.keys())
    minC = min(c for (r, c) in G.keys())
    maxC = max(c for (r, c) in G.keys())

    empty = 0
    for rr in range(minR, maxR+1):
        for cc in range(minC, maxC+1):
            if (rr, cc) not in G:
                empty += 1

    return empty


def solve2(lines):
    G = {}
    r = 0
    for line in lines:
        line = line.strip()
        for c, ch in enumerate(line):
            if ch == "#":
                G[(r, c)] = 0
        r += 1

    t = 1
    while True:
        suggested = consider_moves(G)

        moved = False
        for pos in suggested.keys():
            if len(suggested[pos]) == 1:
                moved = True
                old_pos, d = suggested[pos][0]
                G.pop(old_pos)
                G[pos] = d

        if not moved:
            break

        for pos in G.keys():
            G[pos] = (G[pos]+1) % 4

        # print(G)
        t += 1

    return t


print(CRED + "sample:", solve1(lines_sample), CEND)  # 110
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 4336

print(CRED + "sample:", solve2(lines_sample), CEND)  # 20
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 1005

stop = datetime.now()
print("duration:", stop - start)
