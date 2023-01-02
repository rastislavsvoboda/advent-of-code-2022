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


def try_fall(G, rock, t, b, l, r):
    if b == 0:
        return False, t, b, l, r

    for rr in range(b, t+1):
        for cc in range(l, r+1):
            if rock[rr-b][cc-l] == 0:
                continue
            if G[rr-1][cc] == 1:
                return False, t, b, l, r

    return True, t-1, b-1, l, r


def try_push_old(G, rock, t, b, l, r, d):
    if not (0 <= l+d < 7 and 0 <= r+d < 7):
        return False, t, b, l, r
    for rr in range(b, t+1):
        for cc in range(l, r+1):
            if rock[rr-b][cc-l] == 0:
                continue
            if G[rr][cc+d] == 1:
                return False, t, b, l, r
    return True, t, b, l+d, r+d


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
    # place rock with top/bottom
    for r in range(b, t+1):
        G[r] |= rock[r-b]

    # for top occupied row
    for top_row in range(len(G)-1, -1, -1):
        if G[top_row] > 0:
            return top_row

    return 0


def get_score(G, offset=0, bonus=0):
    for r in range(len(G)-1, -1, -1):
        if G[r] > 0:
            return r + 1 + offset + bonus

    return 0


def print_G(G):
    for r in range(len(G)-1, -1, -1):
        print("".join(G[r]))
    print()


def solve1_old(lines):
    C = 7
    G = []
    G.append([0 for c in range(C)])
    G.append([0 for c in range(C)])
    G.append([0 for c in range(C)])
    row = 3

    for line in lines:
        line = line.strip()
    wind = 0
    i = 0
    cnt = 0
    while i < 2022:
        l = 2
        rock = gen_rock(i % 5)
        h = len(rock)
        w = len(rock[0])
        for x in range(h):
            G.append([0 for c in range(C)])

        r = 2+w-1
        b = row
        t = b+h-1

        can_fall = True
        while can_fall:
            can_push, t, b, l, r = try_push(
                G, rock, t, b, l, r, -1 if line[wind] == "<" else 1)

            wind = (wind+1) % len(line)
            # can_fall, t, b, l, r = try_fall(G, rock, t, b, l, r)

            if b == 0:
                can_fall = False
            else:
                for rr in range(b, t+1):
                    for cc in range(l, r+1):
                        if rock[rr-b][cc-l] != 0 and G[rr-1][cc] == 1:
                            can_fall = False
                            break
                    if not can_fall:
                        break
                if can_fall:
                    t -= 1
                    b -= 1

            if not can_fall:
                break
        top = place(G, rock, t, b, l, r)

        cnt += 1
        # print_G(G)
        row = top + 3 + 1
        i += 1

    # print_G(G)
    print(cnt)

    for r in range(len(G)-1, -1, -1):
        if 1 in G[r]:
            return r + 1

    return 0


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

        top = place(G, rock, t, b)
        row = top + free_rows + 1

        i -= 1

    res = get_score(G)

    return res


def try_compact(G, off):
    for r in range(len(G)-1, -1, -1):
        if G[r] == 0b1111111:
            return off, r

    return off, 0


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
    xx = 0
    try_comp = 400
    typ = 0
    i = 0
    i = 2022
    i = 1000000000000

    delta_i = 0
    delta_wind = 0
    delta_typ = 0
    snapshot = False

    while i > 0:
        delta_i += 1

        rock, w, h = gen_rock(typ % 5)

        l = start_column = 2
        r = start_column = 2+w-1
        b = row
        t = b+h-1

        while len(G) <= t:
            G.append(0)

        if snapshot:
            sss = ""
            for rrr in G:
                sss += str(rrr) + ","
            if (sss, wind, typ) in SNAP:
                # print("found at ", i, len(SNAP))
                if found_first_key == None:
                    found_first_key = (sss, wind, typ)
                    delta_i = 0
                    delta_wind = 0
                    delta_typ = 0
                    score_1 = get_score(G, offset, bonus)
                    # for rs1 in range(len(G)-1, -1, -1):
                    #     if G[rs1] > 0:
                    #         score_1 = rs1 + 1 + offset
                    #         break

                elif (sss, wind, typ) == found_first_key:
                    score_2 = get_score(G, offset, bonus)
                    # for rs2 in range(len(G)-1, -1, -1):
                    #     if G[rs2] > 0:
                    #         score_2 = rs2 + 1 + offset
                    #         break
                    delta_score = score_2 - score_1
                    print(delta_i, delta_wind, delta_typ, delta_score)
                    times_rep = i // delta_i
                    bonus = delta_score * times_rep
                    i %= delta_i
                # print(SNAP.values())
            SNAP[(sss, wind, typ)] += 1

            snapshot = False

        typ = (typ + 1) % types_count
        delta_typ += 1

        can_fall = True
        while can_fall:
            rock, l, r = try_push(G, rock, t, b, l, r,
                                  winds[wind], game_width)

            delta_wind += 1
            wind = (wind+1) % winds_len

            can_fall, t, b = try_fall(G, rock, t, b)

        top = place(G, rock, t, b)
        row = top + free_rows + 1

        i -= 1

        try_comp -= 1

        if try_comp == 0:
            try_comp = 400
            # print("before", len(G))
            offset, delta = try_compact(G, offset)

            # print(offset, delta)
            if delta > 0:
                # print(delta)
                if (delta == 566):
                    snapshot = True
                    # rest = G[:delta]
                    # # print(i, delta, typ, wind)
                    # # print(rest[:60])
                    # sss = ""
                    # for rrr in rest:
                    #     sss += str(rrr) + ","
                    # # print(sss)
                    # if sss in RES:
                    #     print(delta_i, delta_wind, delta_typ)

                    # RES.add(sss)
                    # delta_i = 0
                    # delta_wind = 0
                    # delta_typ = 0

                G = G[delta+1:]
                # print("after", len(G))
                offset += delta+1
                # print(offset)
                row -= delta+1

    res = get_score(G, offset, bonus)

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  #
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  #

# print(CGRN + "puzzle:", solve2(lines_sample), CEND)  #
# print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 1591977077352

stop = datetime.now()
print("duration:", stop - start)
