from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('25.ex1').readlines()
lines_puzzle = open('25.in').readlines()


def parse_SNAFU(s):
    D = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
    num = 0
    p = 1
    for ch in reversed(s.strip()):
        num += D[ch] * p
        p *= 5
    return num


def test_parse_SNAFU():
    data = [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0")
    ]

    for expected, input in data:
        assert expected == parse_SNAFU(input)


def generate_SNAFU(num):
    D = {0: ('0', 0), 1: ('1', 0), 2: ('2', 0), 3: ('=', 1), 4: ('-', 1)}
    s = ""
    while True:
        div = num // 5
        mod = num % 5
        char, add = D[mod]
        s += char
        div += add
        if div == 0:
            break
        num = div
    return s[::-1]


def test_generate_SNAFU():
    data = [
        ("1=-0-2",     1747),
        ("12111",      906),
        ("2=0=",      198),
        ("21",       11),
        ("2=01",      201),
        ("111",       31),
        ("20012",     1257),
        ("112",       32),
        ("1=-1=",      353),
        ("1-12",      107),
        ("12",        7),
        ("1=",        3),
        ("122",       37),
    ]
    for expected, input in data:
        assert expected == generate_SNAFU(input)


def solve1(lines):
    test_parse_SNAFU()
    test_generate_SNAFU()

    total = sum(map(parse_SNAFU, lines))
    res = generate_SNAFU(total)
    assert parse_SNAFU(res) == total
    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 2=-1=0
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 20=022=21--=2--12=-2

stop = datetime.now()
print("duration:", stop - start)
