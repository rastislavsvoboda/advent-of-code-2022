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
    LL = len(R)

    # COST={}
    # for i in range(0,len(V)):
    #     for j in range(i+1,len(V)):
    #         if i == j:
    #             cost = 0
    #         cost = dijkstra1(G, V[i], V[j])
    #         # print(V[i], V[j], cost)
    #         COST[(i,j)] = cost
    #         COST[(j,i)] = cost

    # print(COST)

    # perm = permutations(notJammed) 
    # print(len(list(perm))) 

    # return (len(list(perm)))
    # assert False

    CALCS={}

    PP=set()
    P=[]
    q=[]
    s = "AA"
    t=1

    heapq.heappush(q, (0, s,s,t,[]))
    # q.append((s,s,t,[]))

    maxC = 0

    seen=set()

    while (q):

        cost,pm,pe,t,O = heapq.heappop(q)

        ccc = calc2(C,R,O)
        # print(t,pm,pe,len(O), O, ccc)
        if len(q) % 10000 == 0:
            print(len(q))
        # print(cost)

        if len(O) == L or t == 26:
        # if t == 26:
            # orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
            # if orded not in PP:
            #     PP.add(orded)
            #     P.append(O)
            # if -cost > maxC:
                # maxC = -cost

            if ccc > maxC:
                maxC = ccc
                print("max:", maxC)
            continue

        orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
        if (pm,pe,t,orded) in seen:
            continue
        
        seen.add((pm,pe,t,orded))

        pos_m = G[pm]
        pos_e = G[pe]
        for npm in pos_m:
            for npe in pos_e:

                orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(O)])
                if (npm,npe,t+1,orded) in seen:
                    continue

                # newC = calc2(C,R,O)
                # heapq.heappush(q, (-newC,npm,npe,t+1,O[:]))
                # newC = calc2(C,R,O)
                heapq.heappush(q, (0,npm,npe,t+1,O[:]))



        m_o = False
        e_o = False

        opened = [o[0] for o in O]
        if R[pm] == 0:
            pass
        elif pm not in opened:
            m_o = True
            newO = O[:]
            newO.append((pm,t))
            for npe in pos_e:

                orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(newO)])
                if (pm,npe,t+1,orded) in seen:
                    continue

                newC =calc2(C,R,newO)
                # heapq.heappush(q, (-newC,pm,npe,t+1,newO))
                heapq.heappush(q, (0,pm,npe,t+1,newO))

        if R[pe] == 0:
            pass
        elif pe not in opened:
            e_o = True
            newO = O[:]
            newO.append((pe,t))
            for npm in pos_m:

                orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(newO)])
                if (npm,pe,t+1,orded) in seen:
                    continue

                # newC = calc2(C,R,newO)
                # heapq.heappush(q, (-newC,npm,pe,t+1,newO))
                heapq.heappush(q, (0,npm,pe,t+1,newO))


        if m_o and e_o and pm != pe:
            newO = O[:]
            newO.append((pm,t))
            newO.append((pe,t))

            orded = "".join([a + "_" + str(b) +";" for (a,b) in sorted(newO)])
            if (pm,pe,t+1,orded) in seen:
                continue

            # newC = calc2(C,R,newO)
            # heapq.heappush(q, (-newC,pm,pe,t+1,newO))
            heapq.heappush(q, (0,pm,pe,t+1,newO))



            



    # print("test")
    # xx = [("DD",3),("BB",6), ("JJ",10), ("HH",18), ("EE",22), ("CC",25)]
    # # xx = [("DD",2),("BB",5), ("JJ",9), ("HH",17), ("EE",21), ("CC",24)]
    # print(calc(R,xx))

    # print(len(P))
    # print("best")
    # for xxx in P:
    #     if len(xxx)==6 and ("DD",2) in xxx and ("BB",5) and ("JJ",9) in xxx and ("HH",17) in xxx and ("EE",21) in xxx:
    #         print(xxx)

    # print(len(P), len(PP))

    # res = max([calc2(R,p) for p in P])
    res = maxC

    return res
    
seed(datetime.now())

# print(CRED + "sample:", solve1(lines_sample), CEND)  # 1651
# print(CGRN + "puzzle:", solve1(lines_puzzle), CEND)  # 1947
print(CRED + "sample:", solve2(lines_sample), CEND)  # 
# print(CGRN + "puzzle:", solve2(lines_puzzle), CEND)  # 
# print(solve1_t(text))  #
# print(solve2(lines))  #

stop = datetime.now()
print("duration:", stop - start)
