from datetime import datetime
from aoc_tools import *
from functools import lru_cache

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('19.in').read()
text_sample = open('19.ex1').read()


def calculate(total_minutes, blueprint):
    id, ore_r_ore, cla_r_ore, obs_r_ore, obs_r_cla, geo_r_ore, geo_r_obs = blueprint

    max_ore = max((ore_r_ore, cla_r_ore, obs_r_ore, geo_r_ore))
    max_cla = obs_r_cla
    max_obs = geo_r_obs

    def update_mat(ore_m, cla_m, obs_m, geo_m, ore_r, cla_r, obs_r, geo_r, minutes_left):
        # update material and limit it to max needed values for minutes that left till end
        ore = min(ore_m + ore_r, max_ore * minutes_left)
        cla = min(cla_m + cla_r, max_cla * minutes_left)
        obs = min(obs_m + obs_r, max_obs * minutes_left)
        geo = geo_m + geo_r  # never limit geode
        return (ore, cla, obs, geo)

    @lru_cache(maxsize=None)
    def dp(t, ore_r, cla_r, obs_r, geo_r, ore_m, cla_m, obs_m, geo_m):
        # t - time left, xxx_r - robot, xxx_m - material

        if t <= 0:
            return 0

        answer = 0

        # try build geode robot
        if (ore_m >= geo_r_ore
                and obs_m >= geo_r_obs
                and t > 1):
            mat = update_mat(ore_m - geo_r_ore, cla_m, obs_m - geo_r_obs, geo_m, ore_r, cla_r, obs_r, geo_r, t - 1)
            answer = max(answer, (t - 1) + dp(t - 1, ore_r, cla_r, obs_r, geo_r + 1, *mat))
            # don't try other options when geode robot will be build (cannot have better score)
            return answer

        # try build obsidian robot
        if (ore_m >= obs_r_ore
                and cla_m >= obs_r_cla
                and t > 1
                and obs_r < max_obs
                and obs_m < max_obs * t):
            mat = update_mat(ore_m - obs_r_ore, cla_m - obs_r_cla, obs_m, geo_m, ore_r, cla_r, obs_r, geo_r, t - 1)
            answer = max(answer, dp(t - 1, ore_r, cla_r, obs_r + 1, geo_r, *mat))

        # try build clay robot
        if (ore_m >= cla_r_ore
                and t > 1
                and cla_r < max_cla
                and cla_m < max_cla * t):
            mat = update_mat(ore_m - cla_r_ore, cla_m, obs_m, geo_m, ore_r, cla_r, obs_r, geo_r, t - 1)
            answer = max(answer, dp(t - 1, ore_r, cla_r + 1, obs_r, geo_r, *mat))

        # try build ore robot
        if (ore_m >= ore_r_ore
                and t > 1
                and ore_r < max_ore
                and ore_m < max_obs * t):
            mat = update_mat(ore_m - ore_r_ore, cla_m, obs_m, geo_m, ore_r, cla_r, obs_r, geo_r, t - 1)
            answer = max(answer, dp(t - 1, ore_r + 1, cla_r, obs_r, geo_r, *mat))

        # don't build any robot
        mat = update_mat(ore_m, cla_m, obs_m, geo_m, ore_r, cla_r, obs_r, geo_r, t - 1)
        answer = max(answer, dp(t - 1, ore_r, cla_r, obs_r, geo_r, *mat))

        return answer

    return dp(total_minutes, 1, 0, 0, 0, 0, 0, 0, 0)


def solve(text, part):
    res = None

    B = []

    for line in text.split("\n"):
        id, ore_r_ore, cla_r_ore, obs_r_ore, obs_r_cla, geo_r_ore, geo_r_obs = get_all_nums(line)
        B.append((id, ore_r_ore, cla_r_ore, obs_r_ore, obs_r_cla, geo_r_ore, geo_r_obs))

    if part == 1:
        minutes = 24
        res = 0
        for b in B:
            id = b[0]
            geodes = calculate(minutes, b)
            print(f"blueprint {id} of {len(B)} -> {geodes}")
            res += id * geodes

    elif part == 2:
        minutes = 32
        res = 1
        B = B[:3]  # use only first 3 blueprints
        for b in B:
            id = b[0]
            geodes = calculate(minutes, b)
            print(f"blueprint {id} of {len(B)} -> {geodes}")
            res *= geodes

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 33
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 1127

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 3472 (56 * 62)
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 21546 (21 * 27 * 38)

stop = datetime.now()
print("duration:", stop - start)
