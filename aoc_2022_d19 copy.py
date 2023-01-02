from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('19.ex1').readlines()
lines_puzzle = open('19.in').readlines()
# text = open('19.in').read()


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


def get_geode(ROB, COS, RES, t, ):
    ROB=defaultdict(int)
    COS=defaultdict(int)
    RES=defaultdict(int)

    if t <= 0:
        return 0


    while t > 0:
        print("minute", 24-t)

        # build
        new_robots=[]
        for r in ["geode", "obsidian", "clay"]:
            can_build = True
            needed = COS[r]
            for res in needed.keys():
                val = needed[res]
                if RES[res] < val:
                    can_build = False
                    break
            if can_build:

                # path 1 - to build
                p1 = 0
                ROB2 = ROB.copy()
                COS2 = COS.copy()
                RES2 = RES.copy()
                new_robots2 = new_robots.copy()
                new_robots2.append(r)

                costs = COS2[r]
                for c in costs.keys():
                    val =  costs[c]
                    RES2[c] -= val
                    print(res, val, "; ", end='')


                get_geode(ROB2, COS2, RES2, t-1)
                
                # new_robots.append(r)
                # print("building", r)
                # print("spending:", end='')
                # costs = COS[r]
                # for c in costs.keys():
                #     val =  costs[c]
                #     RES[c] -= val
                #     print(res, val, "; ", end='')
                # print()

                
                # path 2 - not to build
                p2 = 0
                
                res = max(p1, p2)



        # collect
        for r in ROB.keys():
            RES[r] += ROB[r]
            print("collected", r, RES[r])

        for r in new_robots:
            ROB[r] += 1
            print("ready", r, ROB[r])

        t -= 1



def play(b):
    ROB=defaultdict(int)
    COS=defaultdict(int)
    RES=defaultdict(int)

    COS["ore"]={"ore": b[1]}
    COS["clay"]={"ore": b[2]}
    COS["obsidian"]={"ore": b[3], "clay": b[4]}
    COS["geode"]={"ore": b[5],"obsidian": b[6]}

    ROB["ore"] = 1

    RES=defaultdict(int)

    resources = get_geode(ROB, COS, RES, 24)

    res = resources["geode"]
    return res

def solve1(lines):
    res = 0



# Blueprint 1:
#   Each ore robot costs 4 ore.
#   Each clay robot costs 2 ore.
#   Each obsidian robot costs 3 ore and 14 clay.
#   Each geode robot costs 2 ore and 7 obsidian.

    B=[]
    for line in lines:
        line = line.strip()
        nums =[int(x) for x in re.findall(r"[+-]?\d+", line)]
        B.append(nums)

    RES=[]
    for (i,b) in enumerate(B):
        geodes = play(b)
        RES.append(i+1 * geodes)

    res = sum(RES)

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
