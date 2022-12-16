from datetime import datetime
from collections import defaultdict, deque, Counter
from collections import defaultdict, deque
from itertools import permutations
import copy
import re
import time
import heapq
import math
from random import seed
from random import randint


CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('16.ex1').readlines()
lines_puzzle = open('16.in').readlines()

C={}

def calc(R,O):
    s=0
    for (o,t) in O:
        flowT = 30-t
        if flowT > 0:
            s += R[o] *flowT

    return s

def calc2(C,R,O):
    orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
    if orded in C:
        return C[orded];

    s=0
    for (o,t) in O:
        flowT = 26-t
        if flowT > 0:
            s += R[o] *flowT

    C[orded]=s
    return s


def solve1(lines):
    G={}
    R={}
    # O=set()
    for line in lines:
        line = line.strip()
        words = line.split()
        nums = re.findall(r"[+-]?\d+", words[4])
        v = words[1]
        r = int(nums[0])
        others = [ o[:2] for o in words[9:]]
        # print(v,r,others)
        G[v] = others
        R[v] = r

    # print(G)
    # print(R)

    notJammed = []
    for (v,r) in R.items():
        if r != 0:
            notJammed.append(v)

    # print(notJammed)
    L = len(notJammed)

    PP=set()
    P=[]
    q=deque()
    s = "AA"
    t=1
    q.append((s,t,[]))

    seen=set()

    while (q):
        p,t,O = q.popleft()
        # print(p,t,len(O), O)
        if len(q) % 1000000 == 0:
            print(len(q))

        if len(O) == L or t == 30:
            orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
            if orded not in PP:
                PP.add(orded)
                P.append(O)
            continue

        orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
        if (p,t,orded) in seen:
            continue
        
        seen.add((p,t,orded))

        pos = G[p]
        for np in pos:
            q.append((np,t+1,O))

        opened = [o[0] for o in O]
        if R[p] == 0:
            pass
        elif p not in opened:
            newO = O[:]
            newO.append((p,t))
            q.append((p,t+1,newO))
            continue


    print(len(P), len(PP))

    res = max([calc(R,p) for p in P])

    return res


print(CRED + "sample:", solve1(lines_sample), CEND)  # 1651
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 1947

stop = datetime.now()
print("duration:", stop - start)
