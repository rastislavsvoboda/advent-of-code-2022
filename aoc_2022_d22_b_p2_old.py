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


def test2_sample(G, R, C, move_fn):
    assert (8, 14, 1) == move_fn(G, R, C, 5, 11, 0, 1)
    assert (5, 11, 2) == move_fn(G, R, C, 8, 14, 3, 1)

    assert (7, 1, 3) == move_fn(G, R, C, 11, 10, 1, 1)
    assert (11, 10, 3) == move_fn(G, R, C, 7, 1, 1, 1)

    assert (4, 4, 1) == move_fn(G, R, C, 0, 8, 2, 1)
    assert (0, 8, 0) == move_fn(G, R, C, 4, 4, 3, 1)

    assert (4, 3, 1) == move_fn(G, R, C, 0, 8, 3, 1)
    assert (0, 8, 1) == move_fn(G, R, C, 4, 3, 3, 1)

    assert (11, 15, 2) == move_fn(G, R, C, 0, 11, 0, 1)
    assert (0, 11, 2) == move_fn(G, R, C, 11, 15, 0, 1)

    assert (4, 0, 1) == move_fn(G, R, C, 0, 11, 3, 1)
    assert (0, 11, 1) == move_fn(G, R, C, 4, 0, 3, 1)

    assert (4, 7, 1) == move_fn(G, R, C, 3, 8, 2, 1)
    assert (3, 8, 0) == move_fn(G, R, C, 4, 7, 3, 1)

    assert (8, 15, 2) == move_fn(G, R, C, 3, 11, 0, 1)
    assert (3, 11, 2) == move_fn(G, R, C, 8, 15, 0, 1)

    assert (8, 15, 1) == move_fn(G, R, C, 4, 11, 0, 1)
    assert (4, 11, 2) == move_fn(G, R, C, 8, 15, 3, 1)

    assert (11, 12, 3) == move_fn(G, R, C, 7, 0, 2, 1)
    assert (7, 0, 0) == move_fn(G, R, C, 11, 12, 1, 1)

    assert (11, 11, 3) == move_fn(G, R, C, 7, 0, 1, 1)
    assert (7, 0, 3) == move_fn(G, R, C, 11, 11, 1, 1)

    assert (11, 8, 3) == move_fn(G, R, C, 7, 3, 1, 1)
    assert (7, 3, 3) == move_fn(G, R, C, 11, 8, 1, 1)

    assert (11, 8, 0) == move_fn(G, R, C, 7, 4, 1, 1)
    assert (7, 4, 3) == move_fn(G, R, C, 11, 8, 2, 1)

    assert (8, 8, 0) == move_fn(G, R, C, 7, 7, 1, 1)
    assert (7, 7, 3) == move_fn(G, R, C, 8, 8, 2, 1)

    assert (8, 12, 1) == move_fn(G, R, C, 7, 11, 0, 1)
    assert (7, 11, 2) == move_fn(G, R, C, 8, 12, 3, 1)


def test2_puzzle(G, R, C, move_fn, sectors, QQ):
    # PUZZLE
    assert (150, 0, 0) == move_fn(G, R, C, 0, 50, 3, 1, sectors, QQ)
    assert (0, 50, 1) == move_fn(G, R, C, 150, 0, 2, 1, sectors, QQ)

    assert (199, 0, 0) == move_fn(G, R, C, 0, 99, 3, 1, sectors, QQ)
    assert (0, 99, 1) == move_fn(G, R, C, 199, 0, 2, 1, sectors, QQ)

    assert (199, 0, 3) == move_fn(G, R, C, 0, 100, 3, 1, sectors, QQ)
    assert (0, 100, 1) == move_fn(G, R, C, 199, 0, 1, 1, sectors, QQ)

    assert (199, 49, 3) == move_fn(G, R, C, 0, 149, 3, 1, sectors, QQ)
    assert (0, 149, 1) == move_fn(G, R, C, 199, 49, 1, 1, sectors, QQ)

    assert (149, 99, 2) == move_fn(G, R, C, 0, 149, 0, 1, sectors, QQ)
    assert (0, 149, 2) == move_fn(G, R, C, 149, 99, 0, 1, sectors, QQ)

    assert (150, 49, 2) == move_fn(G, R, C, 149, 50, 1, 1, sectors, QQ)
    assert (149, 50, 3) == move_fn(G, R, C, 150, 49, 0, 1, sectors, QQ)

    assert (50, 50, 0) == move_fn(G, R, C, 100, 0, 3, 1, sectors, QQ)
    assert (100, 0, 1) == move_fn(G, R, C, 50, 50, 2, 1, sectors, QQ)

    assert (99, 50, 0) == move_fn(G, R, C, 100, 49, 3, 1, sectors, QQ)
    assert (100, 49, 1) == move_fn(G, R, C, 99, 50, 2, 1, sectors, QQ)

    assert (49, 149, 2) == move_fn(G, R, C, 100, 99, 0, 1, sectors, QQ)
    assert (100, 99, 2) == move_fn(G, R, C, 49, 149, 0, 1, sectors, QQ)

    assert (149, 0, 0) == move_fn(G, R, C, 0, 50, 2, 1, sectors, QQ)

    assert (100, 0, 0) == move_fn(G, R, C, 49, 50, 2, 1, sectors, QQ)

    assert (100, 49, 1) == move_fn(G, R, C, 99, 50, 2, 1, sectors, QQ)

    assert (49, 50, 0) == move_fn(G, R, C, 100, 0, 2, 1, sectors, QQ)

    assert (0, 50, 0) == move_fn(G, R, C, 149, 0, 2, 1, sectors, QQ)

    assert (0, 50, 1) == move_fn(G, R, C, 150, 0, 2, 1, sectors, QQ)

    assert (0, 149, 1) == move_fn(G, R, C, 199, 49, 1, 1, sectors, QQ)
    assert (150, 49, 2) == move_fn(G, R, C, 149, 50, 1, 1, sectors, QQ)
    assert (199, 49, 2) == move_fn(G, R, C, 149, 99, 1, 1, sectors, QQ)
    assert (50, 99, 2) == move_fn(G, R, C, 49, 100, 1, 1, sectors, QQ)
    assert (99, 99, 2) == move_fn(G, R, C, 49, 149, 1, 1, sectors, QQ)


