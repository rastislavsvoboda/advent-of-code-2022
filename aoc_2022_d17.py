from datetime import datetime
from collections import defaultdict

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('17.ex1').readlines()
lines_puzzle = open('17.in').readlines()


def gen_rock(type):
    if type == 0:
        rock = [
            0b0011110]
        w = 4
        h = 1
    elif type == 1:
        rock = [
            0b0001000,
            0b0011100,
            0b0001000,
        ]
        w = 3
        h = 3
    elif type == 2:
        # bottom first !!
        rock = [
            0b0011100,
            0b0000100,
            0b0000100,
        ]
        w = 3
        h = 3
    elif type == 3:
        rock = [
            0b0010000,
            0b0010000,
            0b0010000,
            0b0010000,
        ]
        w = 1
        h = 4
    elif type == 4:
        rock = [
            0b0011000,
            0b0011000,
        ]
        w = 2
        h = 2
    else:
        assert False

    return (rock, w, h)


def try_push(G, rock, t, b, l, r, d, C):
    if d == "<":
        if 0 < l:
            can_push = True
            new_rock = [rr << 1 for rr in rock]
            for rr in range(b, t+1):
                if new_rock[rr-b] & G[rr] > 0:
                    can_push = False
                    break

            if can_push:
                l -= 1
                r -= 1
                rock = new_rock
    else:
        if r < C-1:
            can_push = True
            new_rock = [rr >> 1 for rr in rock]
            for rr in range(b, t+1):
                if new_rock[rr-b] & G[rr] > 0:
                    can_push = False
                    break

            if can_push:
                l += 1
                r += 1
                rock = new_rock

    return rock, l, r


def try_fall(G, rock, t, b):
    can_fall = False
    if b > 0:
        can_fall = True
        for rr in range(b, t+1):
            if rock[rr-b] & G[rr-1] > 0:
                can_fall = False
                break
        if can_fall:
            t -= 1
            b -= 1
    return can_fall, t, b


def place(G, rock, t, b):
    can_compact=False
    # place rock with top/bottom
    for r in range(b, t+1):
        G[r] |= rock[r-b]
        if G[r] == 0b1111111:
            can_compact=True

    # for top occupied row
    for top_row in reversed(range(len(G))):
        if G[top_row] > 0:
            return top_row, can_compact

    return 0, can_compact


def get_score(G, offset=0, bonus=0):
    for r in reversed(range(len(G))):
        if G[r] > 0:
            return r + 1 + offset + bonus

    return 0


def print_G(G):
    for r in reversed(range(len(G))):
        print("".join(G[r]))
    print()


def solve1(lines):
    start_column = 2
    game_width = 7
    types_count = 5
    free_rows = 3

    winds = lines[0].strip()
    winds_len = len(winds)

    G = []

    wind = 0
    row = free_rows
    typ = 0
    i = 2022

    while i > 0:
        rock, w, h = gen_rock(typ % 5)

        l = start_column
        r = start_column+w-1
        b = row
        t = b+h-1

        while len(G) <= t:
            G.append(0)

        typ = (typ + 1) % types_count

        can_fall = True
        while can_fall:
            rock, l, r = try_push(G, rock, t, b, l, r,
                                  winds[wind], game_width)

            wind = (wind+1) % winds_len

            can_fall, t, b = try_fall(G, rock, t, b)

        top, _ = place(G, rock, t, b)
        row = top + free_rows + 1

        i -= 1

    res = get_score(G)

    return res


def try_compact(G):
    for r in reversed(range(len(G))):
        if G[r] == 0b1111111:
            # number of rows that can be removed
            return r+1

    return 0


def solve2(lines):
    start_column = 2
    game_width = 7
    types_count = 5
    free_rows = 3

    winds = lines[0].strip()
    winds_len = len(winds)

    G = []
    found_first_key = None
    SNAP = defaultdict(int)

    wind = 0
    row = free_rows
    offset = 0
    bonus = 0
    typ = 0
    i = 1000000000000
    xx = 1000
    delta_i = 0
    delta_wind = 0
    delta_typ = 0
    snapshot = False

    while i > 0:
        # if xx == 0:
        #     print(i)
        #     xx = 1000
        # xx-=1

        delta_i += 1

        rock, w, h = gen_rock(typ % 5)

        l = start_column
        r = start_column+w-1
        b = row
        t = b+h-1

        while len(G) <= t:
            G.append(0)

        if snapshot:
            game_state = ""
            for rr in G:
                game_state += str(rr) + ","
            if (game_state, wind, typ) in SNAP:
                # print("found at ", i, len(SNAP))
                if found_first_key == None:
                    found_first_key = (game_state, wind, typ)
                    delta_i = 0
                    delta_wind = 0
                    delta_typ = 0
                    score_1 = get_score(G, offset, bonus)

                elif (game_state, wind, typ) == found_first_key:
                    score_2 = get_score(G, offset, bonus)
                    delta_score = score_2 - score_1
                    # print(delta_i, delta_wind, delta_typ, delta_score)
                    times_rep = i // delta_i
                    bonus = delta_score * times_rep
                    i %= delta_i
                    
                # print(SNAP.values())
            SNAP[(game_state, wind, typ)] += 1

        typ = (typ + 1) % types_count
        delta_typ += 1

        can_fall = True
        while can_fall:
            rock, l, r = try_push(G, rock, t, b, l, r,
                                  winds[wind], game_width)

            delta_wind += 1
            wind = (wind+1) % winds_len

            can_fall, t, b = try_fall(G, rock, t, b)

        top, can_compact = place(G, rock, t, b)
        row = top + free_rows + 1

        i -= 1

        if can_compact:
            delta = try_compact(G)
            if delta > 0:
                snapshot = True
                G = G[delta:]
                offset += delta
                row -= delta

    res = get_score(G, offset, bonus)

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 3068
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 3202

# print(CGRN + "puzzle:", solve2(lines_sample), CEND)  #
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 1591977077352

stop = datetime.now()
print("duration:", stop - start)
