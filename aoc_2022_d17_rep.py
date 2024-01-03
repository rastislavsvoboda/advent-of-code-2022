from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('17.in').read()
text_sample = open('17.ex1').read()


def gen_piece(id, max_level):
    bottom = max_level + 3 + 1
    offset = 2
    if id == 0:
        # -
        return [(bottom, offset + 0),
                (bottom, offset + 1),
                (bottom, offset + 2),
                (bottom, offset + 3)]
    if id == 1:
        # +
        return [(bottom, offset + 1),
                (bottom + 1, offset + 0),
                (bottom + 1, offset + 1),
                (bottom + 1, offset + 2),
                (bottom + 2, offset + 1)]
    if id == 2:
        # ┘
        return [(bottom, offset + 0),
                (bottom, offset + 1),
                (bottom, offset + 2),
                (bottom + 1, offset + 2),
                (bottom + 2, offset + 2)]
    if id == 3:
        # |
        return [(bottom, offset + 0),
                (bottom + 1, offset + 0),
                (bottom + 2, offset + 0),
                (bottom + 3, offset + 0)]
    if id == 4:
        # ■
        return [(bottom, offset + 0),
                (bottom, offset + 1),
                (bottom + 1, offset + 0),
                (bottom + 1, offset + 1)]
    assert False


def collides(piece, B):
    return len(B & set(piece)) > 0


def try_push(push, piece, B):
    if push == ">":
        new_piece = [(r, c + 1) for (r, c) in piece]
        if any([c > 6 for (r, c) in new_piece]) or collides(new_piece, B):
            return False, piece
        return True, new_piece
    elif push == "<":
        new_piece = [(r, c - 1) for (r, c) in piece]
        if any([c < 0 for (r, c) in new_piece]) or collides(new_piece, B):
            return False, piece
        return True, new_piece
    else:
        assert False


def try_fall(piece, B):
    new_piece = [(r - 1, c) for (r, c) in piece]
    if any([r <= 0 for (r, c) in new_piece]) or collides(new_piece, B):
        return False, piece
    return True, new_piece


def solve(text, part):
    I = list(text.strip())
    cnt = 0
    max_level = 0
    p = 0
    i = 0
    B = set()
    N = 2022 if part == 1 else 1000000000000

    # for part 2
    # number of rows to detect a cycle
    SNAP_CNT = 200
    CYCLES = defaultdict(list)
    bonus = 0

    while cnt < N:
        cnt += 1
        piece = gen_piece(p, max_level)
        p = (p + 1) % 5
        is_falling = True
        while is_falling:
            push = I[i]
            i = (i + 1) % len(I)
            was_pushed, piece = try_push(push, piece, B)
            is_falling, piece = try_fall(piece, B)
            if not is_falling:
                for pos in piece:
                    B.add(pos)
                max_level = max(max_level, max([r for (r, c) in piece]))

        if part == 2:
            # try to snapshot top x rows to detect a cycle
            if max_level > SNAP_CNT and bonus == 0:
                top_pieces = tuple(sorted([(r - max_level, c) for (r, c) in B if r > max_level - SNAP_CNT]))
                key = (top_pieces, p, i)

                if key in CYCLES:
                    prev_cnt, prev_level = CYCLES[key]
                    delta_cnt = cnt - prev_cnt
                    delta_level = max_level - prev_level
                    reps = (N - cnt) // delta_cnt
                    cnt += reps * delta_cnt
                    bonus = reps * delta_level

                CYCLES[key] = (cnt, max_level)

    res = max_level + bonus

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 3068
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 3202

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 1514285714288
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 1591977077352

stop = datetime.now()
print("duration:", stop - start)
