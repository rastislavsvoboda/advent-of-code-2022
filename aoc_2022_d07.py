from datetime import datetime
from collections import defaultdict

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('7.ex1').readlines()
lines_puzzle = open('7.in').readlines()


def get_d_size(D, S, dir_name):
    if dir_name in S:
        return S[dir_name]

    total_size = 0
    for (type, name, size) in D[dir_name]:
        if type == 'd':
            total_size += get_d_size(D, S, name)
        else:
            assert(type == 'f')
            total_size += size

    S[dir_name] = total_size         
    return total_size


def solve(lines):
    D = defaultdict(list)
    current = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        words = line.split()
        # print(i, words)
        if words[0] == "$":
            # command
            if words[1] == "cd":
                if words[2] == "..":
                    current.pop()
                elif words[2] == "/":
                    current = ["/"]
                else:
                    current.append(words[2])
            elif words[1] == "ls":
                pass
        else:
            # output
            cd_name = "/".join(current)
            if words[0] == "dir":
                d_name = cd_name + "/" + words[1]
                D[cd_name].append(("d", d_name, 0))
            else:
                f_size = int(words[0])
                f_name = words[1]
                D[cd_name].append(("f", f_name, f_size))
        i += 1

    # print(D.keys())

    S = defaultdict(int)
    for k in D.keys():
        S[k] = get_d_size(D, S, k)

    # part 1
    res1 = sum(list(filter(lambda s: s <= 100000,  S.values())))

    # part 2
    space = 70000000
    needed = 30000000
    cur_space = space - S["/"]
    to_free = needed - cur_space

    sorted_dir_sizes = list(sorted(S.values()))

    fitting = list(filter(lambda s: s >= to_free,  sorted_dir_sizes))
    if (len(fitting) > 0):
        res2 = fitting[0]
    else:
        res2 = None

    return (res1, res2)


print(CRED + "sample:", solve(lines_sample), CEND)  # 95437, 24933642
print(CGRN + "puzzle:", solve(lines_puzzle), CEND)  # 1084134, 6183184

stop = datetime.now()
print("duration:", stop - start)
