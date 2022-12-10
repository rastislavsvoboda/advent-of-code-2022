from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('10.ex1').readlines()
lines_puzzle = open('10.in').readlines()

R = 40

def check1(c, x, V):
    c += 1
    if (c - 20) % R == 0:
        V.append(c * x)
    return c


def solve1(lines):
    V = []
    x = 1
    c = 1
    for line in lines:
        words = line.strip().split()
        if words[0] == "noop":
            c = check1(c, x, V)
        elif words[0] == "addx":
            var = int(words[1])
            c = check1(c, x, V)
            x += var
            c = check1(c, x, V)
    res = sum(V)
    return res


def check2(c, x, P):
    i = (c-1) % R
    if abs(x - i) <= 1:
        P += "█"
    else:
        P += " "
    c += 1
    return c


def solve2(lines):
    P = []
    x = 1
    c = 1
    for line in lines:
        words = line.strip().split()
        if words[0] == "noop":
            c = check2(c, x, P)
        elif words[0] == "addx":
            c = check2(c, x, P)
            var = int(words[1])
            c = check2(c, x, P)
            x += var

    for p in range(0, len(P), R):
        print("".join(P[p:p+R]))

    return None


print(CRED + "sample:", solve1(lines_sample), CEND)  # 13140
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 14060
print(CRED + "sample:", solve2(lines_sample), CEND)  #
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # PAPKFKEJ


stop = datetime.now()
print("duration:", stop - start)
