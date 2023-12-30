from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('7.in').read()
text_sample = open('7.ex1').read()


def get_dir_path(d, D, cache):
    if d in cache:
        return cache[d]

    res = 0
    items = D[d]
    for item_type, item_size, item_name in items:
        if item_type == "f":
            res += item_size
        elif item_type == "d":
            res += get_dir_path(item_name, D, cache)
        else:
            assert False

    cache[d] = res
    return res


def solve(text, part):
    D = defaultdict(list)
    cd = []
    for line in text.split("\n"):
        words= line.split()
        if words[0] == "$":
            # cmd
            if words[1] == "cd":
                if words[2] == "..":
                    assert cd != []
                    cd.pop()
                else:
                    cd.append(words[2])
            elif words[1] == "ls":
                pass
            else:
                assert False, (f"unknown cmd {words[1]}")
        else:
            # output
            if words[0] == "dir":
                # dir
                cd_name = "/".join(cd)
                D[cd_name].append(("d", 0, cd_name + "/" + words[1]))
            else:
                # file
                cd_name = "/".join(cd)
                size = int(words[0])
                D[cd_name].append(("f", size, cd_name + "/" + words[1]))

    cache = {}
    get_dir_path("/", D, cache)

    res = None
    if part == 1:
        res = 0
        for k, v in cache.items():
            if v <= 100000:
                res += v
    elif part == 2:
        DISK = 70000000
        NEED = 30000000
        dir_sizes = sorted(list(cache.values()))
        used = cache["/"]
        free = DISK - used
        need_to_free = NEED - free
        fitting = sorted(list(filter(lambda x: x >= need_to_free, dir_sizes)))
        res = min(fitting)

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 95437
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 1084134

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 24933642
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 6183184

stop = datetime.now()
print("duration:", stop - start)
