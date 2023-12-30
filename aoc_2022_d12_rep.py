import heapq
from datetime import datetime
import aoc_tools

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('12.in').read()
text_sample = open('12.ex1').read()


def min_path(start_pos, end_pos, G):
    R = len(G)
    C = len(G[0])
    q = []
    r, c = start_pos
    heapq.heappush(q, (0, r, c))

    res = None
    SEEN = set()
    while q:
        d, r, c = heapq.heappop(q)

        if (r, c) == end_pos:
            res = d
            break

        if (r, c) in SEEN:
            continue

        SEEN.add((r, c))
        ch = G[r][c]

        for rr, cc in aoc_tools.neighbours4(r, c):
            if rr in range(R) and cc in range(C):
                new_ch = G[rr][cc]
                diff = ord(new_ch) - ord(ch)
                if (diff <= 1):
                    q.append((d + 1, rr, cc))

    return res


def solve(text, part):
    res = None

    start_positions = []
    start_pos = None
    end_pos = None

    G = []
    for r, line in enumerate(text.split("\n")):
        row = []
        for c, ch in enumerate(line):
            if ch == "S":
                start_pos = (r, c)
                ch = "a"

            if part == 2:
                if ch == "a":
                    start_positions.append((r, c))

            if ch == "E":
                end_pos = (r, c)
                ch = "z"
            row.append(ch)

        G.append(row)

    if part == 1:
        res = min_path(start_pos, end_pos, G)
    elif part == 2:
        valid_res = []
        for s in start_positions:
            l = min_path(s, end_pos, G)
            if l:
                valid_res.append(l)

        res = min(valid_res)

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 31
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 517

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 29
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 512

stop = datetime.now()
print("duration:", stop - start)
