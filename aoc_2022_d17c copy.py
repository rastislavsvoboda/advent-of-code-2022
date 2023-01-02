from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

# pypy3.exe .\save.py 0

start = datetime.now()
lines_sample = open('17.ex1').readlines()
lines_puzzle = open('17.in').readlines()

def gen_rock(i):
    if i == 0:
        return [[1,1,1,1]]
    if i == 1:
        return [
            [0,1,0],
            [1,1,1],
            [0,1,0],
        ]
    if i == 2:
        return [
            [1,1,1],
            [0,0,1],
            [0,0,1],
        ]
    if i == 3:
        return [
            [1],
            [1],
            [1],
            [1],
        ]
    if i == 4:
        return [
            [1,1],
            [1,1]
        ]
    assert False


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


def try_push(G, rock, t, b, l, r, d):
    if not (0 <= l+d < 7 and 0 <= r+d < 7):
        return False, t, b, l, r
    for rr in range(b, t+1):
        for cc in range(l, r+1):
            if rock[rr-b][cc-l] == 0:
                continue
            if G[rr][cc+d] == 1:
                return False, t, b, l, r
    return True, t, b, l+d, r+d


def place(G, rock, t, b, l, r):
    for rr in range(b, t+1):
        for cc in range(l, r+1):
            if rock[rr-b][cc-l] == 0:
                continue
            assert G[rr][cc] == 0
            G[rr][cc] = 1

    for r in range(len(G)-1, -1, -1):
        if 1 in G[r]:
            return r

    return 0


def print_G(G):
    for r in range(len(G)-1, -1, -1):
        print("".join(G[r]))
    print()


def solve1(lines):
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
                    t-=1
                    b-=1

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

# def solve2(lines):
#     res = 0
#     x = 0
#     for i in range(1000000000000):
#         x +=1
#         if x == 100000000:
#             print(i)
#             x=0
#         res+=1

def try_compact(G, off):
    # print("before", len(G))
    for r in range(len(G)-1, -1, -1):
        if all(x == 1 for x in G[r]):
            return off,r

    return off,0

def solve2x(lines):
    C = 7
    G = []
    G.append(['.' for c in range(C)])
    G.append(['.' for c in range(C)])
    G.append(['.' for c in range(C)])
    row = 3

    for line in lines:
        line = line.strip()
    wind = 0
    i = 0
    cnt = 0
    offset = 0
    xx = 0
    # while i < 2022:
    while i < 1000000000000:
        if xx == 1000000:
            print(i)
            xx=0
        xx +=1

        l = 2
        rock = gen_rock(i % 5)
        h = len(rock)
        w = len(rock[0])

        r = 2+w-1
        b = row
        t = b+h-1

        while len(G)<=t:
            G.append(['.' for c in range(C)])

        can_fall = True
        while can_fall:
            # can_push, t, b, l, r = try_push(
            #     G, rock, t, b, l, r, -1 if line[wind] == "<" else 1)

            can_push = False
            d = -1 if line[wind] == "<" else 1
            if not (0 <= l+d < 7 and 0 <= r+d < 7):
                can_push = False
            else:
                for rr in range(b, t+1):
                    for cc in range(l, r+1):
                        if rock[rr-b][cc-l] == 1 and G[rr][cc+d] == 1:
                            can_push = False
                            break
                    if not can_push:
                        break
                if can_push:
                    l+=d
                    r+=d

            wind = (wind+1) % len(line)
            can_fall, t, b, l, r = try_fall(G, rock, t, b, l, r)
            if not can_fall:
                break
        top = place(G, rock, t, b, l, r)

        cnt += 1
        # print_G(G)
        row = top + 3 + 1
        i += 1

        if i % 10000 == 0:
            # print("before", len(G))
            offset, delta = try_compact(G,offset)

            # print(offset, delta)
            if delta > 0:
                G = G[delta+1:]
                # print("after", len(G))
                offset += delta+1
                # print(offset)
                row -= delta+1


    # print(cnt)
    # print()


    for r in range(len(G)-1, -1, -1):
        if "#" in G[r]:
            return r + 1 + offset

    return 0

def solve2(lines):
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
    offset = 0
    xx = 0
    while i < 2022:
    # while i < 1000000000000:
        if xx == 1000000:
            print(i)
            xx=0
        xx +=1

        l = 2
        typ = i % 5

        if typ == 0:
            rock = [[1,1,1,1]]
            w=4
            h=1
        elif typ == 1:
            rock = [
                [0,1,0],
                [1,1,1],
                [0,1,0],
            ]
            w=3
            h=3
        elif typ == 2:
            rock = [
                [1,1,1],
                [0,0,1],
                [0,0,1],
            ]
            w=3
            h=3
        elif typ == 3:
            rock = [
                [1],
                [1],
                [1],
                [1],
            ]
            w=1
            h=4
        elif typ == 4:
            rock = [
                [1,1],
                [1,1]
            ]
            w=2
            h=2
        else:
            assert False

        # h = len(rock)
        # w = len(rock[0])

        r = 2+w-1
        b = row
        t = b+h-1

        while len(G)<=t:
            G.append([0 for c in range(C)])

        for xxx in range(3):
            if line[wind] == "<":
                if l>0:
                    l-=1
                    r-=1
            else:
                if r<C-1:
                    l+=1
                    r+=1
            wind = (wind+1) % len(line)
            t-=1
            b-=1

        can_fall = True
        while can_fall:
            can_push = True
            d = -1 if line[wind] == "<" else 1
            if not (0 <= l+d < 7 and 0 <= r+d < 7):
                can_push = False
            else:
                for rr in range(b, t+1):
                    for cc in range(l, r+1):
                        if rock[rr-b][cc-l] == 1 and G[rr][cc+d] == 1:
                            can_push = False
                            break
                    if not can_push:
                        break
                if can_push:
                    l+=d
                    r+=d

            wind = (wind+1) % len(line)

            can_fall = True
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
                    t-=1
                    b-=1
        top = place(G, rock, t, b, l, r)

        cnt += 1
        # print_G(G)
        row = top + 3 + 1
        i += 1

        if i % 1000 == 0:
            # print("before", len(G))
            offset, delta = try_compact(G,offset)

            # print(offset, delta)
            if delta > 0:
                G = G[delta+1:]
                # print("after", len(G))
                offset += delta+1
                # print(offset)
                row -= delta+1


    # print(cnt)
    # print()


    for r in range(len(G)-1, -1, -1):
        if 1 in G[r]:
            return r + 1 + offset

    return 0


# p1_sample = solve1(lines_sample)
# print(CRED + "sample:", p1_sample, CEND)  # 3068
# assert p1_sample == 3068



# p1_sample = solve2(lines_sample)
# print(CRED + "sample:", p1_sample, CEND)  # 3068
# assert p1_sample == 3068


print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  #

stop = datetime.now()
print("duration:", stop - start)
