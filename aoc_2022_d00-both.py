from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

# pypy3.exe .\save.py 0

start = datetime.now()
lines_sample = open('0.ex1').readlines()
lines_puzzle = open('0.in').readlines()
# text = open('0.in').read()


# def get_data(text):
#     data = []
#     for grp in text.split('\n\n'):
#         entries = []
#         for row in grp.split():
#             entries.append(row)
#         data.append(parse_entry(entries))
#     return data

# def parse_entry(entries):
#     # answers = []
#     # for entry in entries:
#     #     answers.append(set(entry))
#     # return answers
#     return entries

def solve1(lines):
    res = 0

    for line in lines:
        line = line.strip()
        words = line.split()
        nums = re.findall(r"[+-]?\d+", line)
        print(line)
        # print(words)
        # print(nums)

        res += 1

    return res


# def solve1_t(text):
#     res = 0

#     data = get_data(text)
#     for d in data:
#         print(d)
#         res += 1

#     return res


print(CRED + "sample:", solve1(lines_sample), CEND)  #
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  #
# print(solve1_t(text))  #
# print(solve2(lines))  #

stop = datetime.now()
print("duration:", stop - start)
