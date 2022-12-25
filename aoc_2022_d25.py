from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('25.ex1').readlines()
lines_puzzle = open('25.in').readlines()


def parse_SNAFU(s):
    num = 0
    for i, ch in enumerate(reversed(s)):
        x = 0
        if ch == "0":
            x = 0
        elif ch == "1":
            x = 1
        elif ch == "2":
            x = 2
        elif ch == "-":
            x = -1
        elif ch == "=":
            x = -2
        else:
            assert False
        num += x * pow(5, i)
    return num


def generate_SNAFU(num):
    d = 5
    s = ""
    x = num
    while True:
        x = num // d
        y = num % d

        if y == 0:
            s += "0"
        elif y == 1:
            s += "1"
        elif y == 2:
            s += "2"
        elif y == 3:
            s += "="
            x += 1
        elif y == 4:
            s += "-"
            x += 1
        else:
            assert False

        if x == 0:
            break
        num = x

    return s[::-1]


def solve1(lines):
    sum = 0
    for line in lines:
        line = line.strip()
        sum += parse_SNAFU(line)

    res = generate_SNAFU(sum)

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 2=-1=0
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 20=022=21--=2--12=-2

stop = datetime.now()
print("duration:", stop - start)
