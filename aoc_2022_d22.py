from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
lines_sample = open('22.ex1').readlines()
lines_puzzle = open('22.in').readlines()


def move1(G, R, C, r, c, d, i):
    pos = r, c
    while i > 0:
        if d == 1:
            r += 1
            if (r, c) not in G:
                r = 0
            while (r, c) not in G:
                r += 1
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c
        elif d == 3:
            r -= 1
            if (r, c) not in G:
                r = R
            while (r, c) not in G:
                r -= 1
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c
        elif d == 0:
            c += 1
            if (r, c) not in G:
                c = 0
            while (r, c) not in G:
                c += 1
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c
        elif d == 2:
            c -= 1
            if (r, c) not in G:
                c = C
            while (r, c) not in G:
                c -= 1
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c
        i -= 1
    return pos


def test1_sample(G, R, C):
    assert G[(0, 8)] == "."
    assert G[(0, 9)] == "."
    assert G[(0, 10)] == "."
    assert G[(0, 11)] == "#"
    assert G[(0, 7)] == " "
    assert G[(0, 12)] == " "
    assert G[(R-1, C-2)] == "#"

    r, c, d = 6, 11, 0
    assert (6, 0) == move1(G, R, C, 6, 11, 0, 1)
    assert (6, 1) == move1(G, R, C, 6, 11, 0, 2)
    assert (6, 1) == move1(G, R, C, 6, 11, 0, 3)

    assert (6, 10) == move1(G, R, C, 6, 11, 2, 1)
    assert (6, 9) == move1(G, R, C, 6, 11, 2, 2)
    assert (6, 8) == move1(G, R, C, 6, 11, 2, 3)
    assert (6, 8) == move1(G, R, C, 6, 11, 2, 4)


def solve1(lines, type, is_test):
    res = 0

    G = {}
    R = 0
    C = 0
    while True:
        line = lines[R][:-1]
        if line == "":
            break
        for (c, ch) in enumerate(line):
            if ch != " ":
                G[(R, c)] = ch
                if is_test:
                    # no walls, allow testing moves between planes
                    G[(R, c)] = '.'

            C = max(C, c)

        R += 1

        res += 1
    C = C+1

    if is_test:
        print(R, C)
        # print(G)

    cmd = lines[R+1].strip()
    I = []
    d = ""
    for ch in cmd:
        if ch in ["", "R", "L"]:
            if d != "":
                I.append(int(d))
                d = ""
            I.append(ch)
        else:
            d += ch
    if d != "":
        I.append(int(d))

    d = 0
    r = 0
    c = lines[0].index('.')
    if is_test:
        print(r, c, d)

    if is_test:
        return "None"

    for i in I:
        # move
        if i == "L":
            d = (d+4-1) % 4
        elif i == "R":
            d = (d+1) % 4
        else:
            assert isinstance(i, int)
            r, c = move1(G, R, C, r, c, d, i)

    res = 1000*(r+1) + 4 * (c+1) + d

    return res


