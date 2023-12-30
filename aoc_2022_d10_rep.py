from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('10.in').read()
text_sample = open('10.ex1').read()


def check(t, X, C):
    if t in C:
        val = X * t
    else:
        val = None
    return val


def draw(t, X):
    if abs(X - ((t - 1) % 40)) <= 1:
        ch = "█"
    else:
        ch = "."
    return ch


def solve(text, part):
    X = 1
    t = 1
    if part == 1:
        C = [20, 60, 100, 140, 180, 220]
        V = []

        for line in text.split("\n"):
            words = line.split()

            if words[0] == "noop":
                v = check(t, X, C)
                if v:
                    V.append(v)
                t += 1
            elif words[0] == "addx":
                n = int(words[1])
                v = check(t, X, C)
                if v:
                    V.append(v)
                t += 1
                v = check(t, X, C)
                if v:
                    V.append(v)
                t += 1
                X += n
            else:
                assert False

            if t > max(C):
                break

        res = sum(V)
    else:
        D = []

        for line in text.split("\n"):
            words = line.split()

            if words[0] == "noop":
                ch = draw(t, X)
                D.append(ch)
                t += 1
            elif words[0] == "addx":
                n = int(words[1])
                ch = draw(t, X)
                D.append(ch)
                t += 1
                ch = draw(t, X)
                D.append(ch)
                t += 1
                X += n
            else:
                assert False

        for i in range(0, len(D), 40):
            print("".join(D[i:i + 40]))
        res = "...read the display..."

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 13140
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 14060

print(CRED + "sample:", solve(text_sample, 2), CEND)  #
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  #

stop = datetime.now()
print("duration:", stop - start)
