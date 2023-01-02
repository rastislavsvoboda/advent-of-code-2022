from datetime import datetime
from collections import defaultdict, deque, Counter
from collections import defaultdict, deque
from itertools import permutations
import copy
import re
import time
import heapq
import math

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

def calc3(C,R,O,tM):
    # orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
    # if orded in C:
    #     return C[orded];

    s=0
    for (o,t) in O:
        flowT = tM-t
        if flowT > 0:
            s += R[o] *flowT

    # C[orded]=s
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
        print(line)
        print("...", v,r,others)
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
    q.append((s,t,set()))

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



    # print("test")
    # xx = [("DD",3),("BB",6), ("JJ",10), ("HH",18), ("EE",22), ("CC",25)]
    # # xx = [("DD",2),("BB",5), ("JJ",9), ("HH",17), ("EE",21), ("CC",24)]
    # print(calc(R,xx))

    # print(len(P))
    # print("best")
    # for xxx in P:
    #     if len(xxx)==6 and ("DD",2) in xxx and ("BB",5) and ("JJ",9) in xxx and ("HH",17) in xxx and ("EE",21) in xxx:
    #         print(xxx)

    print(len(P), len(PP))

    res = max([calc(R,p) for p in P])

    return res


def dijkstra1(m, start_pos, end_pos):
    q = []
    marked = set()
    min_steps = math.inf
    heapq.heappush(q, (0, start_pos))

    while q:
        s, p = heapq.heappop(q)

        if (s, p) in marked:
            continue

        if p == end_pos:
            min_steps = s
            break

        marked.add((s, p))

        adj = m[p]
        for a in adj:
            # if (a, k) in marked:
            #     continue
            heapq.heappush(q, (s+1, a))

    return min_steps

def getVal1(pm,t,O,G,R,L,DP,tM):
    orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
    # orded = frozenset(O)
    if (pm,t,orded) in DP:
        return DP[(pm,t,orded)]

    res = None
    if t == tM:
        res = calc3(None, R,O, tM)
        # print(res)
    elif len(O) == L:
        res = getVal1(pm,t+1,O,G,R,L,DP,tM)
    else:
        vals=[]

        opened = [o[0] for o in O]
        m_o = False
        e_o = False
        pos_m = G[pm]

        for npm in pos_m:
            vals.append(getVal1(npm,t+1,O[:],G,R,L,DP,tM))

        if R[pm] == 0:
            pass
        elif pm not in opened:
            m_o = True
            newO = O[:]
            newO.append((pm,t))
            vals.append(getVal1(pm,t+1,newO,G,R,L,DP,tM))

        res = max(vals)

    assert res is not None
    if len(DP)>0 and res > max(DP.values()):
        print(res)
    DP[(pm,t,orded)] = res

    
    return res
def getVal(pm,pe,t,O,G,R,L,DP,tM):
    # orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
    orded = frozenset(O)
    if (pm,pe,t,orded) in DP:
        return DP[(pm,pe,t,orded)]

    res = None
    if t == tM:
        res = calc3(None, R,O, tM)
        # print(res)
    elif len(O) == L:
        res = getVal(pm,pe,t+1,O,G,R,L,DP,tM)
    else:
        vals=[]

        opened = [o[0] for o in O]
        m_o = False
        e_o = False
        pos_m = G[pm]
        pos_e = G[pe]

        for npm in pos_m:
            for npe in pos_e:
                vals.append(getVal(npm,npe,t+1,O[:],G,R,L,DP,tM))

        if R[pm] == 0:
            pass
        elif pm not in opened:
            m_o = True
            newO = O[:]
            newO.append((pm,t))
            # newO = O | frozenset()
            for npe in pos_e:
                vals.append(getVal(pm,npe,t+1,newO,G,R,L,DP,tM))

        if R[pe] == 0:
            pass
        elif pe not in opened:
            e_o = True
            newO = O[:]
            newO.append((pe,t))
            for npm in pos_m:
                vals.append(getVal(npm,pe,t+1,newO,G,R,L,DP,tM))

        if m_o and e_o and pm != pe:
            newO = O[:]
            newO.append((pm,t))
            newO.append((pe,t))
            vals.append(getVal(pm,pe,t+1,newO,G,R,L,DP,tM))

        res = max(vals)

    assert res is not None
    if len(DP)>0 and res > max(DP.values()):
        print(res)
    DP[(pm,pe,t,orded)] = res

    
    return res


def solve1b(lines):
    V=[]
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
        V.append(v)

    # print(G)
    # print(R)

    notJammed = []
    for (v,r) in R.items():
        if r != 0:
            notJammed.append(v)

    print(notJammed)
    L = len(notJammed)
    # LL = len(R)
    DP={}

    res = getVal1("AA",1,[],G,R,L,DP,30)

    return res

def solve2(lines):
    V=[]
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
        V.append(v)

    # print(G)
    # print(R)

    notJammed = []
    for (v,r) in R.items():
        if r != 0:
            notJammed.append(v)

    print(notJammed)
    L = len(notJammed)
    # LL = len(R)
    DP={}

    res = getVal("AA","AA",1,[],G,R,L,DP,26)

    return res

# x = [("1",1), ("2",2)]

# y = frozenset(x)

# D={}
# D[y] = 1

# x2 = [("2",2),("1",1)]
# y2 = frozenset(x2)

# x3 = [("2",2),("1",2)]
# y3 = frozenset(x3)


# print(y in D.keys())
# print(y2 in D.keys())
# print(y3 in D.keys())



# print(CRED + "sample:", solve1(lines_sample), CEND)  # 1651
print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 1947
# print(CRED + "sample:", solve2(lines_sample), CEND)  # 
# print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 
# print(solve1_t(text))  #
# print(solve2(lines))  #

stop = datetime.now()
print("duration:", stop - start)
