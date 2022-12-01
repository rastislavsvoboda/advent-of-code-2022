from datetime import datetime

# pypy3.exe .\save.py 1

start = datetime.now()
text = open('1.in').read()


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


data = get_data(text)
print(solve1(data))  # 70509
print(solve2(data))  # 208567

stop = datetime.now()
print("duration:", stop - start)