import heapq
from datetime import datetime
from aoc_tools import *
from functools import lru_cache

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('16.in').read()
text_sample = open('16.ex1').read()


def calculate(start_valve, minutes, players, G, R, V, IV):
    start_valve_index = IV[start_valve]

    @lru_cache(maxsize=None)
    def dp(current_valve_index, time_left, players, open_valves):
        if players == 0:
            return 0

        if time_left == 0:
            return dp(start_valve_index, minutes, players - 1, open_valves)

        res = 0

        rate = R[V[current_valve_index]]
        if rate > 0 and (open_valves & (1 << current_valve_index)) == 0:
            flow_for_open = rate * (time_left - 1)
            res = max(res, flow_for_open + dp(current_valve_index, time_left - 1, players,
                                              open_valves | (1 << current_valve_index)))

        for next_valve in G[V[current_valve_index]]:
            res = max(res, dp(IV[next_valve], time_left - 1, players, open_valves))

        return res

    return dp(start_valve_index, minutes, players, 0)


def solve(text, part):
    # graph of connections
    G = defaultdict(list)
    # rates
    R = {}

    res = None

    # start pos
    st = "AA"

    V = {}
    IV = {}

    vi = 0
    for line in text.split("\n"):
        left, right = line.split(";")
        valve = left.split()[1]
        rate = get_all_nums(left.split()[-1])[0]
        words = right.replace(",", "").split()[4:]
        next_valves = [v.strip() for v in words]
        R[valve] = rate
        V[vi] = valve
        IV[valve] = vi
        vi += 1
        for v in next_valves:
            G[valve].append(v)

    if part == 1:
        res = calculate(st, 30, 1, G, R, V, IV)
    elif part == 2:
        res = calculate(st, 26, 2, G, R, V, IV)

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 1651
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 1947

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 1707
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 2556

stop = datetime.now()
print("duration:", stop - start)
