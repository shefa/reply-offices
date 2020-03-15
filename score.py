from simulated_annealing import *
import random
import sys
from collections import namedtuple

Worker = namedtuple('Worker', 'company, bonus, skills')
OFFICE = list()
DEVS = list()
PMS = list()
state = list()
state2 = list()
ma3x = list()
moves_full=[[-1,0],[1,0],[0,-1],[0,1]]
moves=[[-1,0],[0,-1]]

initial_solution = sys.argv[2]
m, n, num_dev, num_pms = 0, 0, 0, 0


def score_btw(x,y):
    obshto=0
    for i in x.skills:
        if i in y.skills:
            obshto+=1
    obshto*=(len(x.skills)+len(y.skills)-2*obshto)
    if x.company==y.company:
        obshto+=x.bonus*y.bonus
    return obshto

def score_thing(x,y,x1,y1):
    guy1 = PMS[ma3x[x][y]] if OFFICE[x][y]=='M'     else DEVS[ma3x[x][y]]
    guy2 = PMS[ma3x[x1][y1]] if OFFICE[x1][y1]=='M' else DEVS[ma3x[x1][y1]]
    return score_btw(guy1,guy2)


def score(s):
    global ma3x
    ma3x=list(list(-1 for j in range(m)) for i in range(n))
    res=0
    for i in range(num_dev):
        if s[i][0]!=-1:
            ma3x[s[i][0]][s[i][1]]=i
    for i in range(num_pms):
        if s[num_dev+i][0]!=-1:
            ma3x[s[num_dev+i][0]][s[num_dev+i][1]]=i

    for i in range(n):
        for j in range(m):
            if ma3x[i][j]!=-1:
                for x in moves:
                    if i+x[0]>=0 and j+x[1]>=0 and ma3x[i+x[0]][j+x[1]]!=-1:
                        res+=score_thing(i,j,i+x[0],j+x[1])

    return res


def main():
    global OFFICE, DEVS, PMS, ma3x, m, n, num_dev, num_pms, state
    filename = sys.argv[1]
    with open(filename) as file:
        split_input=file.readline().strip().split()
        m = int(split_input[0])
        n = int(split_input[1])
        for i in range(n):
            OFFICE.append(file.readline().strip())
        num_dev = int(file.readline().strip())
        for i in range(num_dev):
            split_input = file.readline().strip().split()
            DEVS.append(Worker(split_input[0], int(split_input[1]), set(split_input[3:])))
        num_pms = int(file.readline().strip())
        for i in range(num_pms):
            split_input = file.readline().strip().split()
            PMS.append(Worker(split_input[0], int(split_input[1]), set()))

    with open(initial_solution) as file:
        for i in range(num_dev+num_pms):
            split_input=file.readline().strip().split()
            if split_input[0]=='X':
                state.append((-1,-1))
            else:
                state.append((int(split_input[1]),int(split_input[0])))

    ma3x=list(list(-1 for j in range(m)) for i in range(n))
    print(score(state))
    
if __name__ == '__main__':
    main()

