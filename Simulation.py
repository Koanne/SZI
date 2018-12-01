from tkinter import *
from random import randint
from Collector import Collector
from MapElement import MapElement
from Road import Road
from Dump import Dump
from Bin import Bin
import time

class Simulation(object):

    def checkIfPositionIsEmpty(self, position):
        for i in self.mapElements:
            if i.position == position:
                return False
        return True

    def addRoad(self, position1, position2):
        if position1[0]==position2[0]:
            for i in range(position2[1]-position1[1]):
                element = Road(position1[0], i)
                self.mapElements.append(element)
        elif position1[1]==position2[1]:
            for i in range(position2[0]-position1[0]):
                element = Road(i, position1[1])
                self.mapElements.append(element)

    def addRoads(self):
        self.addRoad([0,1],[self.gridWidth,1])
        self.addRoad([0,4],[self.gridWidth,4])
        self.addRoad([0,7],[self.gridWidth,7])
        r = randint(1, 6)
        for i in range(0, r):
            s = randint(1, self.gridWidth-2)
            self.addRoad([s, 1],[s, self.gridHeight-1])

    def __init__(self, binsAmount):
        self.gridWidth = 20
        self.gridHeight = 9
        self.fieldSize = 64
        self.window = Tk()
        self.canvas = Canvas(self.window, width = self.fieldSize*self.gridWidth, height = self.fieldSize*self.gridHeight)
        self.binsAmount = binsAmount
        self.window.title("Simulation")
        self.collector = Collector()
        self.mapElements = []
        self.grassImage = PhotoImage(file='grass.png')
        types = ['plastic', 'paper', 'glass', 'other']
        n = 0
        for j in types:
            new = Dump(n, 0, j)
            n = n + 1 
            self.mapElements.append(new)


        self.addRoads()

        for i in range(0, binsAmount):
            rightPosition = False
            while not rightPosition:
                x = randint(0, self.gridWidth - 1)
                y = randint (0, self.gridHeight - 1)
                if self.checkIfPositionIsEmpty([x,y]):
                    rightPosition = True
            element = Bin(x, y)
            self.mapElements.append(element)
        
        self.collector.position = [1,1]

    def display(self):
  
        for i in range(0, self.gridWidth):
            for j in range(0, self.gridHeight):
                self.canvas.create_image(i*self.fieldSize, j*self.fieldSize, image=self.grassImage, anchor=NW)


        for i in self.mapElements:
            x = i.position[0]
            y = i.position[1]
            self.canvas.create_image(x*self.fieldSize, y*self.fieldSize, image=i.image, anchor=NW)
        x = self.collector.position[0]
        y = self.collector.position[1]
        self.canvas.create_image(x*self.fieldSize, y*self.fieldSize, image=self.collector.image, anchor=NW)
        self.canvas.pack()
    
    def go(self):
        self.display()
        time.sleep(1.5)
        self.collector.move()
        self.window.update_idletasks()
        self.window.update()

    def start(self):
        while True:
            self.go()