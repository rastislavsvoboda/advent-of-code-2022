from datetime import datetime
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('11.ex1').readlines()
lines_puzzle = open('11.in').readlines()


def solve1(lines):
    I = []
    M = []
    OPS = []
    T = []
    m = 0
    i = 0
    while i < len(lines):
        nums = re.findall(r"[+-]?\d+", lines[i+1].strip())
        M.append([int(n) for n in nums])
        OPS.append(lines[i+2].strip().split()[-3:])
        x = int(lines[i+3].strip().split()[-1])
        m1 = int(lines[i+4].strip().split()[-1])
        m2 = int(lines[i+5].strip().split()[-1])
        T.append((x, m1, m2))
        I.append(0)
        i += 7
        m += 1

    for r in range(20):
        for m in range(len(M)):
            # print("monkey", m)
            for i in M[m]:
                # print("item", i)
                I[m] += 1
                x = OPS[m][2]
                op = OPS[m][1]
                if x == "old":
                    v = i
                else:
                    v = int(x)
                if op == "*":
                    newV = i * v
                elif op == "+":
                    newV = i + v
                else:
                    assert False
                # print("new", newV)
                newV = newV // 3
                # print("bored", newV)
                # print("test", T[m][0])
                if newV % T[m][0] == 0:
                    toM = T[m][1]
                    # print("true", toM)
                else:
                    toM = T[m][2]
                    # print("false", toM)
                M[toM].append(newV)
            # assert(False)
            M[m] = []
        # for m in range(len(M)):
        #     print(m, ":", M[m])
        # assert(False)

    # print(I)
    l = list(sorted(I))
    res = l[-1] * l[-2]
    return res


def solve2(lines):
    I = []
    M = []
    OPS = []
    T = []
    m = 0
    i = 0
    while i < len(lines):
        nums = re.findall(r"[+-]?\d+", lines[i+1].strip())
        M.append([int(n) for n in nums])
        OPS.append(lines[i+2].strip().split()[-3:])
        x = int(lines[i+3].strip().split()[-1])
        m1 = int(lines[i+4].strip().split()[-1])
        m2 = int(lines[i+5].strip().split()[-1])
        T.append((x, m1, m2))
        I.append(0)
        i += 7
        m += 1

    divNum = 1
    for t,m1_,m2_ in T:
        divNum *= t

    for r in range(10000):
        for m in range(len(M)):
            for i in M[m]:
                I[m] += 1
                x = OPS[m][2]
                op = OPS[m][1]
                if x == "old":
                    v = i
                else:
                    v = int(x)
                if op == "*":
                    newV = i * v
                elif op == "+":
                    newV = i + v
                else:
                    assert False
                itemToStore = newV % divNum

                if itemToStore % T[m][0] == 0:
                    toM = T[m][1]
                else:
                    toM = T[m][2]
                M[toM].append(itemToStore)
            M[m] = []

    # print(I)
    l = list(sorted(I))
    res = l[-1] * l[-2]
    return res

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 10605
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 111210
print(CRED + "sample:", solve2(lines_sample), CEND)  # 2713310158
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 15447387620

stop = datetime.now()
print("duration:", stop - start)
