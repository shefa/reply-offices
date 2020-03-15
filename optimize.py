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

def score_single(x,y):
    if x==-1:
        return 0

    nx, ny, res = 0, 0, 0
    for i in moves_full:
        nx, ny = x+i[0], y+i[1]
        if nx>=0 and nx<n and ny>=0 and ny<m and ma3x[nx][ny]!=-1:
            res+=score_thing(x,y,nx,ny)

    return res

def update(x,y):
    #print("updating!!", x, y, state[x], state[y], OFFICE[state[x][0]][state[x][1]], OFFICE[state[y][0]][state[y][1]] if state[y][0]!=-1 else 'Empty')
    if state[y][0]!=-1:
        ma3x[state[x][0]][state[x][1]], ma3x[state[y][0]][state[y][1]]=ma3x[state[y][0]][state[y][1]], ma3x[state[x][0]][state[x][1]]
    else:
        ma3x[state[x][0]][state[x][1]] = y if y < num_dev else y-num_dev
    state[x], state[y] = state[y], state[x]

def score_swap(x,y):
    #print("swap", x, y, state[x], state[y], OFFICE[state[x][0]][state[x][1]], OFFICE[state[y][0]][state[y][1]] if state[y][0]!=-1 else 'Empty')
    tmpx=ma3x[state[x][0]][state[x][1]]
    oldscore = score_single(state[x][0], state[x][1]) + score_single(state[y][0],state[y][1])
    if state[y][0]!=-1:
        ma3x[state[x][0]][state[x][1]], ma3x[state[y][0]][state[y][1]]=ma3x[state[y][0]][state[y][1]], ma3x[state[x][0]][state[x][1]]
    else:
        ma3x[state[x][0]][state[x][1]]= y if y < num_dev else y-num_dev
    newscore = score_single(state[x][0], state[x][1]) + score_single(state[y][0],state[y][1])
    
    if state[y][0]!=-1:
        ma3x[state[x][0]][state[x][1]], ma3x[state[y][0]][state[y][1]]=ma3x[state[y][0]][state[y][1]], ma3x[state[x][0]][state[x][1]]
    else:
        ma3x[state[x][0]][state[x][1]]=tmpx
    return newscore-oldscore


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


def better_solution(scorez,solution):
    global state2
    print("found better solution",scorez)
    f = open(initial_solution+'x', "w")
    solution2=[(i[1],i[0]) for i in solution]
    f.write(str(solution2)[2:-2].replace(',','').replace(') (','\n'))
    f.close()



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

    print("initial score",score(state))

    simulated_annealing = SimulatedAnnealingWithNonImproveStoppingCriterion(
        random,
        get_neighbourhood_function(random,num_dev),
        score_swap,
        30,
        score(state),
        500,
        get_multiplicative_cooling_schedule_function(0.92),
        1500000,
        better_solution,
        update
    )
    simulated_annealing.run(state)

if __name__ == '__main__':
    main()