def solve2_old(lines, type, is_test):
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


def get_cube_type(R, C):
    if R % 4 == 0 and C % 3 == 0:
        Q = R // 4
        assert C // 3 == Q
        return 4, 3, R // 4
    if R % 3 == 0 and C % 4 == 0:
        Q = R // 3
        assert C // 4 == Q
        return 3, 4, R // 3
    return None


def get_map_sectors(G, RR, CC, QQ):
    s = 1
    sectors = []
    for r in range(RR):
        row = []
        for c in range(CC):
            if (r*QQ, c*QQ) in G:
                if G[(r*QQ, c*QQ)] != "":
                    row.append(s)
                    s += 1
                else:
                    row.append(None)
            else:
                row.append(None)
        sectors.append(row)

    return sectors


def get_point_sector(r, c, sectors, QQ):
    rr = r // QQ
    cc = c // QQ
    if 0 <= rr < len(sectors) and 0 <= cc < len(sectors[0]):
        s = sectors[rr][cc]
        return s
    return None


def get_next_point(r, c, d):
    # RIGHT
    if d == 0:
        return (r, c+1)
    # DOWN
    if d == 1:
        return (r+1, c)
    # LEFT
    if d == 2:
        return (r, c-1)
    # UP
    if d == 3:
        return (r-1, c)
    assert False


def get_sector_edge(sectors, s, d, q):
    found = False
    for r in range(len(sectors)):
        for c in range(len(sectors[0])):
            if sectors[r][c] == s:
                found = True
                break
        if found:
            break

    assert found

    top_r, left_c = r * q, c * q

    if d == 0:
        # right column
        rows = []
        for rr in range(q):
            rows.append([(top_r+rr, left_c + (q-1))])
        return rows
    elif d == 1:
        # bottom row
        return [[(top_r + (q-1), left_c+cc) for cc in range(q)]]
    elif d == 2:
        # left column
        rows = []
        for rr in range(q):
            rows.append([(top_r+rr, left_c)])
        return rows
    elif d == 3:
        # top row
        return [[(top_r, left_c+cc) for cc in range(q)]]
    else:
        assert False


def rotate_right(matrix):
    R = len(matrix)
    C = len(matrix[0])

    # create empty with transposed size
    rotated = []
    for _r in range(C):
        row = []
        for _c in range(R):
            row.append(None)
        rotated.append(row)

    for rr in range(R):
        for cc in range(C):
            rotated[cc][R-1-rr] = matrix[rr][cc]

    return rotated


def rotate_left(matrix):
    R = len(matrix)
    C = len(matrix[0])

    # create empty with transposed size
    rotated = []
    for _r in range(C):
        row = []
        for _c in range(R):
            row.append(None)
        rotated.append(row)

    for rr in range(R):
        for cc in range(C):
            rotated[C-1-cc][rr] = matrix[rr][cc]

    return rotated


def rotate_180(matrix):
    # could use rotate_left(rotate_left(matrix)), but it is not fun ;-)
    R = len(matrix)
    C = len(matrix[0])

    # create empty with same size
    rotated = []
    for _r in range(R):
        row = []
        for _c in range(C):
            row.append(None)
        rotated.append(row)

    for rr in range(R):
        for cc in range(C):
            rotated[R-1-rr][C-1-cc] = matrix[rr][cc]

    return rotated


