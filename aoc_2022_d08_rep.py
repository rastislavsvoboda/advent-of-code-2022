from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('8.in').read()
text_sample = open('8.ex1').read()


def is_visible(r, c, D):
    R = len(D)
    C = len(D[0])
    cur = D[r][c]

    if r == 0 or r == R - 1 or c == 0 or c == C - 1:
        return True

    vis_up = True
    for rr in range(r - 1, -1, -1):
        if D[rr][c] >= cur:
            vis_up = False
            break

    vis_down = True
    for rr in range(r + 1, R, 1):
        if D[rr][c] >= cur:
            vis_down = False
            break

    vis_left = True
    for cc in range(c - 1, -1, -1):
        if D[r][cc] >= cur:
            vis_left = False
            break

    vis_right = True
    for cc in range(c + 1, C, 1):
        if D[r][cc] >= cur:
            vis_right = False
            break

    return vis_up or vis_down or vis_left or vis_right


def get_score(r, c, D):
    R = len(D)
    C = len(D[0])
    cur = D[r][c]

    cnt_up = 0
    for rr in range(r - 1, -1, -1):
        cnt_up += 1
        if D[rr][c] >= cur:
            break

    cnt_down = 0
    for rr in range(r + 1, R, 1):
        cnt_down += 1
        if D[rr][c] >= cur:
            break

    cnt_left = 0
    for cc in range(c - 1, -1, -1):
        cnt_left += 1
        if D[r][cc] >= cur:
            break

    cnt_right = 0
    for cc in range(c + 1, C, 1):
        cnt_right += 1
        if D[r][cc] >= cur:
            break

    return cnt_up * cnt_down * cnt_left * cnt_right


def solve(text, part):
    D = []
    for line in text.split("\n"):
        D.append([int(n) for n in list(line)])

    R = len(D)
    C = len(D[0])

    res = 0
    for r in range(R):
        for c in range(C):
            if part == 1:
                if is_visible(r, c, D):
                    res += 1
            elif part == 2:
                score = get_score(r, c, D)
                res = max(res, score)

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 21
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 1812

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 8
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 315495

stop = datetime.now()
print("duration:", stop - start)
