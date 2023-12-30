from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('1.in').read()
text_sample = open('1.ex1').read()


def get_data(text):
    data = []
    for grp in text.split('\n\n'):
        entries = []
        for row in grp.split():
            entries.append(row)
        data.append(parse_entry(entries))
    return data


def parse_entry(entries):
    calories = [int(e) for e in entries]
    return calories


def solve1(data):
    totals = [sum(d) for d in data]
    res = max(totals) 
    return res


def solve2(data):
    totals = [sum(d) for d in data]
    res = sum(sorted(totals)[-3:])
    return res


data_sample = get_data(text_sample)
data_puzzle = get_data(text_puzzle)

print(CRED + "sample:", solve1(data_sample), CEND)  # 24000
print(CGRN + "puzzle:", solve1(data_puzzle), CEND)  # 70509
print(CRED + "sample:", solve2(data_sample), CEND)  # 45000
print(CGRN + "puzzle:", solve2(data_puzzle), CEND)  # 208567

stop = datetime.now()
print("duration:", stop - start)