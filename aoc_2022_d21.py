from datetime import datetime

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('21.ex1').readlines()
lines_puzzle = open('21.in').readlines()


def invert_op(op):
    OPS = "+-*/"
    INV = "-+/*"
    i = OPS.index(op)
    return INV[i]


def eval_op(v1, v2, op):
    if op == "+":
        return v1+v2
    if op == "-":
        return v1-v2
    if op == "*":
        return v1*v2
    if op == "/":
        assert v1 % v2 == 0
        return v1//v2
    assert False


def traverse(G, node):
    if len(G[node][0]) == 0:
        # assert G[node][2] is not None
        return G[node][2]
    else:
        v1 = traverse(G, G[node][0][0])
        v2 = traverse(G, G[node][0][1])
        if v1 is None or v2 is None:
            return None

        res = eval_op(v1, v2, G[node][1])
        # print(v1,v2,G[node][1],res)
        G[node] = (G[node][0], G[node][1], res)
        return res


def traverse_back(G, node, val):
    if len(G[node][0]) == 0:
        # assert G[node][2] is not None
        if G[node][2] is None:
            # print("setting", node, val)
            G[node] = (G[node][0], G[node][1], val)
        return G[node][2]
    else:
        n1 = G[node][0][0]
        n1val = G[n1][2]

        n2 = G[node][0][1]
        n2val = G[n2][2]

        op = G[node][1]

        if n1val is None:
            needed_v1 = eval_op(val, n2val, invert_op(op))
            n1val = traverse_back(G, n1, needed_v1)
        elif n2val is None:
            # be careful how to inverse - and /
            if op == "-":
                needed_v2 = eval_op(n1val, val, "-")
            elif op == "/":
                needed_v2 = eval_op(n1val, val, "/")
            else:
                needed_v2 = eval_op(val, n1val, invert_op(op))
            n2val = traverse_back(G, n2, needed_v2)
        else:
            assert False

        assert n1[1] is not None
        assert n2[1] is not None
        assert val == eval_op(n1val, n2val, op)
        return val


def get_node_val(G, node, name):    
    if len(G[node][0]) == 0:        
        if (node == name):
            return G[node][2]        
        return None
    else:
        v1 = get_node_val(G, G[node][0][0], name)
        if v1 is not None:
            return v1
        v2 = get_node_val(G, G[node][0][1], name)
        if v2 is not None:
            return v2
        return None

def solve1(lines):
    G = {}

    root_node_1, root_node_2, root_node_op = None, None, None
    for line in lines:
        words = line.strip().split()
        monkey = words[0][:-1]

        if monkey == "root":
            root_node_1 = words[1]
            root_node_2 = words[3]
            root_node_op = words[2]
        elif len(words) == 2:
            G[monkey] = ([], None, int(words[1]))
        else:
            G[monkey] = ([words[1], words[3]], words[2], None)

    val1 = traverse(G, root_node_1)
    val2 = traverse(G, root_node_2)
    res = eval_op(val1, val2, root_node_op)

    return res


def solve2(lines):
    G = {}
    ROOT = "root"
    HUMN = "humn"

    root_node_1, root_node_2, root_node_op = None, None, None
    for line in lines:
        words = line.strip().split()
        monkey = words[0][:-1]

        if monkey == ROOT:
            root_node_1 = words[1]
            root_node_2 = words[3]
        elif monkey == HUMN:
            G[monkey] = ([], None, None)
        elif len(words) == 2:
            G[monkey] = ([], None, int(words[1]))
        else:
            G[monkey] = ([words[1], words[3]], words[2], None)

    val1 = traverse(G, root_node_1)
    # print(val1)
    val2 = traverse(G, root_node_2)
    # print(val2)

    res = None
    if val1 is None:
        assert val2 is not None
        traverse_back(G, root_node_1, val2)
        res = get_node_val(G, root_node_1, HUMN)
    elif val2 is None:
        assert val1 is not None
        traverse_back(G, root_node_2, val1)
        res = get_node_val(G, root_node_2, HUMN)
    else:
        assert False

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 152
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 158661812617812

print(CRED + "sample:", solve2(lines_sample), CEND)  # 301
print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 3352886133831

stop = datetime.now()
print("duration:", stop - start)
