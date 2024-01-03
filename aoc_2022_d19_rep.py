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
    id, ore_r_ore, clay_r_ore, obsidian_r_ore, obsidian_r_clay, geo_r_ore, geo_r_obsidian = blueprint

    robots = (1, 0, 0, 0)
    materials = (0, 0, 0, 0)

    ORE = 0
    CLAY = 1
    OBS = 2
    GEO = 3

    max_ore = max([ore_r_ore, clay_r_ore, obsidian_r_ore, geo_r_ore])
    max_clay = obsidian_r_clay
    max_obs = geo_r_obsidian

    def limit_resources(new_material, minutes_left):
        # limit to max needed resources in left minutes
        new_material[ORE] = min(new_material[ORE], max_ore * minutes_left)
        new_material[CLAY] = min(new_material[CLAY], max_clay * minutes_left)
        new_material[OBS] = min(new_material[OBS], max_obs * minutes_left)
        return new_material

    @lru_cache(maxsize=None)
    def dp(state):
        (minutes, robots, materials) = state

        if minutes <= 0:
            return 0

        answer = 0

        # build geo
        if (materials[ORE] >= geo_r_ore
                and materials[OBS] >= geo_r_obsidian
                and minutes > 1):
            new_robots = list(robots)
            new_robots[GEO] += 1
            new_material = list(materials)
            new_material[ORE] -= geo_r_ore
            new_material[OBS] -= geo_r_obsidian
            for i in range(4):
                new_material[i] += robots[i]

            new_material = limit_resources(new_material, minutes - 1)

            answer = max(answer, (1 * (minutes - 1)) + dp((minutes - 1, tuple(new_robots), tuple(new_material))))
            # don't try other option when GEO will be build
            return answer

        # build obsidian
        if (materials[ORE] >= obsidian_r_ore
                and materials[CLAY] >= obsidian_r_clay
                and minutes > 1
                and robots[OBS] < max_obs
                and materials[OBS] < max_obs * minutes):
            new_robots = list(robots)
            new_robots[OBS] += 1
            new_material = list(materials)
            new_material[ORE] -= obsidian_r_ore
            new_material[CLAY] -= obsidian_r_clay
            for i in range(4):
                new_material[i] += robots[i]

            new_material = limit_resources(new_material, minutes - 1)

            answer = max(answer, dp((minutes - 1, tuple(new_robots), tuple(new_material))))

        # build clay
        if (materials[ORE] >= clay_r_ore
                and minutes > 1
                and robots[CLAY] < max_clay
                and materials[CLAY] < max_clay * minutes):
            new_robots = list(robots)
            new_robots[CLAY] += 1
            new_material = list(materials)
            new_material[ORE] -= clay_r_ore
            for i in range(4):
                new_material[i] += robots[i]

            new_material = limit_resources(new_material, minutes - 1)

            answer = max(answer, dp((minutes - 1, tuple(new_robots), tuple(new_material))))

        # build ore
        if (materials[ORE] >= ore_r_ore
                and minutes > 1
                and robots[ORE] < max_ore
                and materials[ORE] < max_obs * minutes):
            new_robots = list(robots)
            new_robots[ORE] += 1
            new_material = list(materials)
            new_material[ORE] -= ore_r_ore
            for i in range(4):
                new_material[i] += robots[i]

            new_material = limit_resources(new_material, minutes - 1)

            answer = max(answer, dp((minutes - 1, tuple(new_robots), tuple(new_material))))

        # don't build any robot
        new_material = []
        for i in range(4):
            new_material.append(materials[i] + robots[i])

        new_material = limit_resources(new_material, minutes - 1)

        answer = max(answer, dp((minutes - 1, robots, tuple(new_material))))

        return answer

    return dp((total_minutes, robots, materials))


def solve(text, part):
    res = 0

    B = []

    for line in text.split("\n"):
        id, ore_r_ore, clay_r_ore, obs_r_ore, obs_r_clay, geo_r_ore, geo_r_obs = get_all_nums(line)
        B.append((id, ore_r_ore, clay_r_ore, obs_r_ore, obs_r_clay, geo_r_ore, geo_r_obs))

    if part == 1:
        minutes = 24
        for b in B:
            id = b[0]
            print(f"blueprint {id} of {len(B)}", end="")
            geodes = calculate(minutes, b)
            print(f" -> {geodes}")
            res += id * geodes

    elif part == 2:
        minutes = 32
        res = 1
        B_to_use = B[:3]
        for b in B_to_use:
            id = b[0]
            print(f"blueprint {id} of {len(B_to_use)}", end="")
            geodes = calculate(minutes, b)
            print(f" -> {geodes}")
            res *= geodes

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 33
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 1127

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 3472
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 21546

stop = datetime.now()
print("duration:", stop - start)