def move2_sample(G, R, C, r, c, d, i):
    Q = R // 3
    assert C // 4 == Q

    qr = r // Q
    qc = c // Q
    assert (qr, qc) in [(0, 2), (1, 0), (1, 1), (1, 2), (2, 2), (2, 3)]

    pos = r, c, d
    while i > 0:
        rr, cc, dd = pos
        if dd == 1:
            # DOWN
            r += 1
            if (r, c) not in G:
                if (qr, qc) == (1, 0):
                    r = 3 * Q - 1
                    c = (3 * Q - 1) - (cc % Q)
                    d = 3
                elif (qr, qc) == (1, 1):
                    c = 2 * Q
                    r = (3 * Q - 1) - (cc % Q)
                    d = 0
                elif (qr, qc) == (2, 2):
                    r = 2 * Q - 1
                    c = (1 * Q - 1) - (cc % Q)
                    d = 3
                elif (qr, qc) == (2, 3):
                    c = 0 * Q
                    r = (2 * Q - 1) - (cc % Q)
                    d = 0
                else:
                    assert False
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c, d
        elif dd == 3:
            # UP
            r -= 1
            if (r, c) not in G:
                if (qr, qc) == (1, 0):
                    r = 0 * Q
                    c = (3 * Q - 1) - (cc % Q)
                    d = 1
                elif (qr, qc) == (1, 1):
                    c = 2 * Q
                    r = (0 * Q) + (cc % Q)
                    d = 0
                elif (qr, qc) == (0, 2):
                    r = 1 * Q
                    c = (1 * Q - 1) - (cc % Q)
                    d = 1
                elif (qr, qc) == (2, 3):
                    c = 3 * Q - 1
                    r = (2 * Q - 1) - (cc % Q)
                    d = 2
                else:
                    assert False
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c, d
        elif dd == 0:
            # RIGHT
            c += 1
            if (r, c) not in G:
                if (qr, qc) == (0, 2):
                    c = 4 * Q - 1
                    r = (3 * Q - 1) - (rr % Q)
                    d = 2
                elif (qr, qc) == (1, 2):
                    r = 2 * Q
                    c = (4 * Q - 1) - (rr % Q)
                    d = 1
                elif (qr, qc) == (2, 3):
                    c = 3 * Q - 1
                    r = (1 * Q - 1) - (rr % Q)
                    d = 2
                else:
                    assert False
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c, d
        elif dd == 2:
            # LEFT
            c -= 1
            if (r, c) not in G:
                if (qr, qc) == (0, 2):
                    r = 1 * Q
                    c = (1 * Q) + (rr % Q)
                    d = 1
                elif (qr, qc) == (1, 0):
                    r = 3 * Q - 1
                    c = (4 * Q - 1) - (rr % Q)
                    d = 3
                elif (qr, qc) == (2, 2):
                    r = 2 * Q - 1
                    c = (2 * Q - 1) - (rr % Q)
                    d = 3
                else:
                    assert False
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c, d
        i -= 1
    return pos


