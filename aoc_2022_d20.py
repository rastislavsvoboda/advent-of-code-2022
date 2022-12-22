from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('20.ex1').readlines()
lines_puzzle = open('20.in').readlines()


def find_zero(A, zero_i):
    zero = A.index((zero_i, 0))
    L = len(A)
    x1000 = (zero + 1000) % L
    x2000 = (zero + 2000) % L
    x3000 = (zero + 3000) % L
    # print(A[x1000][1], A[x2000][1], A[x3000][1])
    res = A[x1000][1]+A[x2000][1]+A[x3000][1]
    return res


def solve(lines, part):
    res = 0
    A = []
    B = []
    zero_i = None
    KEY = 811589153

    repeat = 1 if part == 1 else 10
    multiply = 1 if part == 1 else KEY

    for i, line in enumerate(lines):
        line = line.strip()
        n = [int(n) for n in re.findall(r"[+-]?\d+", line)][0]
        A.append((i, n*multiply))
        B.append((i, n*multiply))
        if n == 0:
            zero_i = i

    L = len(A)

    for _ in range(repeat):
        for (j, a) in A:
            assert len(B) == L
            i = B.index((j, a))
            if a == 0:
                continue
            # cut at item and swap, so item is virtually first/last            
            p_left = B[:i]
            p_right = B[i+1:]
            p_joined = p_right + p_left
            aa = a % (L-1)
            if aa == 0:
                continue          
            # cut and stick item in place  
            p_left = p_joined[:aa]
            p_right = p_joined[aa:]
            B = p_left + [(j, a)] + p_right

    res = find_zero(B, zero_i)

    return res


print(CRED + "sample:", solve(lines_sample, 1), CEND)  # 3
print(CGRN + "puzzle:", solve(lines_puzzle, 1), CEND)  # 5962

print(CRED + "sample:", solve(lines_sample, 2), CEND)  # 1623178306
print(CGRN + "puzzle:", solve(lines_puzzle, 2), CEND)  # 9862431387256

stop = datetime.now()
print("duration:", stop - start)
