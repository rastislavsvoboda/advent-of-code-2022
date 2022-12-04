from datetime import datetime
import re

start = datetime.now()
lines = open('4.in').readlines()
# lines = open('4.ex1').readlines()


def in_range(s1, e1, s2, e2):
    # s2-e2 in range of s1-e2
    return s1 <= s2 <= e1 and s1 <= e2 <= e1


def overlap(s1, e1, s2, e2):
    # s2-e2 overlap s1-e2
    return s1 <= s2 <= e1 or s1 <= e2 <= e1


def solve(lines):
    res1 = 0
    res2 = 0

    for line in lines:
        line = line.strip()
        nums = re.findall(r"\d+", line)
        N = [int(n) for n in nums]
        a, b, c, d = N
        # print(N)

        if in_range(a, b, c, d) or in_range(c, d, a, b):
            res1 += 1

        if overlap(a, b, c, d) or overlap(c, d, a, b):
            res2 += 1

    return res1, res2


print(solve(lines))  # 487, 849

stop = datetime.now()
print("duration:", stop - start)
