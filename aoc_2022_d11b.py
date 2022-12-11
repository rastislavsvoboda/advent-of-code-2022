from datetime import datetime
from collections import namedtuple

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
text_sample = open('11.ex1').read()
text_puzzle = open('11.in').read()

Monkey = namedtuple(
    'Monkey', 'index operation test_num monkey_true monkey_false')


def solve1(text):
    M = []
    I = []
    C = []
    for grp in text.split('\n\n'):
        index_row, items_row, operation_row, test_row, true_row, false_row = grp.split(
            '\n')
        index = int(index_row.split(':')[0].split(' ')[1])
        items = [int(n) for n in items_row.split(':')[1].split(',')]
        operation = operation_row.split(' ')[-3:]
        test_num = int(test_row.split(' ')[-1])
        monkey_true = int(true_row.split(' ')[-1])
        monkey_false = int(false_row.split(' ')[-1])
        m = Monkey(index, operation, test_num, monkey_true, monkey_false)
        M.append(m)
        I.append(items)
        C.append(0)

    for r in range(20):
        for i, m in enumerate(M):
            # print("monkey", m)
            for item in I[i]:
                # print("item", i)
                C[i] += 1
                x = m.operation[2]
                op = m.operation[1]
                if x == "old":
                    v = item
                else:
                    v = int(x)
                if op == "*":
                    newV = item * v
                elif op == "+":
                    newV = item + v
                else:
                    print("ERROR")
                newV = newV // 3
                if newV % m.test_num == 0:
                    monkey_to_index = m.monkey_true
                else:
                    monkey_to_index = m.monkey_false
                I[monkey_to_index].append(newV)
            I[i] = []

    counts = list(sorted(C))
    res = counts[-1] * counts[-2]
    return res


def solve2(text):
    M = []
    I = []
    C = []
    div_num = 1
    for grp in text.split('\n\n'):
        index_row, items_row, operation_row, test_row, true_row, false_row = grp.split(
            '\n')
        index = int(index_row.split(':')[0].split(' ')[1])
        items = [int(n) for n in items_row.split(':')[1].split(',')]
        operation = operation_row.split(' ')[-3:]
        test_num = int(test_row.split(' ')[-1])
        monkey_true = int(true_row.split(' ')[-1])
        monkey_false = int(false_row.split(' ')[-1])
        m = Monkey(index, operation, test_num, monkey_true, monkey_false)
        M.append(m)
        I.append(items)
        C.append(0)
        div_num *= test_num

    for r in range(10000):
        for i, m in enumerate(M):
            # print("monkey", m)
            for item in I[i]:
                # print("item", i)
                C[i] += 1
                x = m.operation[2]
                op = m.operation[1]
                if x == "old":
                    v = item
                else:
                    v = int(x)
                if op == "*":
                    newV = item * v
                elif op == "+":
                    newV = item + v
                else:
                    print("ERROR")
                newV %= div_num
                if newV % m.test_num == 0:
                    monkey_to_index = m.monkey_true
                else:
                    monkey_to_index = m.monkey_false
                I[monkey_to_index].append(newV)
            I[i] = []

    l = list(sorted(C))
    res = l[-1] * l[-2]
    return res


print(CRED + "sample:", solve1(text_sample), CEND)  # 10605
print(CGRN + "puzzle:", solve1(text_puzzle), CEND)  # 111210
print(CRED + "sample:", solve2(text_sample), CEND)  # 2713310158
print(CGRN + "puzzle:", solve2(text_puzzle), CEND)  # 15447387620

stop = datetime.now()
print("duration:", stop - start)
