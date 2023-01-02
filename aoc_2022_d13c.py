from datetime import datetime
from functools import cmp_to_key

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('13.ex1').read()
lines_puzzle = open('13.in').read()


def comp(l, r):
    if isinstance(l, int) and isinstance(r, int):
        return -1 if l < r else 1 if l > r else 0

    if isinstance(l, list) and isinstance(r, list):
        if len(l) == 0 or len(r) == 0:
            return -1 if len(l) < len(r) else 1 if len(l) > len(r) else 0
        cmp_head = comp(l[0], r[0])
        return comp(l[1:], r[1:]) if cmp_head == 0 else cmp_head

    if isinstance(l, int) and isinstance(r, list):
        return comp([l], r)

    if isinstance(l, list) and isinstance(r, int):
        return comp(l, [r])

    assert False


def solve1(text):
    I = []
    i = 1
    for grp in text.split('\n\n'):
        lines = grp.split('\n')
        l = eval(lines[0].strip())
        r = eval(lines[1].strip())
        # print(l)
        # print(r)
        if comp(l, r) != 1:
            I.append(i)

        i += 1

    # print(I)
    res = sum(I)
    return res


def solve2(text):
    D = []

    for line in text.split('\n'):
        if line == "":
            continue
        D.append(eval(line))

    i1 = 1
    i2 = 1
    for d in D:
        if comp(d, [[2]]) < 0:
            i1 += 1
        if comp(d, [[6]]) < 0:
            i2 += 1

    if comp([[2]], [[6]]) < 0:
        i2 += 1
    else:
        i1 += 1

    res = i1 * i2
    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 13
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 5393
print(CRED + "sample:", solve2(lines_sample), CEND)  # 140
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 26712

stop = datetime.now()
print("duration:", stop - start)
