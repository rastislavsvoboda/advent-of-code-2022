from datetime import datetime
from collections import namedtuple
from aoc_tools import *

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'

start = datetime.now()
text_puzzle = open('11.in').read()
text_sample = open('11.ex1').read()


Monkey = namedtuple('Monkey', 'index operation test_num monkey_true monkey_false')


def apply(item, op):
    a, o, b = op
    assert a == "old"
    if b != "old":
        n = int(b)
    else:
        n = item
    if o == "+":
        return item + n
    if o == "*":
        return item * n
    assert False, op

def solve(text, part):
    res = 0
    if part == 1:
        M = {}
        I = {}
        for grp in text.split("\n\n"):
            id_str, items_str, op_str, test_str, iftrue_str, iffalse_str = grp.split("\n")
            id = get_all_nums(id_str)[0]
            items = get_all_nums(items_str)
            op = op_str.split("=")[1].split()
            test = get_all_nums(test_str)[0]
            test_t = get_all_nums(iftrue_str)[0]
            test_f = get_all_nums(iffalse_str)[0]
            m = Monkey(id, op, test, test_t, test_f)
            M[id] = m
            I[id] = items

        INSP = defaultdict(int)
        for r in range(20):
            for i in range(len(M)):
                m = M[i]
                items = I[i]
                for item in items:
                    INSP[i] += 1
                    new_item = apply(item,  m.operation)
                    new_item = new_item // 3
                    if new_item % m.test_num == 0:
                        I[m.monkey_true].append(new_item)
                    else:
                        I[m.monkey_false].append(new_item)
                I[i] = []
            # print(f"after round {r+1}")
            # for x in range(len(I)):
            #     print(I[x])

            # print(INSP)
        insp = list(sorted(INSP.values(), reverse=True))
        res = insp[0] * insp[1]
    else:
        M = {}
        I = {}
        num = 1
        for grp in text.split("\n\n"):
            id_str, items_str, op_str, test_str, iftrue_str, iffalse_str = grp.split("\n")
            id = get_all_nums(id_str)[0]
            items = get_all_nums(items_str)
            op = op_str.split("=")[1].split()
            test = get_all_nums(test_str)[0]
            test_t = get_all_nums(iftrue_str)[0]
            test_f = get_all_nums(iffalse_str)[0]
            m = Monkey(id, op, test, test_t, test_f)
            # print(m)
            M[id] = m
            I[id] = items
            # use all factors that monkey are testing
            num *= test

        INSP = defaultdict(int)
        for r in range(10000):
            for i in range(len(M)):
                m = M[i]
                items = I[i]
                for item in items:
                    INSP[i] += 1
                    new_item = apply(item,  m.operation)
                    # modulo by all multiples for used factors
                    new_item = new_item % num
                    # for big numbers this starts to slow down
                    if new_item % m.test_num == 0:
                        I[m.monkey_true].append(new_item)
                    else:
                        I[m.monkey_false].append(new_item)
                I[i] = []

        insp = list(sorted(INSP.values(), reverse=True))
        res = insp[0] * insp[1]

    return res


print(CRED + "sample:", solve(text_sample, 1), CEND)  # 10605
print(CGRN + "puzzle:", solve(text_puzzle, 1), CEND)  # 111210

print(CRED + "sample:", solve(text_sample, 2), CEND)  # 2713310158
print(CGRN + "puzzle:", solve(text_puzzle, 2), CEND)  # 15447387620

stop = datetime.now()
print("duration:", stop - start)
