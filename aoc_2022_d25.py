from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('25.ex1').readlines()
lines_puzzle = open('25.in').readlines()


def parse_SNAFU(s):
    num = 0
    for i, ch in enumerate(reversed(s.strip())):
        n = 0
        if ch == "0":
            n = 0
        elif ch == "1":
            n = 1
        elif ch == "2":
            n = 2
        elif ch == "-":
            n = -1
        elif ch == "=":
            n = -2
        else:
            assert False, "incorrect character"
        num += n * pow(5, i)
    return num


def generate_SNAFU(num):
    s = ""
    while True:
        div = num // 5
        mod = num % 5

        if mod == 0:
            s += "0"
        elif mod == 1:
            s += "1"
        elif mod == 2:
            s += "2"
        elif mod == 3:
            s += "="
            div += 1
        elif mod == 4:
            s += "-"
            div += 1

        if div == 0:
            break
        
        num = div

    return s[::-1]


def solve1(lines):
    total = sum(map(parse_SNAFU, lines))
    res = generate_SNAFU(total)
    assert parse_SNAFU(res) == total
    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 2=-1=0
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 20=022=21--=2--12=-2

stop = datetime.now()
print("duration:", stop - start)
