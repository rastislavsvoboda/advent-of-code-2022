from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('24.in').read()
text_sample2 = open('24.ex2').read()


def move_bliz(R, C, bliz):
    DIRS = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    new_bliz = []
    for (r, c), ch in bliz:
        dr, dc = DIRS[ch]
        r += dr
        c += dc
        # wrap around (using % is quite slower)
        if r == R - 1:
            r = 1
        elif r == 0:
            r = R - 2
        if c == C - 1:
            c = 1
        elif c == 0:
            c = C - 2
        new_bliz.append(((r, c), ch))
    return new_bliz


def get_bliz_at(R, C, bliz, t, memo):
    init_bliz = bliz

    def dp(t):
        if t == 0:
            return init_bliz

        if t in memo:
            return memo[t]

        memo[t] = move_bliz(R, C, dp(t - 1))
        return memo[t]

    return dp(t)


def has_bliz_at_pos(r, c, bliz):
    for (b_pos, _) in bliz:
        if (r, c) == b_pos:
            return True
    return False


def get_time(G, R, C, B, memo, start_pos, end_pos, start_time):
    res = None
    q = deque()
    q.append((start_time, start_pos))
    SEEN = set()

    while len(q) > 0:
        state = q.popleft()

        if state in SEEN:
            continue

        SEEN.add(state)

        time, pos = state
        if pos == end_pos:
            res = time
            break

        r, c = pos

        new_bliz = get_bliz_at(R, C, B, time + 1, memo)

        # try to move, but avoid blizzard
        for (rr, cc) in neighbours4(r, c):
            if rr in range(R) and cc in range(C) and G[rr][cc] != "#":
                if not has_bliz_at_pos(rr, cc, new_bliz):
                    q.append((time + 1, (rr, cc)))

        # try to stay, but avoid blizzard
        if not has_bliz_at_pos(r, c, new_bliz):
            q.append((time + 1, (r, c)))

    return res


def solve(text):
    G = [list(line) for line in text.split("\n")]
    R = len(G)
    C = len(G[0])
    # blizzards are in internal part of G, without outer frame
    B = [((r, c), G[r][c]) for r in range(1, R - 1) for c in range(1, C - 1) if G[r][c] != "."]

    start_c = G[0].index(".")
    end_c = G[R - 1].index(".")

    memo = {}

    start_p = (0, start_c)
    end_p = (R - 1, end_c)

    time = get_time(G, R, C, B, memo, start_p, end_p, 0)
    res1 = time
    time = get_time(G, R, C, B, memo, end_p, start_p, time)
    time = get_time(G, R, C, B, memo, start_p, end_p, time)
    res2 = time

    return res1, res2


print(CRED + "sample:", solve(text_sample2), CEND)  # 18, 54
print(CGRN + "puzzle:", solve(text_puzzle), CEND)  # 255, 809

stop = datetime.now()
print("duration:", stop - start)
