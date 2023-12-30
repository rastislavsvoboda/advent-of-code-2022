from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('3.in').read()
text_sample = open('3.ex1').read()


def priority(ch):
    if "a" <= ch <= "z":
        return ord(ch) - ord("a") + 1
    if "A" <= ch <= "Z":
        return ord(ch) - ord("A") + 27
    assert False, ch


def to_chars(s):
    return set([c for c in s])


def solve1(text):
    res = 0
    for line in text.split("\n"):
        n = len(line)
        assert n % 2 == 0
        r1chars = to_chars(line[:n // 2])
        r2chars = to_chars(line[n // 2:])
        common = r1chars & r2chars
        assert len(common) == 1
        res += priority(common.pop())

    return res


def solve2(text):
    res = 0
    L = [line for line in text.split("\n")]
    for i in range(0, len(L), 3):
        r1chars = to_chars(L[i])
        r2chars = to_chars(L[i + 1])
        r3chars = to_chars(L[i + 2])
        common = r1chars & r2chars & r3chars
        assert len(common) == 1
        res += priority(common.pop())

    return res


print(CRED + "sample:", solve1(text_sample), CEND)  # 157
print(CGRN + "puzzle:", solve1(text_puzzle), CEND)  # 8298

print(CRED + "sample:", solve2(text_sample), CEND)  # 70
print(CGRN + "puzzle:", solve2(text_puzzle), CEND)  # 2708

stop = datetime.now()
print("duration:", stop - start)
