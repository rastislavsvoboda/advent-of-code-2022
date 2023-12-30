from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('2.in').read()
text_sample = open('2.ex1').read()

O1 = "ABC"
O2 = "XYZ"


def score(o1, o2):
    i1 = O1.index(o1)
    i2 = O2.index(o2)

    score = i2 + 1

    if i1 == i2:
        # draw
        score += 3
    elif (i2 - i1 + 3) % 3 == 1:
        # win
        score += 6
    elif (i2 - i1 + 3) % 3 == 2:
        # loose
        score += 0

    return score


def solve1(text):
    res = 0
    for g in text.split("\n"):
        a, b = g.split()
        res += score(a, b)
    return res


def play(a, instr):
    i1 = O1.index(a)

    if instr == "Y":
        # draw
        i2 = i1
    elif instr == "X":
        # loose
        i2 = (i1 + 2) % 3
    elif instr == "Z":
        # win
        i2 = (i1 + 1) % 3
    else:
        assert False, instr

    return O2[i2]


def solve2(text):
    res = 0
    for g in text.split("\n"):
        a, instr = g.split()
        b = play(a, instr)
        res += score(a, b)
    return res


print(CRED + "sample:", solve1(text_sample), CEND)  # 15
print(CGRN + "puzzle:", solve1(text_puzzle), CEND)  # 11150

print(CRED + "sample:", solve2(text_sample), CEND)  # 12
print(CGRN + "puzzle:", solve2(text_puzzle), CEND)  # 8295

stop = datetime.now()
print("duration:", stop - start)
