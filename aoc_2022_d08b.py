from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('8.ex1').readlines()
lines_puzzle = open('8.in').readlines()


# Down,Right,Up,Left
DR = [1, 0, -1, 0]
DC = [0, 1, 0, -1]


def is_visible(D, r, c):
    R = len(D)
    C = len(D[0])
    tree = D[r][c]

    V = [True for i in range(4)]
    for i in range(4):
        rr = r + DR[i]
        cc = c + DC[i]
        while 0 <= rr < R and 0 <= cc < C:
            if tree <= D[rr][cc]:
                V[i] = False
                break
            rr += DR[i]
            cc += DC[i]

    return any(V)


def score(D, r, c):
    R = len(D)
    C = len(D[0])
    tree = D[r][c]

    S = [0 for i in range(4)]
    for i in range(4):
        rr = r + DR[i]
        cc = c + DC[i]
        while 0 <= rr < R and 0 <= cc < C:
            S[i] += 1
            if tree <= D[rr][cc]:
                break
            rr += DR[i]
            cc += DC[i]

    s = 1
    for n in S:
        s *= n
    return s


def solve1(lines):
    D = []
    for line in lines:
        D.append([int(n) for n in line.strip()])

    # print(D)
    R = len(D)
    C = len(D[0])

    res1 = 0
    res2 = 0
    for r in range(R):
        for c in range(C):
            vis = is_visible(D, r, c)
            if vis:
                res1 += 1

            sco = score(D, r, c)
            if sco > res2:
                res2 = sco

    return res1, res2


print(CRED + "sample:", solve1(lines_sample), CEND)  # 21, 8
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 1812, 315495

stop = datetime.now()
print("duration:", stop - start)