def can_move_to(G, r, c):
    assert (r, c) in G
    ch = G[(r, c)]
    return ch != "#"


def get_descriptor_puzzle(s, d):
    # s-sector
    # d-direction
    # .12
    # .3.
    # 45.
    # 6..

    # dir: 0=R,1=D,2=L,3=R
    # "N"=normal (continuos), L=turn left, R=turn right, F=flip 180
    D = {
        1: [("N", 2), ("N", 3), ("F", 4), ("R", 6)],
        2: [("F", 5), ("R", 3), ("N", 1), ("N", 6)],
        3: [("L", 2), ("N", 5), ("L", 4), ("N", 1)],
        4: [("N", 5), ("N", 6), ("F", 1), ("R", 3)],
        5: [("F", 2), ("R", 6), ("N", 4), ("N", 3)],
        6: [("L", 5), ("N", 2), ("L", 1), ("N", 4)],
    }

    return D[s][d]


def step_puzzle(r, c, d, sectors, QQ):
    current_sector = get_point_sector(r, c, sectors, QQ)
    next_point_r, next_point_c = get_next_point(r, c, d)
    next_sector = get_point_sector(next_point_r, next_point_c, sectors, QQ)
    if next_sector != None:
        # moved within map
        r, c = next_point_r, next_point_c
        # d is not modified
    else:
        operation, next_sector = get_descriptor_puzzle(current_sector, d)
        if operation == "N":
            edge_d = (d + 2) % 4
            edge = get_sector_edge(sectors, next_sector, edge_d, QQ)
            if edge_d == 0 or edge_d == 2:
                r_off = r % QQ
                r, c = edge[r_off][0]
            else:
                c_off = c % QQ
                r, c = edge[0][c_off]
            # d is not modified
        elif operation == "R":
            d = (d + 1) % 4
            edge_d = (d + 2) % 4
            edge = get_sector_edge(sectors, next_sector, edge_d, QQ)
            if edge_d == 0 or edge_d == 2:
                c_off = c % QQ
                r, c = edge[c_off][0]
            else:
                r_off = r % QQ
                r, c = edge[0][r_off]
        elif operation == "L":
            d = (d - 1 + 4) % 4
            edge_d = (d + 2) % 4
            edge = get_sector_edge(sectors, next_sector, edge_d, QQ)
            if edge_d == 0 or edge_d == 2:
                c_off = c % QQ
                r, c = edge[c_off][0]
            else:
                r_off = r % QQ
                r, c = edge[0][r_off]
        elif operation == "F":
            d = (d + 2) % 4
            edge_d = (d + 2) % 4
            edge = get_sector_edge(sectors, next_sector, edge_d, QQ)
            if edge_d == 0 or edge_d == 2:
                r_off = r % QQ
                r, c = edge[(QQ-1)-r_off][0]
            else:
                c_off = c % QQ
                r, c = edge[0][c_off]
        else:
            assert False
    return r, c, d


