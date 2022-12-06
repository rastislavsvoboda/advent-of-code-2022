from datetime import datetime

start = datetime.now()
lines = open('6.in').readlines()
lines = open('6.ex1').readlines()


def solve(lines, part):
    res = 0

    if part == 1:
        length = 4
    else:
        length = 14

    for line in lines:
        line = line.strip()
        for i in range(len(line)-length+1):
            marker = set(list(line[i:i+length]))
            if len(marker) == length:
                res = i+length
                break

    return res


print(solve(lines, 1))  # 1109
print(solve(lines, 2))  # 3965

stop = datetime.now()
print("duration:", stop - start)
