from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('21.ex1').readlines()
lines_puzzle = open('21.in').readlines()


def solve1(lines):
    res = 0

    G = {}
    R = {}
    for line in lines:
        line = line.strip()
        words = line.split()
        # print(words)
        monkey = words[0][:-1]
        if len(words) == 2:
            R[monkey] = int(words[-1])
        else:
            G[monkey] = words[1:3+1]

    while "root" not in R:
        for k in G.keys():
            formula = G[k]
            if formula[0] in R and formula[2] in R:
                a = int(R[formula[0]])
                b = int(R[formula[2]])
                if formula[1] == "+":
                    R[k] = a + b
                if formula[1] == "-":
                    R[k] = a - b
                if formula[1] == "*":
                    R[k] = a * b
                if formula[1] == "/":
                    R[k] = a // b

    res = R["root"]
    return res


def invert_op(op):
    if op == "+":
        return "-"
    if op == "-":
        return "+"
    if op == "/":
        return "*"
    if op == "*":
        return "/"
    assert False


def try_eval_node(R, k, formula):
    if formula[0] in R and formula[2] in R:
        a = int(R[formula[0]])
        b = int(R[formula[2]])
        if formula[1] == "+":
            R[k] = a + b
        if formula[1] == "-":
            R[k] = a - b
        if formula[1] == "*":
            R[k] = a * b
        if formula[1] == "/":
            assert a % b == 0
            R[k] = a // b
        return True
    return False


def try_set_node(R, k, formula):
    if k in R and formula[0] in R and formula[2] in R:
        return False
    if k in R and formula[2] in R:
        v = R[k]
        b = int(R[formula[2]])
        if formula[1] == "+":
            R[formula[0]] = v - b
        if formula[1] == "-":
            R[formula[0]] = v + b
        if formula[1] == "*":
            assert v % b == 0
            R[formula[0]] = v // b
        if formula[1] == "/":
            R[formula[0]] = v * b
        return True
    if k in R and formula[0] in R:
        v = R[k]
        a = int(R[formula[0]])
        if formula[1] == "+":
            R[formula[2]] = v - a
        if formula[1] == "-":
            R[formula[2]] = a - v
        if formula[1] == "*":
            assert v % a == 0
            R[formula[2]] = v // a
        if formula[1] == "/":
            assert a % v == 0
            R[formula[2]] = a // v
        return True
    return False


def solve2(lines):
    G = {}
    R = {}

    root_nodes = None

    for line in lines:
        words = line.strip().split()
        monkey = words[0][:-1]

        if monkey == "root":
            root_nodes = [words[1], words[3]]
            # print("root_nodes", root_nodes)
            continue
        if monkey == "humn":
            # ignore
            continue

        if len(words) == 2:
            R[monkey] = int(words[-1])
        else:
            G[monkey] = words[1:]

    while not (root_nodes[0] in R or root_nodes[1] in R):
        for k in G:
            if try_eval_node(R, k, G[k]):
                G.pop(k)
                break

    if root_nodes[0] in R:
        R[root_nodes[1]] = R[root_nodes[0]]
    elif root_nodes[1] in R:
        R[root_nodes[0]] = R[root_nodes[1]]
    else:
        assert False, "should have computed at least on node in root's formula"

    while "humn" not in R:
        for k in G:
            if try_set_node(R, k, G[k]):
                break
        for k in G:
            if try_eval_node(R, k, G[k]):
                G.pop(k)
                break

    res = R["humn"]

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 152
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 158661812617812
print(CRED + "sample:", solve2(lines_sample), CEND)  # 301
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 3352886133831

stop = datetime.now()
print("duration:", stop - start)
