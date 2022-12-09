from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample1 = open('9.ex1').readlines()
lines_sample2 = open('9.ex2').readlines()
lines_puzzle = open('9.in').readlines()


DIRS = "DRUL"
DR = [1, 0, -1, 0]
DC = [0, 1, 0, -1]


def move(head, direction):
    h_r, h_c = head
    h_r += DR[direction]
    h_c += DC[direction]
    return (h_r, h_c)


def follow(head, tail):
    h_r, h_c = head
    t_r, t_c = tail

    if not (-1 <= (h_r - t_r) <= 1 and -1 <= (h_c - t_c) <= 1):
        if h_c > t_c:
            t_c += 1
        elif h_c < t_c:
            t_c -= 1
        if h_r > t_r:
            t_r += 1
        elif h_r < t_r:
            t_r -= 1

    return (t_r, t_c)


def print_d(D):
    lst = list(D)
    R1 = min(list(map(lambda x: x[0], lst)))
    C1 = min(list(map(lambda x: x[1], lst)))
    R2 = max(list(map(lambda x: x[0], lst)))
    C2 = max(list(map(lambda x: x[1], lst)))

    for r in range(R1, R2+1):
        for c in range(C1, C2+1):
            if (r, c) in D:
                print("#", end='')
            else:
                print(".", end='')
        print()


def print_p2(T):
    R1 = -10
    C1 = 0
    R2 = 0
    C2 = 10

    for r in range(R1, R2+1):
        for c in range(C1, C2+1):
            x = "."
            for j in range(9, -1, -1):
                if (r, c) == T[j]:
                    if j == 0:
                        x = "H"
                    else:
                        x = j
            if x == "." and r == 0 and c == 0:
                x = "s"

            print(x, end='')
        print()


def solve1(lines):
    res = 0
    D = set()
    h = (0, 0)
    t = (0, 0)
    D.add(t)
    for line in lines:
        words = line.strip().split()
        dir_ = words[0]
        d = DIRS.index(dir_)
        c = int(words[1])
        for i in range(c):
            h = move(h, d)
            t = follow(h, t)
            D.add(t)

    # print_d(D)
    res = len(D)
    return res


def solve2(lines):
    res = 0
    D = set()
    # first is head, then 9 knots
    T = [(0, 0) for i in range(10)]
    D.add(T[-1])
    for line in lines:
        words = line.strip().split()
        dir_ = words[0]
        d = DIRS.index(dir_)
        c = int(words[1])
        for i in range(c):
            T[0] = move(T[0], d)
            for j in range(1, 10):
                T[j] = follow(T[j-1], T[j])
                # print_p2(T)
                # print("-----")
            D.add(T[-1])

    # print_d(D)
    res = len(D)
    return res


print(CRED + "sample1:", solve1(lines_sample1), CEND)  # 13
print(CGRN + "puzzle: ", solve1(lines_puzzle), CEND)   # 6236
print(CRED + "sample1:", solve2(lines_sample1), CEND)  # 1
print(CRED + "sample2:", solve2(lines_sample2), CEND)  # 36
print(CGRN + "puzzle: ", solve2(lines_puzzle), CEND)   # 2449

stop = datetime.now()
print("duration:", stop - start)
