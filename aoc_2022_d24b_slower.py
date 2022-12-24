from datetime import datetime
import heapq

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('24.ex2').readlines()
lines_puzzle = open('24.in').readlines()

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def move_bliz(R, C, bliz):
    new_bliz = []
    for b in bliz:
        r, c, d = b
        dr, dc = DIRS[d]
        r += dr
        c += dc
        if r == R-1:
            r = 1
        elif r == 0:
            r = R-2
        if c == C-1:
            c = 1
        elif c == 0:
            c = C-2
        new_bliz.append((r, c, d))
    return new_bliz


def get_bliz_at(R, C, bliz, t, memo):
    init_bliz = bliz

    def dp(t):
        if t == 0:
            return init_bliz

        if t in memo:
            return memo[t]

        prev_bliz = dp(t-1)
        new_bliz = move_bliz(R, C, prev_bliz)

        memo[t] = new_bliz
        return memo[t]

    return dp(t)


def get_time(G, R, C, B, memo, start_pos, end_pos, start_time):
    res = None
    q = []
    heapq.heappush(q, (start_time, start_pos[0], start_pos[1]))
    SEEN = set()

    while len(q) > 0:
        state = heapq.heappop(q)

        if state in SEEN:
            continue

        SEEN.add(state)

        time, r, c = state
        if (r, c) == end_pos:
            res = time
            break

        new_bliz = get_bliz_at(R, C, B, time+1, memo)
        unique_bliz = set([(br, bc) for (br, bc, bd) in new_bliz])

        for d in DIRS:
            rr = r+d[0]
            cc = c+d[1]
            if 0 <= rr < R and 0 <= cc < C:
                if G[rr][cc] == "#":
                    continue
                if (rr, cc) in unique_bliz:
                    continue

                if (time+1, rr, cc) not in SEEN:
                    heapq.heappush(q, (time+1, rr, cc))

        if (r, c) not in unique_bliz:
            if ((time+1, r, c)) not in SEEN:
                heapq.heappush(q, (time+1, r, c))

    return res


def solve(lines):
    BLIZ = ">v<^"
    B = []
    G = []
    r = 0
    for line in lines:
        row = []
        for c, ch in enumerate(line.strip()):
            if ch in BLIZ:
                B.append((r, c, BLIZ.index(ch)))
                ch = "."
            row.append(ch)
        G.append(row)
        r += 1

    R = len(G)
    C = len(G[0])

    start_c = G[0].index(".")
    end_c = G[R-1].index(".")
    # print(start_c, end_c)

    memo = {}

    start_p = (0, start_c)
    end_p = (R-1, end_c)

    time = get_time(G, R, C, B, memo, start_p, end_p, 0)
    res1 = time
    time = get_time(G, R, C, B, memo, end_p, start_p, time)
    time = get_time(G, R, C, B, memo, start_p, end_p, time)
    res2 = time
    return res1, res2


print(CRED + "sample:", solve(lines_sample), CEND)  # 18, 54
print(CGRN + "puzzle:", solve(lines_puzzle), CEND)  # 255, 809

stop = datetime.now()
print("duration:", stop - start)
