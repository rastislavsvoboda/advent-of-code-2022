from datetime import datetime
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('21.in').read()
text_sample = open('21.ex1').read()

HUMN = "humn"

def evaluate_op(a, op, b):
    if op == "+":
        val = a + b
    elif op == "-":
        val = a - b
    elif op == "*":
        val = a * b
    elif op == "/":
        assert a % b == 0
        val = a // b
    else:
        assert False
    return val


def try_evaluate_op(formula, R):
    assert len(formula) == 3, f"{formula}"
    a, op, b = formula
    if a in R and b in R:
        val = evaluate_op(R[a], op, R[b])
        return True, val
    return False, None


def evaluate_normal(node, G, R):
    if node in R:
        return R[node]

    formula = G[node]
    a, op, b = formula
    val_a = evaluate_normal(a, G, R)
    val_b = evaluate_normal(b, G, R)
    if val_a is None or val_b is None:
        return None

    val = evaluate_op(val_a, op, val_b)
    R[node] = val
    return val


def evaluate_reversed(node, result, R, G):
    if node == HUMN:
        R[HUMN] = result

    if node in R:
        return R[node]

    formula = G[node]

    assert len(formula) == 3, f"{formula}"
    a, op, b = formula

    if a != HUMN and a in R:
        val_a = R[a]

        if op == "+":
            val = result - val_a
        elif op == "-":
            val = val_a - result
        elif op == "*":
            assert result % val_a == 0
            val = result // val_a
        elif op == "/":
            assert val_a % result == 0
            val = val_a // result
        else:
            assert False

        val_b = evaluate_reversed(b, val, R, G)

    elif b != HUMN and  b in R:
        val_b = R[b]

        if op == "+":
            val = result - val_b
        elif op == "-":
            val = result + val_b
        elif op == "*":
            assert result % val_b == 0
            val = result // val_b
        elif op == "/":
            val = result * val_b
        else:
            assert False

        val_a = evaluate_reversed(a, val, R, G)

    else:
        assert False

    assert result == evaluate_op(val_a, op, val_b)
    return result


def solve(text, part):
    res = None

    G = {}
    R = {}
    ROOT = "root"
    for line in text.split("\n"):
        parts = line.split(": ")
        node = parts[0]
        formula = parts[1].split()
        G[node] = formula
        if len(formula) == 1:
            n = int(formula[0])
            R[node] = n

    if part == 1:
        res = evaluate_normal(ROOT, G, R)
    elif part == 2:
        root_formula = G[ROOT]
        assert len(root_formula) == 3
        humn_formula = G[HUMN]
        assert len(humn_formula) == 1
        R[HUMN] = None

        root_left = root_formula[0]
        root_right = root_formula[2]

        # evaluate both sides, one will be evaluated to number
        val_left = evaluate_normal(root_left, G, R)
        val_right = evaluate_normal(root_right, G, R)

        if not val_left is None:
            val = val_left
            target = root_right
        elif not val_right is None:
            val = val_right
            target = root_left
        else:
            assert False

        evaluate_reversed(target, val, R, G)

        res = R[HUMN]

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 152
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 158661812617812

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 301
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 3352886133831

stop = datetime.now()
print("duration:", stop - start)
