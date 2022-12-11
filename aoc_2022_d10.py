from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('10.ex1').readlines()
lines_puzzle = open('10.in').readlines()


def check1(c, x, S, V):
    c += 1
    if c in S:
        V.append(c * x)
    return c


def solve1(lines):
    S = [20, 60, 100, 140, 180, 220]
    V = []
    res = 0
    x = 1
    c = 1
    for line in lines:
        words = line.strip().split()
        if words[0] == "noop":
            c = check1(c, x, S, V)
        elif words[0] == "addx":
            var = int(words[1])
            c = check1(c, x, S, V)
            x += var
            c = check1(c, x, S, V)
    res = sum(V)

    return res


def check2(c, x, p, P):
    i = (c-1) % 40

    if abs(x - i) <= 1:
        p += "█"
    else:
        p += " "
    if len(p) == 40:
        P.append(p)
        p = ""
    c += 1

    return c, p


def solve2(lines):
    P = []
    p = ""
    x = 1
    c = 1
    for line in lines:
        words = line.strip().split()
        if words[0] == "noop":
            c, p = check2(c, x, p, P)
        elif words[0] == "addx":
            c, p = check2(c, x, p, P)
            var = int(words[1])
            c, p = check2(c, x, p, P)
            x += var

    for p in P:
        print(p)

    return None


print(CRED + "sample:", solve1(lines_sample), CEND)  # 13140
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 14060
print(CRED + "sample:", solve2(lines_sample), CEND)  #
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # PAPKFKEJ


stop = datetime.now()
print("duration:", stop - start)