def move2_puzzle(G, R, C, r, c, d, i):
    Q = R // 4

    assert C // 3 == Q

    qr = r // Q
    qc = c // Q
    assert (qr, qc) in [(0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (3, 0)]

    pos = r, c, d
    while i > 0:
        rr, cc, dd = pos
        if dd == 1:
            # DOWN
            r += 1
            if (r, c) not in G:
                if (qr, qc) == (3, 0):
                    r = 0 * Q
                    c = (2 * Q) + (cc % Q)
                    d = 1
                elif (qr, qc) == (2, 1):
                    c = (1 * Q - 1)
                    r = (3 * Q) + (cc % Q)
                    d = 2
                elif (qr, qc) == (0, 2):
                    c = 2 * Q - 1
                    r = (1 * Q) + (cc % Q)
                    d = 2
                else:
                    assert False
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c, d
        elif dd == 3:
            # UP
            r -= 1
            if (r, c) not in G:
                if (qr, qc) == (2, 0):
                    c = 1 * Q
                    r = (1 * Q) + (cc % Q)
                    d = 0
                elif (qr, qc) == (0, 1):
                    c = 0 * Q
                    r = (3 * Q) + (cc % Q)
                    d = 0
                elif (qr, qc) == (0, 2):
                    r = (4 * Q - 1)
                    c = (0 * Q) + (cc % Q)
                    d = 3
                else:
                    assert False
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c, d
        elif dd == 0:
            # RIGHT
            c += 1
            if (r, c) not in G:
                if (qr, qc) == (0, 2):
                    c = (2 * Q - 1)
                    r = (3 * Q - 1) - (rr % Q)
                    d = 2
                elif (qr, qc) == (1, 1):
                    r = 1 * Q - 1
                    c = (2 * Q) + (rr % Q)
                    d = 3
                elif (qr, qc) == (2, 1):
                    c = 3 * Q - 1
                    r = (1 * Q - 1) - (rr % Q)
                    d = 2
                elif (qr, qc) == (3, 0):
                    r = 3 * Q - 1
                    c = (1 * Q) + (rr % Q)
                    d = 3
                else:
                    assert False
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c, d
        elif dd == 2:
            # LEFT
            c -= 1
            if (r, c) not in G:
                if (qr, qc) == (0, 1):
                    c = 0 * Q
                    r = (3 * Q - 1) - (rr % Q)
                    d = 0
                elif (qr, qc) == (1, 1):
                    r = 2 * Q
                    c = (0 * Q) + (rr % Q)
                    d = 1
                elif (qr, qc) == (2, 0):
                    c = 1 * Q
                    r = (1 * Q - 1) - (rr % Q)
                    d = 0
                elif (qr, qc) == (3, 0):
                    r = 0 * Q
                    c = (1 * Q) + (rr % Q)
                    d = 1
                else:
                    assert False
            assert (r, c) in G
            if G[(r, c)] == "#":
                break
            pos = r, c, d
        i -= 1
    return pos


def test2_sample(G, R, C):
    assert (8, 14, 1) == move2_sample(G, R, C, 5, 11, 0, 1)
    assert (5, 11, 2) == move2_sample(G, R, C, 8, 14, 3, 1)

    assert (7, 1, 3) == move2_sample(G, R, C, 11, 10, 1, 1)
    assert (11, 10, 3) == move2_sample(G, R, C, 7, 1, 1, 1)

    assert (4, 4, 1) == move2_sample(G, R, C, 0, 8, 2, 1)
    assert (0, 8, 0) == move2_sample(G, R, C, 4, 4, 3, 1)

    assert (4, 3, 1) == move2_sample(G, R, C, 0, 8, 3, 1)
    assert (0, 8, 1) == move2_sample(G, R, C, 4, 3, 3, 1)

    assert (11, 15, 2) == move2_sample(G, R, C, 0, 11, 0, 1)
    assert (0, 11, 2) == move2_sample(G, R, C, 11, 15, 0, 1)

    assert (4, 0, 1) == move2_sample(G, R, C, 0, 11, 3, 1)
    assert (0, 11, 1) == move2_sample(G, R, C, 4, 0, 3, 1)

    assert (4, 7, 1) == move2_sample(G, R, C, 3, 8, 2, 1)
    assert (3, 8, 0) == move2_sample(G, R, C, 4, 7, 3, 1)

    assert (8, 15, 2) == move2_sample(G, R, C, 3, 11, 0, 1)
    assert (3, 11, 2) == move2_sample(G, R, C, 8, 15, 0, 1)

    assert (8, 15, 1) == move2_sample(G, R, C, 4, 11, 0, 1)
    assert (4, 11, 2) == move2_sample(G, R, C, 8, 15, 3, 1)

    assert (11, 12, 3) == move2_sample(G, R, C, 7, 0, 2, 1)
    assert (7, 0, 0) == move2_sample(G, R, C, 11, 12, 1, 1)

    assert (11, 11, 3) == move2_sample(G, R, C, 7, 0, 1, 1)
    assert (7, 0, 3) == move2_sample(G, R, C, 11, 11, 1, 1)

    assert (11, 8, 3) == move2_sample(G, R, C, 7, 3, 1, 1)
    assert (7, 3, 3) == move2_sample(G, R, C, 11, 8, 1, 1)

    assert (11, 8, 0) == move2_sample(G, R, C, 7, 4, 1, 1)
    assert (7, 4, 3) == move2_sample(G, R, C, 11, 8, 2, 1)

    assert (8, 8, 0) == move2_sample(G, R, C, 7, 7, 1, 1)
    assert (7, 7, 3) == move2_sample(G, R, C, 8, 8, 2, 1)

    assert (8, 12, 1) == move2_sample(G, R, C, 7, 11, 0, 1)
    assert (7, 11, 2) == move2_sample(G, R, C, 8, 12, 3, 1)


def test2_puzzle(G, R, C):
    # PUZZLE
    assert (150, 0, 0) == move2_puzzle(G, R, C, 0, 50, 3, 1)
    assert (0, 50, 1) == move2_puzzle(G, R, C, 150, 0, 2, 1)

    assert (199, 0, 0) == move2_puzzle(G, R, C, 0, 99, 3, 1)
    assert (0, 99, 1) == move2_puzzle(G, R, C, 199, 0, 2, 1)

    assert (199, 0, 3) == move2_puzzle(G, R, C, 0, 100, 3, 1)
    assert (0, 100, 1) == move2_puzzle(G, R, C, 199, 0, 1, 1)

    assert (199, 49, 3) == move2_puzzle(G, R, C, 0, 149, 3, 1)
    assert (0, 149, 1) == move2_puzzle(G, R, C, 199, 49, 1, 1)

    assert (149, 99, 2) == move2_puzzle(G, R, C, 0, 149, 0, 1)
    assert (0, 149, 2) == move2_puzzle(G, R, C, 149, 99, 0, 1)

    assert (150, 49, 2) == move2_puzzle(G, R, C, 149, 50, 1, 1)
    assert (149, 50, 3) == move2_puzzle(G, R, C, 150, 49, 0, 1)

    assert (50, 50, 0) == move2_puzzle(G, R, C, 100, 0, 3, 1)
    assert (100, 0, 1) == move2_puzzle(G, R, C, 50, 50, 2, 1)

    assert (99, 50, 0) == move2_puzzle(G, R, C, 100, 49, 3, 1)
    assert (100, 49, 1) == move2_puzzle(G, R, C, 99, 50, 2, 1)

    assert (49, 149, 2) == move2_puzzle(G, R, C, 100, 99, 0, 1)
    assert (100, 99, 2) == move2_puzzle(G, R, C, 49, 149, 0, 1)

    assert (149, 0, 0) == move2_puzzle(G, R, C, 0, 50, 2, 1)

    assert (100, 0, 0) == move2_puzzle(G, R, C, 49, 50, 2, 1)

    assert (100, 49, 1) == move2_puzzle(G, R, C, 99, 50, 2, 1)

    assert (49, 50, 0) == move2_puzzle(G, R, C, 100, 0, 2, 1)

    assert (0, 50, 0) == move2_puzzle(G, R, C, 149, 0, 2, 1)

    assert (0, 50, 1) == move2_puzzle(G, R, C, 150, 0, 2, 1)

    assert (0, 149, 1) == move2_puzzle(G, R, C, 199, 49, 1, 1)
    assert (150, 49, 2) == move2_puzzle(G, R, C, 149, 50, 1, 1)
    assert (199, 49, 2) == move2_puzzle(G, R, C, 149, 99, 1, 1)
    assert (50, 99, 2) == move2_puzzle(G, R, C, 49, 100, 1, 1)
    assert (99, 99, 2) == move2_puzzle(G, R, C, 49, 149, 1, 1)


def solve2(lines, type, is_test):
    res = 0

    is_sample = type == "sample"

    G = {}
    R = 0
    C = 0
    while True:
        line = lines[R][:-1]
        if line == "":
            break
        for (c, ch) in enumerate(line):
            if ch != " ":
                G[(R, c)] = ch
                if is_test:
                    # no walls, allow testing moves between planes
                    G[(R, c)] = '.'
            C = max(C, c)

        R += 1

        res += 1
    C = C+1
    if is_test:
        print(R, C)

    cmd = lines[R+1].strip()
    I = []
    d = ""
    for ch in cmd:
        if ch in ["", "R", "L"]:
            if d != "":
                I.append(int(d))
                d = ""
            I.append(ch)
        else:
            d += ch
    if d != "":
        I.append(int(d))

    d = 0
    r = 0
    c = lines[0].index('.')
    if is_test:
        print(r, c, d)

    if is_sample:
        assert R == 12
        assert C == 16
        if is_test:
            test2_sample(G, R, C)
            return "None"
    else:
        assert R == 200
        assert C == 150
        if is_test:
            test2_puzzle(G, R, C)
            return "None"

    for i in I:
        # move
        if i == "L":
            d = (d+4-1) % 4
        elif i == "R":
            d = (d+1) % 4
        else:
            assert isinstance(i, int)

            if is_sample:
                r, c, d = move2_sample(G, R, C, r, c, d, i)
            else:
                r, c, d = move2_puzzle(G, R, C, r, c, d, i)

    # print(r+1, c+1, d)
    res = 1000*(r+1) + 4 * (c+1) + d

    return res


is_test = False

# hardcoded for my input

print(CRED + "sample:", solve1(lines_sample, "sample", is_test), CEND)  # 6032
print(CGRN + "puzzle:", solve1(lines_puzzle, "puzzle", is_test), CEND)  # 76332

print(CRED + "sample:", solve2(lines_sample, "sample", is_test), CEND)  # 5031
print(CGRN + "puzzle:", solve2(lines_puzzle, "puzzle", is_test), CEND)  # 144012


stop = datetime.now()
print("duration:", stop - start)
