from State import State
import copy
import math
from PriorityQueue import PriorityQueue

class MovementLogic(object):
    def __init__(self, mapElements, gridWidth, gridHeight):
        self.mapElements = mapElements
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight

    def checkIfPositionIsCorrect(self, position):
        if position[0]<0 or position[0]>=self.gridWidth or position[1]<0 or position[1]>=self.gridHeight:
            return False
        else:
            return True
        
    def stateValueExists(self, state, states):
        found = False
        for i in states:
            if str(str(i.position)+str(i.rotation))==str(str(state.position)+str(state.rotation)) :
                found = True
                break
        return found

    def returnElementAhead(self, state):
        if state.rotation==0:
            for i in self.mapElements:
                if state.position[0]==i.position[0] and state.position[1]-1==i.position[1]:
                    return i
        elif state.rotation==1:
            for i in self.mapElements:
                if state.position[1]==i.position[1] and state.position[0]+1==i.position[0]:
                    return i
        elif state.rotation==2:
            for i in self.mapElements:
                if state.position[0]==i.position[0] and state.position[1]+1==i.position[1]:
                    return i
        elif state.rotation==3:
            for i in self.mapElements:
                if state.position[1]==i.position[1] and state.position[0]-1==i.position[0]:
                    return i
    
    def getActions(self, start, final):
        print("*****************************************************************************************************")
        print("Cel: "+str(final))
        actions = []
        explored = []
        currentState =  start
        currentState.priority = 99
        fringe = PriorityQueue()
        fringe.insert(currentState)

        while not self.testGoal(currentState, final):
            currentState = fringe.delete(currentState, self.mapElements)
            print("Zmieniamy obecny stan")
            print(str(currentState.position), str(currentState.rotation))

            explored.append(currentState)

            if self.testGoal(currentState, final):
                for i in explored:
                    actions.append(i.action)
                return actions
            #explored.append(currentState)
            for j in self.getSuccessors(currentState):
                print("Sprawdzam dany następnik:")
                x = copy.deepcopy(j[1])
                x.action = j[0]
                x.parent = copy.deepcopy(currentState)
                x.priority = self.getPriority(x, final)
                print(str(x.position), str(x.rotation), "priorytet: ", str(x.priority))
                if not self.stateValueExists(x, explored) and not self.stateValueExists(x, fringe.queue):
                    fringe.insert(x)
                    print("Dodano następnik, nie było go ani we fringe ani w explored")
                elif self.stateValueExists(x, fringe.queue):
                    print("Następnik był we fringe")
                    for i in fringe.queue:
                        if x.position==i.position and x.rotation==i.rotation and x.priority<i.priority:
                            i = copy.deepcopy(x)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    def testGoal(self, state, p):
        x = p[0]
        y = p[1]
        if ((state.position[0] == x+1) or (state.position[0] == x-1)) and state.position[1]==y:
            return True
        if ((state.position[1] == y+1) or (state.position[1] == y-1)) and state.position[0]==x:
            return True
        return False

    ################################# metoda do zmiany?
    # problemem jest sytuacja, gdy collectorowi nie opłaca się jechać prosto i musi skręcić
    # wtedy oba skręty mają ten sam priorytet, a nie powinny
    # i to jest chyba w sumie tylko do zmiany?
    def getPriority(self, s, finalPosition):
        # [x,y] = s.position
        # r = s.rotation
        # b = 0

        # if r == 0:
        #     y -= 1
        # elif r == 1:
        #     x +=1
        # elif r == 2:
        #     y += 1
        # elif r == 3:
        #     x -= 1

        # if self.returnElementAhead(s) is not None:
        #      if self.returnElementAhead(s).isPassable():
        #          b = 100
        return self.getDistance(s.position, finalPosition) + self.getPathCost(s)  #<- tylko to powinno tu zostać
        # return self.getDistance([x,y], finalPosition) - b + cost

    # funkcja h(n)
    def getDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def getSuccessors(self, state):
        succ = []
        if self.returnElementAhead(state) is not None:
            if self.returnElementAhead(state).isPassable():
                astate = copy.deepcopy(state)
                if astate.rotation==0:
                    astate.position[1] += -1
                elif astate.rotation==1:
                    astate.position[0] += 1
                elif astate.rotation==2:
                    astate.position[1] += 1
                else:
                    astate.position[0] += -1
                astate.cost=self.returnElementAhead(state).getCost()
                if self.checkIfPositionIsCorrect(astate.position):
                    succ.append(["goAhead", astate])
        lstate = copy.deepcopy(state)
        lstate.rotation = (lstate.rotation-1+4)%4
        lstate.cost = 1
        succ.append(["turnLeft", lstate])
        rstate = copy.deepcopy(state)
        rstate.rotation = (rstate.rotation+1)%4
        rstate.cost = 1
        succ.append(["turnRight", rstate])
        return succ

    ################################# metoda do zmiany?
    def getPathCost(self, currentState):
        # na razie zwraca faktyczny koszt ścieżki przebytej od startu do currentState
        # ale może powinna zwracać coś innego XD
        # albo po prostu źle liczy XD
        # to jest ta funkcja g(n) jakby co
        state = copy.copy(currentState)
        cost = 0
        while state.parent is not None:
            cost += state.cost
            state = state.parent
        return cost




    