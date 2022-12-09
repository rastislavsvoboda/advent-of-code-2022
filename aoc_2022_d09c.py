from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample1 = open('9.ex1').readlines()
lines_sample2 = open('9.ex2').readlines()
lines_puzzle = open('9.in').readlines()


DIRS = {"D": (1, 0), "R": (0, 1), "U": (-1, 0), "L": (0, -1)}


def move(head, direction):
    h_r, h_c = head
    d_r, d_c = direction

    return (h_r + d_r, h_c + d_c)


def sign(x):
    return -1 if x < 0 else 1 if x > 0 else 0


def follow(head, tail):
    h_r, h_c = head
    t_r, t_c = tail
    d_r, d_c = h_r - t_r, h_c - t_c

    if abs(d_r) > 1 or abs(d_c) > 1:
        t_r += sign(d_r)
        t_c += sign(d_c)

    return (t_r, t_c)


def solve1(lines):
    D = set()
    h = (0, 0)
    t = (0, 0)
    D.add(t)

    for line in lines:
        words = line.strip().split()
        direction = DIRS[words[0]]
        amount = int(words[1])
        for i in range(amount):
            h = move(h, direction)
            t = follow(h, t)
            D.add(t)

    res = len(D)
    return res


def solve2(lines):
    D = set()
    # first is head, then 9 knots
    T = [(0, 0) for i in range(10)]
    D.add(T[-1])

    for line in lines:
        words = line.strip().split()
        direction = DIRS[words[0]]
        amount = int(words[1])
        for i in range(amount):
            T[0] = move(T[0], direction)
            for j in range(1, 10):
                T[j] = follow(T[j-1], T[j])
            D.add(T[-1])

    res = len(D)
    return res


print(CRED + "sample1:", solve1(lines_sample1), CEND)  # 13
print(CGRN + "puzzle: ", solve1(lines_puzzle), CEND)   # 6236
print(CRED + "sample1:", solve2(lines_sample1), CEND)  # 1
print(CRED + "sample2:", solve2(lines_sample2), CEND)  # 36
print(CGRN + "puzzle: ", solve2(lines_puzzle), CEND)   # 2449

stop = datetime.now()
print("duration:", stop - start)
