from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
lines_sample = open('6.ex1').readlines()
lines_puzzle = open('6.in').readlines()


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


print(CRED + "sample:", solve(lines_sample, 1), CEND)  # 7
print(CGRN + "puzzle:", solve(lines_puzzle, 1), CEND)  # 1109

print(CRED + "sample:", solve(lines_sample, 2), CEND)  # 19
print(CGRN + "puzzle:", solve(lines_puzzle, 2), CEND)  # 3965

stop = datetime.now()
print("duration:", stop - start)
