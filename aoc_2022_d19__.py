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

RES_ORE = 0
RES_CLA = 1
RES_OBS = 2
RES_GEO = 3
ROB_ORE = 4
ROB_CLA = 5
ROB_OBS = 6
ROB_GEO = 7


def can_build(COS, game_data, robot):
    needed = COS[robot]
    for res in needed.keys():
        val = needed[res]
        if game_data[res] < val:
            return False

    return True


def add_data(data1, data2):
    a1, b1, c1, d1, e1, f1, g1, h1 = data1
    a2, b2, c2, d2, e2, f2, g2, h2 = data2
    return (a1+a2, b1+b2, c1+c2, d1+d2, e1+e2, f1+f2, g1+g2, h1+h2)

def sub_data(data1, data2):
    a1, b1, c1, d1, e1, f1, g1, h1 = data1
    a2, b2, c2, d2, e2, f2, g2, h2 = data2
    return (a1-a2, b1-b2, c1-c2, d1-d2, e1-e2, f1-f2, g1-g2, h1-h2)


def get_game(COS, game_data, t):

    valuable = RES_GEO
    # valuable = RES_CLA

    memo = {}

    def dp(game_data, t):
        if t == 0:
            return (0, 0, 0, 0, 0, 0, 0, 0)

        if not (game_data, t) in memo:
            max_geode = 0
            answer = None

            for new_robot in [ROB_ORE,ROB_CLA,ROB_OBS,ROB_GEO]:
                if can_build(COS, game_data, new_robot):
                    new_ore = game_data[ROB_ORE]
                    new_cla = game_data[ROB_CLA]
                    new_obs = game_data[ROB_OBS]
                    new_geo = game_data[ROB_GEO]
                    new_ore_rob = 1 if new_robot == ROB_ORE else 0
                    new_cla_rob = 1 if new_robot == ROB_CLA else 0
                    new_obs_rob = 1 if new_robot == ROB_OBS else 0
                    new_geo_rob = 1 if new_robot == ROB_GEO else 0

                    turn_data = (new_ore, new_cla, new_obs, new_geo, new_ore_rob, new_cla_rob, new_obs_rob, new_geo_rob)

                    costs = COS[new_robot]
                    turn_data = sub_data(turn_data, (costs[RES_ORE],costs[RES_CLA],costs[RES_OBS],costs[RES_GEO],0,0,0,0))

                    new_game = add_data(
                        game_data,turn_data)

                    build_answer = add_data(turn_data, dp(new_game, t-1))
                    if build_answer[valuable] > max_geode:
                        max_geode = build_answer[valuable]
                        answer = build_answer

            new_ore = game_data[ROB_ORE]
            new_cla = game_data[ROB_CLA]
            new_obs = game_data[ROB_OBS]
            new_geo = game_data[ROB_GEO]
            turn_data = (new_ore, new_cla, new_obs, new_geo, 0, 0, 0, 0)

            new_game = add_data(
                game_data, (new_ore, new_cla, new_obs, new_geo, 0, 0, 0, 0))

            no_build_answer = add_data(turn_data, dp(new_game, t-1))

            if no_build_answer[valuable] > max_geode:
                max_geode = no_build_answer[valuable]
                answer = no_build_answer

            memo[(game_data, t)] = answer

        return memo[(game_data, t)]

    return dp(game_data, t)


def play(b):
    COS = defaultdict(int)

    COS[ROB_ORE] = {RES_ORE: b[1], RES_CLA:0, RES_OBS:0, RES_GEO:0}
    COS[ROB_CLA] = {RES_ORE: b[2], RES_CLA:0, RES_OBS:0, RES_GEO:0}
    COS[ROB_OBS] = {RES_ORE: b[3], RES_CLA: b[4], RES_OBS:0, RES_GEO:0}
    COS[ROB_GEO] = {RES_ORE: b[5], RES_OBS: b[6], RES_CLA:0, RES_GEO:0}

# RES_ORE=0
# RES_CLA=1
# RES_OBS=2
# RES_GEO=3
# ROB_ORE=4
# ROB_CLA=5
# ROB_OBS=6
# ROB_GEO=7

    start_data = (0, 0, 0, 0, 1, 0, 0, 0)

    RES = defaultdict(int)

    # res = get_game(ROB, COS, RES, 24)
    end_data = get_game(COS, start_data, 24)

    result = end_data[RES_GEO]
    return result


def solve1(lines):
    res = 0


# Blueprint 1:
#   Each ore robot costs 4 ore.
#   Each clay robot costs 2 ore.
#   Each obsidian robot costs 3 ore and 14 clay.
#   Each geode robot costs 2 ore and 7 obsidian.

    B = []
    for line in lines:
        line = line.strip()
        nums = [int(x) for x in re.findall(r"[+-]?\d+", line)]
        B.append(nums)

    RES = []
    for (i, b) in enumerate(B):
        geodes = play(b)
        RES.append(i+1 * geodes)

    res = sum(RES)

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  #
# print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  #

stop = datetime.now()
print("duration:", stop - start)
