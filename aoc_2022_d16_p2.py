from datetime import datetime
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('16.ex1').readlines()
lines_puzzle = open('16.in').readlines()


def most_preasure(minutes, n_players, I, R, M, G):
    memo = {}
    start_node = I['AA']

    def dp(current_node: int, open_valves: int, time_left: int, n_players: int):
        if n_players == 0:
            return 0

        if time_left <= 0:
            return dp(start_node, open_valves, minutes, n_players - 1)

        if not (current_node, open_valves, time_left, n_players) in memo:
            answer = 0
            if not (open_valves & (1 << current_node)) and R[M[current_node]] > 0:
                open_valve_score = R[M[current_node]] * (time_left - 1)
                answer = max(answer, open_valve_score + dp(current_node,
                             open_valves | 1 << current_node, time_left - 1, n_players))
            answer = max(answer, max([dp(I[neighbor], open_valves, time_left - 1, n_players)
                                      for neighbor in G[M[current_node]]]))
            memo[(current_node, open_valves, time_left, n_players)] = answer

        return memo[(current_node, open_valves, time_left, n_players)]

    return dp(start_node, 0, minutes, n_players)


def solve2(lines):
    V = []
    G = {}
    R = {}
    M = {}
    I = {}
    for line in lines:
        line = line.strip()
        words = line.split()
        nums = re.findall(r"[+-]?\d+", words[4])
        v = words[1]
        r = int(nums[0])
        others = [o[:2] for o in words[9:]]
        G[v] = others
        R[v] = r
        V.append(v)

    for i, v in enumerate(sorted(V)):
        M[i] = v
        I[v] = i

    res = most_preasure(26, 2, I, R, M, G)

    return res


print(CRED + "sample:", solve2(lines_sample), CEND)  # 1707
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 2556

stop = datetime.now()
print("duration:", stop - start)
