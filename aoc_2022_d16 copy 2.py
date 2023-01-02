from datetime import datetime
from collections import defaultdict, deque, Counter
import copy
import re

CRED = '\033[91m'
CGRN = '\033[92m'
CEND = '\033[0m'


start = datetime.now()
lines_sample = open('16.ex1').readlines()
lines_puzzle = open('16.in').readlines()

def calc(R,O):
    s=0
    for (o,t) in O:
        flowT = 30-t+1
        if flowT > 0:
            s += R[o] *flowT

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
        print(v,r,others)
        G[v] = others
        R[v] = r

    print(G)
    print(R)

    notJammed = []
    for (v,r) in R.items():
        if r != 0:
            notJammed.append(v)

    print(notJammed)
    L = len(notJammed)


    P=[]
    q=deque()
    s = "AA"
    t=1
    q.append((s,t,[]))

    seen=set()

    while (q):
        p,t,O = q.popleft()
        print(p,t,len(O), O)

        if len(O) == L:
            P.append(O)
            continue

        if t==30:
            P.append(O)
            continue

        orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
        if (p,t,orded) in seen:
            continue
        
        seen.add((p,t,orded))

        pos = G[p]
        for np in pos:

            opened = [o[0] for o in O]
            if R[p] == 0:
                newO = O[:]
            elif p not in opened:
                newO = O[:]
                newO.append((p,t+1))

            q.append((np,t+1,newO))


    # print("test")
    # xx = [("DD",3),("BB",6), ("JJ",10), ("HH",18), ("EE",22), ("CC",25)]
    # print(calc(R,xx))

    res = max([calc(R,p) for p in P])

    return res



print(CRED + "sample:", solve1(lines_sample), CEND)  #
# print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  #
# print(solve1_t(text))  #
# print(solve2(lines))  #

stop = datetime.now()
print("duration:", stop - start)
