from tkinter import *
from random import randint
from Collector import Collector
from MapElement import MapElement
from Road import Road
from Grass import Grass
from Dump import Dump
from Bin import Bin
from State import State
import time
import copy
import math
from PriorityQueue import PriorityQueue

class Simulation(object):

##################################################################### PODSTAWOWE METODY
    def checkIfPositionIsCorrect(self, position):
        if position[0]<0 or position[0]>=self.gridWidth or position[1]<0 or position[1]>=self.gridHeight:
            return False
        else:
            return True
        
    def checkIfPositionIsEmpty(self, position):
        for i in self.mapElements:
            if i.position == position:
                return False
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

##################################################################### GENEROWANIE MAPY
    def __init__(self, binsAmount):
        self.gridWidth = 20
        self.gridHeight = 9
        self.fieldSize = 64
        self.window = Tk()
        self.canvas = Canvas(self.window, width = self.fieldSize*self.gridWidth, height = self.fieldSize*self.gridHeight)
        self.binsAmount = binsAmount
        self.window.title("Simulation")
        self.collector = Collector(1, 1, 1)
        self.positionToVisit = [3,4]
        self.mapElements = []
        self.addDumps()
        self.addRoads()
        self.addBins()
        self.addGrass()


    def addDumps(self):
        types = ['plastic', 'paper', 'glass', 'other']
        n = 0
        for j in types:
            new = Dump(n, 0, j)
            n = n + 1
            self.mapElements.append(new)

    def addRoad(self, position1, position2):
        if position1[0]==position2[0]:
            for i in range(position1[1], position2[1]+1):
                if self.checkIfPositionIsEmpty([position1[0], i]):
                    element = Road(position1[0], i)
                    self.mapElements.append(element)
        elif position1[1]==position2[1]:
            for i in range(position1[0], position2[0]+1):
                if self.checkIfPositionIsEmpty([i, position1[1]]):
                    element = Road(i, position1[1])
                    self.mapElements.append(element)

    def addRoads(self):
        self.addRoad([0,1],[self.gridWidth,1])
        self.addRoad([0,4],[self.gridWidth,4])
        self.addRoad([0,7],[self.gridWidth,7])
        r = randint(1, 6)
        for i in range(0, r):
            s = randint(1, self.gridWidth-2)
            self.addRoad([s, 1],[s, self.gridHeight-2])

    def addBins(self):
        for i in range(0, self.binsAmount):
            rightPosition = False
            while not rightPosition:
                x = randint(0, self.gridWidth - 1)
                y = randint (0, self.gridHeight - 1)
                if self.checkIfPositionIsEmpty([x,y]):
                    rightPosition = True
            element = Bin(x, y)
            self.mapElements.append(element)

    def addGrass(self):
        for i in range (0, self.gridWidth):
            for j in range (0, self.gridHeight):
                if self.checkIfPositionIsEmpty([i,j]):
                    element = Grass(i,j)
                    self.mapElements.append(element)

    def display(self):
        for i in self.mapElements:
            x = i.position[0]
            y = i.position[1]
            self.canvas.create_image(x*self.fieldSize, y*self.fieldSize, image=i.image, anchor=NW)
        x = self.collector.state.position[0]
        y = self.collector.state.position[1]
        self.canvas.create_image(x*self.fieldSize, y*self.fieldSize, image=self.collector.image, anchor=NW)
        self.canvas.pack()

    def update(self):
        self.display()
        self.window.update_idletasks()
        self.window.update()
        time.sleep(1.5)

    def start(self):
        #while True:
        self.update()
        actions = self.graphSearch()
        #print(str(actions))
        for i in actions:
            print(i)
            self.update()
            self.collector.doAction(i)
            

##################################################################### RUCH AGENTA
    def graphSearch(self):
        print(str(self.positionToVisit))
        # time.sleep(10)
        actions = []
        explored = []
        currentState =  copy.deepcopy(self.collector.state)
        currentState.priority = 1
        fringe = PriorityQueue()
        fringe.insert(currentState)

        while not self.testGoal(currentState):
            currentState = fringe.delete(currentState)
            print("Zmieniamy obecny stan")
            print(str(currentState.position), str(currentState.rotation))


            if self.testGoal(currentState):
                for j in fringe.queue:
                    print(str(j.priority)+"."+str(j.position)+str(j.rotation))
                for i in explored:
                    actions.append(i.action)
                return actions
            
            explored.append(currentState)
            for j in self.getSuccessors(currentState):
                print("Sprawdzam dany następnik:")
                x = copy.deepcopy(j[1])
                x.action = j[0]
                x.parent = copy.deepcopy(currentState)
                x.priority = self.getPriority(x)
                print(str(x.position), str(x.rotation))
                if not self.stateValueExists(x, explored) and not self.stateValueExists(x, fringe.queue):
                    fringe.insert(x)
                    print("Dodano następnik, nie było go ani we fringe ani w explored")
                elif self.stateValueExists(x, fringe.queue):
                    print("Następnik był we fringe")
                    for i in fringe.queue:
                        if x.position==i.position and x.rotation==i.rotation and x.priority<i.priority:
                            i = copy.deepcopy(x)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # time.sleep(5)
##################################################################### 

    def testGoal(self, state):
        #for [x,y] in self.positionsToVisit:
        x = self.positionToVisit[0]
        y = self.positionToVisit[1]
        if ((state.position[0] == x+1) or (state.position[0] == x-1)) and state.position[1]==y:
            return True
        if ((state.position[1] == y+1) or (state.position[1] == y-1)) and state.position[0]==x:
            return True
        return False

    def getPriority(self, s):
        [x,y] = s.position
        r = s.rotation
        if r == 0:
            y -= 1
        elif r == 1:
            x +=1
        elif r == 2:
            y += 1
        elif r == 3:
            x -= 1
        return self.getDistance([x,y], self.positionToVisit)

    def getDistance(self, pos1, pos2):
        return math.sqrt(abs(pos1[0] - pos2[0])**2 + abs(pos1[1] - pos2[1])**2)

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
                if self.checkIfPositionIsCorrect(astate.position):
                    succ.append(["goAhead", astate])
        lstate = copy.deepcopy(state)
        lstate.rotation = (lstate.rotation-1+4)%4
        succ.append(["turnLeft", lstate])
        rstate = copy.deepcopy(state)
        rstate.rotation = (rstate.rotation+1)%4
        succ.append(["turnRight", rstate])
        return succ
