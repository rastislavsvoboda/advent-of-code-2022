from collections import deque, defaultdict, Counter
import itertools
import re
from typing import TypeVar, Generator, Iterable, Tuple, List

_T = TypeVar("T")


def pairwise(elements: Iterable[_T]) -> Generator[Tuple[_T, _T], None, None]:
    elements_iter = iter(elements)
    last_element = next(elements_iter)
    for element in elements_iter:
        yield (last_element, element)
        last_element = element


def all_pairs(elements: Iterable[_T]) -> Generator[Tuple[_T, _T], None, None]:
    elements_list = list(elements)
    for i in range(len(elements_list)):
        for j in range(i + 1, len(elements_list)):
            yield (elements_list[i], elements_list[j])


def all_tuples(elements: Iterable[_T]) -> Generator[Tuple[_T, _T], None, None]:
    elements_list = list(elements)
    for i in range(len(elements_list)):
        for j in range(len(elements_list)):
            if j == i: continue
            yield (elements_list[i], elements_list[j])


def chunk(elements, count):
    elements_list = list(elements)
    for i in range(0, len(elements_list), count):
        yield elements_list[i:i + count]


def get_all_nums(line):
    return list(map(int, re.findall(r"[+-]?\d+", line.strip())))


def neighbours4(r, c):
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        rr = r + dr
        cc = c + dc
        yield (rr, cc)


def neighbours8(r, c):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if not (dr == 0 and dc == 0):
                rr = r + dr
                cc = c + dc
                yield (rr, cc)


def neighbours9(r, c):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            rr = r + dr
            cc = c + dc
            yield (rr, cc)


def rotate_r(grid):
    R = len(grid)
    C = len(grid[0])

    rotated_grid = []
    for rr in range(C):
        row = []
        for cc in range(R):
            row.append("?")
        rotated_grid.append(row)

    for r in range(R):
        for c in range(C):
            rotated_grid[c][R - 1 - r] = grid[r][c]

    return rotated_grid


def rotate_l(grid):
    R = len(grid)
    C = len(grid[0])

    rotated_grid = []
    for rr in range(C):
        row = []
        for cc in range(R):
            row.append("?")
        rotated_grid.append(row)

    for r in range(R):
        for c in range(C):
            rotated_grid[C - 1 - c][r] = grid[r][c]

    return rotated_grid


def flip_h(grid):
    R = len(grid)
    C = len(grid[0])

    flipped_grid = []
    for rr in range(R):
        row = []
        for cc in range(C):
            row.append("?")
        flipped_grid.append(row)

    for r in range(R):
        for c in range(C):
            flipped_grid[R - 1 - r][c] = grid[r][c]

    return flipped_grid


def flip_v(grid):
    R = len(grid)
    C = len(grid[0])

    flipped_grid = []
    for rr in range(R):
        row = []
        for cc in range(C):
            row.append("?")
        flipped_grid.append(row)

    for r in range(R):
        for c in range(C):
            flipped_grid[r][C - 1 - c] = grid[r][c]

    return flipped_grid

def sign(x):
    return -1 if x < 0 else 1 if x > 0 else 0

