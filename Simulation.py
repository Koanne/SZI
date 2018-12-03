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

class Simulation(object):

##################################################################### PODSTAWOWE METODY
    def checkIfPositionIsEmpty(self, position):
        for i in self.mapElements:
            if i.position == position:
                return False
        return True

    def returnElementAhead(self):
        pass

##################################################################### GENEROWANIE MAPY
    def __init__(self, binsAmount):
        self.gridWidth = 20
        self.gridHeight = 9
        self.fieldSize = 64
        self.window = Tk()
        self.canvas = Canvas(self.window, width = self.fieldSize*self.gridWidth, height = self.fieldSize*self.gridHeight)
        self.binsAmount = binsAmount
        self.window.title("Simulation")
        self.collector = Collector(1, 1, 2)
        self.positionsToVisit = []
        self.fringeBins = []
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
            self.positionsToVisit.append([x,y])
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
        while True:
            self.moveCollector()

##################################################################### RUCH AGENTA
    def moveCollector(self):
        self.update()
        self.collector.turnLeft()

    def graphSearch(self):
        pass

#####################################################################

    def testGoal(self)
        for i in self.positionsToVisit:
            if (position[0] == self.collector.position[0] + 1) or (position[0] == self.collector.position[0] - 1):
                return True
            if (position[1] == self.collector.position[1] + 1) or (position[0] == self.collector.position[1] - 1):
                return True
        return False

    def getPriority(self, pos1, pos2)
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
