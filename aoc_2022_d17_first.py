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
        return ["@@@@"]
    if i == 1:
        return [
            ".@.",
            "@@@",
            ".@."
        ]
    if i == 2:
        return [
            "@@@",
            "..@",
            "..@",
        ]
    if i == 3:
        return [
            "@",
            "@",
            "@",
            "@",
        ]
    if i == 4:
        return [
            "@@",
            "@@"
        ]
    assert False


def try_fall(G, rock, t, b, l, r):
    if b == 0:
        return False, t, b, l, r

    for rr in range(b, t+1):
        for cc in range(l, r+1):
            if rock[rr-b][cc-l] == ".":
                continue
            if G[rr-1][cc] == "#":
                return False, t, b, l, r

    return True, t-1, b-1, l, r


def try_push(G, rock, t, b, l, r, d):
    if not (0 <= l+d < 7 and 0 <= r+d < 7):
        return False, t, b, l, r
    for rr in range(b, t+1):
        for cc in range(l, r+1):
            if rock[rr-b][cc-l] == ".":
                continue
            if G[rr][cc+d] == "#":
                return False, t, b, l, r
    return True, t, b, l+d, r+d


def place(G, rock, t, b, l, r):
    for rr in range(b, t+1):
        for cc in range(l, r+1):
            if rock[rr-b][cc-l] == ".":
                continue
            assert G[rr][cc] == "."
            G[rr][cc] = "#"

    for r in range(len(G)-1, -1, -1):
        if "#" in G[r]:
            return r

    return 0


def print_G(G):
    for r in range(len(G)-1, -1, -1):
        print("".join(G[r]))
    print()


def solve1(lines):
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
    while i < 2022:
        l = 2
        rock = gen_rock(i % 5)
        h = len(rock)
        w = len(rock[0])
        for x in range(h):
            G.append(['.' for c in range(C)])

        r = 2+w-1
        b = row
        t = b+h-1

        can_fall = True
        while can_fall:
            can_push, t, b, l, r = try_push(
                G, rock, t, b, l, r, -1 if line[wind] == "<" else 1)
            wind = (wind+1) % len(line)
            can_fall, t, b, l, r = try_fall(G, rock, t, b, l, r)
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
        if "#" in G[r]:
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
        lll ="".join(G[r])
        if lll == "#######":
            return off,r

    return off,0

def solve2(lines):
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
            can_push, t, b, l, r = try_push(
                G, rock, t, b, l, r, -1 if line[wind] == "<" else 1)
            wind = (wind+1) % len(line)
            can_fall, t, b, l, r = try_fall(G, rock, t, b, l, r)
            if not can_fall:
                break
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
        if "#" in G[r]:
            return r + 1 + offset

    return 0




# p1_sample = solve2(lines_sample)
# print(CRED + "sample:", p1_sample, CEND)  # 3068
# assert p1_sample == 3068


print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 

stop = datetime.now()
print("duration:", stop - start)
