from datetime import datetime

start = datetime.now()
lines = open('3.in').readlines()
# lines = open('3.ex1').readlines()


def priority(c):
    if c.isupper():
        res = ord(c) - ord('A') + 27
    else:
        res = ord(c) - ord('a') + 1
    return res


def solve1(lines):
    COMP = []
    for line in lines:
        line = line.strip()
        half = len(line) // 2
        p1 = line[:half]
        p2 = line[half:]
        C1 = set([c for c in p1])
        C2 = set([c for c in p2])
        common = C1.intersection(C2)
        # print(common)
        assert len(common) == 1
        COMP.append(common.pop())

    res = sum([priority(c) for c in COMP])

    return res


def solve2(lines):
    COMP = []
    i = 0
    while (i < len(lines)):
        line1 = lines[i].strip()
        i += 1
        line2 = lines[i].strip()
        i += 1
        line3 = lines[i].strip()
        i += 1
        C1 = set([c for c in line1])
        C2 = set([c for c in line2])
        C3 = set([c for c in line3])
        common = C1.intersection(C2).intersection(C3)
        # print(common)
        assert len(common) == 1
        COMP.append(common.pop())

    res = sum([priority(c) for c in COMP])

    return res


print(solve1(lines))  # 8298
print(solve2(lines))  # 2708

stop = datetime.now()
print("duration:", stop - start)
