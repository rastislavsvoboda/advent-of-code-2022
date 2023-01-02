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


def can_build(COS, RES, r):
    needed = COS[r]
    for res in needed.keys():
        val = needed[res]
        if RES[res] < val:
            return False

    return True


def add_dict(d1,d2):
    res = d1.copy()
    for k in d2.keys():
        res[k] += d2[k]

    return res

def sub_dict(d1,d2):
    res = d1.copy()
    for k in d2.keys():
        res[k] -= d2[k]

    return res


def get_game(ROB, COS, RES, t):
    # ROB=defaultdict(int)
    # COS=defaultdict(int)
    # RES=defaultdict(int)

    valuable = "geode"
    valuable = "clay"

    memo = {}

    def dp(ROB, RES, t):
        if t == 0:
            return ({"ore":0, "clay":0, "obsidian": 0, "geode":0}, {"ore":0, "clay":0, "obsidian": 0, "geode":0})
        
        key_rob = (ROB["ore"], ROB["clay"], ROB["obsidian"], ROB["geode"])
        key_res = (RES["ore"], RES["clay"], RES["obsidian"], RES["geode"])

        if t == 2:
            pass

        if t == 3:
            pass

        if not (key_rob, key_res, t) in memo:
            max_geode = 0
            answer = None

            for new_robot in ["clay", "obsidian", "geode"]:
                gain_res = {"ore":0, "clay":0, "obsidian": 0, "geode":0}
                gain_rob = {"ore":0, "clay":0, "obsidian": 0, "geode":0}

                    # new_res = RES.copy()
                    # for r in ROB:
                    #     new_res[r] += ROB[r]


                if can_build(COS, RES, new_robot):



                    # new_res = RES.copy()
                    # for r in ROB:
                    #     new_res[r] += ROB[r]

                    # costs = COS[new_robot]
                    # for c in costs.keys():
                    #     val =  costs[c]
                    #     new_res[c] -= val

                    # new_rob = ROB.copy()
                    # new_rob[new_robot] += 1
                    # gain_rob[new_robot] += 1

                    # gain_res[new_robot] += 1
                    # costs = COS[r]
                    # for c in costs.keys():
                    #     val =  costs[c]
                    #     gain_res[c] -= val                    

                    # ret_res, ret_rob = dp(new_rob, new_res, t-1)
                    # ret_res = add_dict(ret_res, gain_res)
                    # ret_rob = add_dict(ret_rob, gain_rob)
                    # sum_res = RES.copy()

                    if (ret_res[valuable] > max_geode):
                        answer = ret_res, ret_rob
                        max_geode = ret_res[valuable]

            new_rob = ROB.copy()

            new_res = RES.copy()
            for r in ROB:
                new_res[r] += ROB[r]

            ret_res, ret_rob = dp(new_rob, new_res, t-1)
            if (ret_res[valuable] > max_geode):
                answer = ret_res, ret_rob
                max_geode = ret_res[valuable]

            memo[(key_rob, key_res, t)] = answer

        return memo[(key_rob, key_res, t)]

    return dp(ROB, RES, t)    



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

    # res = get_game(ROB, COS, RES, 24)
    res,rob= get_game(ROB, COS, RES, 3)

    result = res["geode"]
    return result

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
# print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  #
# print(solve1_t(text))  #
# print(solve2(lines))  #

stop = datetime.now()
print("duration:", stop - start)