def move2new_puzzle(G, R, C, r, c, d, i, sectors, QQ):
    while(i > 0):
        r2, c2, d2 = step_puzzle(r, c, d, sectors, QQ)

        if can_move_to(G, r2, c2):
            r, c, d = r2, c2, d2
        else:
            break
        i -= 1
    return r, c, d


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

    RR, CC, QQ = get_cube_type(R, C)
    if is_sample:
        assert RR == 3
        assert CC == 4
        assert QQ == 4
    else:
        assert RR == 4
        assert CC == 3
        assert QQ == 50

    sectors = get_map_sectors(G, RR, CC, QQ)
    assert len(sectors) == RR
    assert len(sectors[0]) == CC
    s = []
    for rr in range(RR):
        for cc in range(CC):
            if sectors[rr][cc] != None:
                s.append(sectors[rr][cc])
                print(sectors[rr][cc], end='')
            else:
                print(".", end='')
        print()
    assert len(s) == 6

    start_sector = get_point_sector(r, c, sectors, QQ)
    assert start_sector == 1

    assert get_next_point(0, 0, 0) == (0, 1)
    assert get_next_point(0, 0, 1) == (1, 0)
    assert get_next_point(0, 0, 2) == (0, -1)
    assert get_next_point(0, 0, 3) == (-1, 0)

    if is_test:
        if is_sample:
            # sectors: q=4
            #   1
            # 234
            #   56
            s = 1
            s1_right_edge = get_sector_edge(sectors, s, 0, QQ)
            assert len(s1_right_edge) == QQ
            assert s1_right_edge[0] == [(0, 11)]
            assert s1_right_edge[1] == [(1, 11)]
            assert s1_right_edge[2] == [(2, 11)]
            assert s1_right_edge[3] == [(3, 11)]

            s1_bottom_edge = get_sector_edge(sectors, s, 1, QQ)
            assert len(s1_bottom_edge) == 1
            assert len(s1_bottom_edge[0]) == QQ
            assert s1_bottom_edge[0] == [(3, 8), (3, 9), (3, 10), (3, 11)]

            s1_left_edge = get_sector_edge(sectors, s, 2, QQ)
            assert len(s1_left_edge) == QQ
            assert s1_left_edge[0] == [(0, 8)]
            assert s1_left_edge[1] == [(1, 8)]
            assert s1_left_edge[2] == [(2, 8)]
            assert s1_left_edge[3] == [(3, 8)]

            s1_top_edge = get_sector_edge(sectors, s, 3, QQ)
            assert len(s1_top_edge) == 1
            assert len(s1_top_edge[0]) == QQ
            assert s1_top_edge[0] == [(0, 8), (0, 9), (0, 10), (0, 11)]

            s6_right_edge = get_sector_edge(sectors, 6, 0, QQ)
            assert s6_right_edge[0][0] == (8, 15)
            assert s6_right_edge[QQ-1][0] == (11, 15)

            s6_bottom_edge = get_sector_edge(sectors, 6, 1, QQ)
            assert s6_bottom_edge[0][0] == (11, 12)
            assert s6_bottom_edge[0][QQ-1] == (11, 15)

            s6_left_edge = get_sector_edge(sectors, 6, 2, QQ)
            assert s6_left_edge[0][0] == (8, 12)
            assert s6_left_edge[QQ-1][0] == (11, 12)

            s6_top_edge = get_sector_edge(sectors, 6, 3, QQ)
            assert s6_top_edge[0][0] == (8, 12)
            assert s6_top_edge[0][QQ-1] == (8, 15)

            # rotate right 90
            m2x3 = [[1, 2, 3], [4, 5, 6]]
            m2x3_r = rotate_right(m2x3)
            assert m2x3_r == [[4, 1], [5, 2], [6, 3]]
            m2x3_rr = rotate_right(m2x3_r)
            assert m2x3_rr == [[6, 5, 4], [3, 2, 1]]
            m2x3_rrr = rotate_right(m2x3_rr)
            assert m2x3_rrr == [[3, 6], [2, 5], [1, 4]]
            m2x3_rrrr = rotate_right(m2x3_rrr)
            assert m2x3_rrrr == m2x3

            # rotate left 90
            m3x2 = [[1, 2], [3, 4], [5, 6]]
            m3x2_l = rotate_left(m3x2)
            assert m3x2_l == [[2, 4, 6], [1, 3, 5]]
            m3x2_ll = rotate_left(m3x2_l)
            assert m3x2_ll == [[6, 5], [4, 3], [2, 1]]
            m3x2_lll = rotate_left(m3x2_ll)
            assert m3x2_lll == [[5, 3, 1], [6, 4, 2]]
            m3x2_llll = rotate_left(m3x2_lll)
            assert m3x2_llll == m3x2

            # rotate 180
            m3_3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            m3_3_180 = rotate_180([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            assert m3_3_180 == [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
            m3_3_360 = rotate_180(m3_3_180)
            assert m3_3_360 == m3_3
        else:

            test2_puzzle(G, R, C, move2new_puzzle, sectors, QQ)

    else:
        pass

    for i in I:
        # move
        if i == "L":
            d = (d+4-1) % 4
        elif i == "R":
            d = (d+1) % 4
        else:
            assert isinstance(i, int)

            if is_sample:
                assert False, "Not implemented"
            else:

                # while(i > 0):
                #     r2, c2, d2 = move2new_puzzle(R, C, r, c, d, sectors, QQ)

                #     if can_move_to(G, r2, c2):
                #         r, c, d = r2, c2, d2
                #     else:
                #         break
                #     i -= 1
                r, c, d = move2new_puzzle(G, R, C, r, c, d, i, sectors, QQ)

    # print(r+1, c+1, d)
    res = 1000*(r+1) + 4 * (c+1) + d
    return res


is_test = False

# hardcoded for my input

print(CRED + "sample:", solve1(lines_sample, "sample", is_test), CEND)  # 6032
print(CGRN + "puzzle:", solve1(lines_puzzle, "puzzle", is_test), CEND)  # 76332

# print(CRED + "sample:", solve2(lines_sample, "sample", is_test), CEND)  # 5031
print(CGRN + "puzzle:", solve2(lines_puzzle, "puzzle", is_test), CEND)  # 144012


stop = datetime.now()
print("duration:", stop - start)
