from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('13.ex1').read()
lines_puzzle = open('13.in').read()


def comp(n1, n2):
    if isinstance(n1, int) and isinstance(n2, int):
        return -1 if n1 < n2 else 1 if n1 > n2 else 0

    if isinstance(n1, list) and isinstance(n2, list):
        if len(n1) == 0 or len(n2) == 0:
            return -1 if len(n1) < len(n2) else 1 if len(n1) > len(n2) else 0
        if n1[0] == n2[0]:
            return comp(n1[1:], n2[1:])
        return comp(n1[0], n2[0])

    if isinstance(n1, int) and isinstance(n2, list):
        return comp([n1], n2)

    if isinstance(n1, list) and isinstance(n2, int):
        return comp(n1, [n2])

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


def bubbleSort(arr):
    n = len(arr)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if not comp(arr[j], arr[j + 1]):
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

        if not swapped:
            return


def solve2(text):
    D = []
    D.append([[2]])
    D.append([[6]])

    for line in text.split('\n'):
        if line == "":
            continue
        D.append(eval(line))

    bubbleSort(D)

    # for x in D:
    #     print(x)

    i1 = D.index([[2]]) + 1
    i2 = D.index([[6]]) + 1
    res = i1 * i2
    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 13
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 5393
print(CRED + "sample:", solve2(lines_sample), CEND)  # 140
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 26712

stop = datetime.now()
print("duration:", stop - start)
