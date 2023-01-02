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

RES_ORE=0
RES_CLA=1
RES_OBS=2
RES_GEO=3
ROB_ORE=4
ROB_CLA=5
ROB_OBS=6
ROB_GEO=7


def can_build(COS, game_data, robot):
    needed = COS[robot]
    for res in needed.keys():
        val = needed[res]
        if game_data[res] < val:
            return False

    return True


def add_data(data1, data2):
    a1,b1,c1,d1,e1,f1,g1,h1 = data1
    a2,b2,c2,d2,e2,f2,g2,h2 = data2
    return (a1+a2,b1+b2,c1+c2,d1+d2,e1+e2,f1+f2,g1+g2,h1+h2)

def get_game(COS, game_data, t):
    
    valuable = "geode"
    valuable = "clay"

    memo = {}

    def dp(game_data, t):
        if t == 0:
            return (0,0,0,0,0,0,0,0)
        
        if not (game_data, t) in memo:
            max_geode = 0
            answer = None

            # for new_robot in [ROB_CLA,ROB_OBS,ROB_GEO]:
            #     if can_build(COS, game_data, new_robot):
            #         new_game_data = game_data

            #         costs = COS[new_robot]
            #         for r in costs:
            #             new_game_data[r] -= costs[r]

            #         new_game_data[new_robot] += 1

            #         answer = dp(new_game_data, t-1)

            new_ore = game_data[ROB_ORE] * t
            new_cla = game_data[ROB_CLA] * t
            new_obs = game_data[ROB_OBS] * t
            new_geo = game_data[ROB_GEO] * t
            turn_data = (new_ore,new_cla,new_obs,new_geo,0,0,0,0)

            new_game = add_data(game_data,(new_ore,new_cla,new_obs,new_geo,0,0,0,0))

            # answer = add_data(answer,(new_ore,new_cla,new_obs,new_geo,0,0,0,0))

            answer = add_data(turn_data, dp(game_data, t-1))

            memo[(game_data, t)] = answer

        return memo[(game_data, t)]

    return dp(game_data, t)    



def play(b):
    ROB=defaultdict(int)
    COS=defaultdict(int)
    RES=defaultdict(int)

    COS[ROB_ORE]={RES_ORE: b[1]}
    COS[ROB_CLA]={RES_ORE: b[2]}
    COS[ROB_OBS]={RES_ORE: b[3], RES_CLA: b[4]}
    COS[ROB_GEO]={RES_ORE: b[5], RES_OBS: b[6]}

# RES_ORE=0
# RES_CLA=1
# RES_OBS=2
# RES_GEO=3
# ROB_ORE=4
# ROB_CLA=5
# ROB_OBS=6
# ROB_GEO=7

    start_data=(0,0,0,0,1,0,0,0)


    RES=defaultdict(int)

    # res = get_game(ROB, COS, RES, 24)
    end_data = get_game(COS, start_data, 3)

    result = end_data[RES_GEO]
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
