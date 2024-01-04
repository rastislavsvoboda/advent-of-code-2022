from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('23.in').read()
text_sample = open('23.ex1').read()


def is_other_elf_around(r, c, G):
    cnt = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (r + dr, c + dc) in G:
                cnt += 1
    assert cnt >= 1
    return cnt > 1


def propose(r, c, G, prop):
    p = prop

    for dp in range(4):
        pp = (p + dp) % 4
        if pp == 0:
            # N, NE, NW
            if (not (r - 1, c) in G) and not (r - 1, c + 1) in G and not (r - 1, c - 1) in G:
                return (r - 1, c)
        elif pp == 1:
            # S, SE, SW
            if (not (r + 1, c) in G) and not (r + 1, c + 1) in G and not (r + 1, c - 1) in G:
                return (r + 1, c)
        elif pp == 2:
            # W, NW, SW
            if (not (r, c - 1) in G) and not (r - 1, c - 1) in G and not (r + 1, c - 1) in G:
                return (r, c - 1)
        elif pp == 3:
            # E, NE, SE
            if (not (r, c + 1) in G) and not (r - 1, c + 1) in G and not (r + 1, c + 1) in G:
                return (r, c + 1)
        else:
            assert prop, f"Wrong prop {prop}"

    return (r, c)


def solve(text, part):
    res = None

    G = {}
    for r, line in enumerate(text.split("\n")):
        for c, ch in enumerate(line):
            if ch == "#":
                G[(r, c)] = "#"

    N = len(G.keys())

    prop = 0
    t = 0
    while True:
        PROPOSING = defaultdict(list)
        for (r, c) in G.keys():
            if is_other_elf_around(r, c, G):
                (rr, cc) = propose(r, c, G, prop)
                PROPOSING[(rr, cc)].append((r, c))

        any_moved = False
        for k, v in PROPOSING.items():
            if len(v) == 1:
                G.pop(v[0])
                G[k] = "#"
                any_moved = True

        prop = (prop + 1) % 4

        t += 1
        if part == 1:
            if t == 10:
                coords = list(G.keys())
                min_r = min([r for (r, c) in coords])
                max_r = max([r for (r, c) in coords])
                min_c = min([c for (r, c) in coords])
                max_c = max([c for (r, c) in coords])

                area = (max_r - min_r + 1) * (max_c - min_c + 1)
                elfs = len(coords)
                res = area - elfs
                assert elfs == N
                break
        elif part == 2:
            if not any_moved:
                res = t
                break
        else:
            break

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 110
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 4336

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 20
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 1005

stop = datetime.now()
print("duration:", stop - start)
