from tkinter import *
from random import randint
from Collector import Collector
from MapElement import MapElement
from Dump import Dump
from Bin import Bin

class Simulation(object):

    def checkIfPositionIsEmpty(self, position):
        for i in self.mapElements:
            if i.position == position:
                return False
        return True
            
    def __init__(self, gridSize, binsAmount):
        self.size = 500
        self.gridSize = gridSize
        self.fieldSize = self.size / self.gridSize
        self.window = Tk()
        self.canvas = Canvas(self.window, width = self.size, height = self.size)
        self.binsAmount = binsAmount
        self.window.title("Simulation")
        self.collector = Collector()
        self.mapElements = []

        types = ['plastic', 'paper', 'glass', 'other']
        n = 1
        for j in types:
            new = Dump(0, n, j)
            n = n + 1 
            self.mapElements.append(new)

        for i in range(0, binsAmount):
            rightPosition = False
            while not rightPosition:
                x = randint(0, self.gridSize - 1)
                y = randint (0, self.gridSize - 1)
                if self.checkIfPositionIsEmpty([x,y]):
                    rightPosition = True
            element = Bin(x, y)
            self.mapElements.append(element)
        
        self.collector.position = [0,0]

    def display(self):
        self.canvas.create_rectangle(0, 0, self.size, self.size, fill="pink")
        for i in self.mapElements:
            x = i.position[0]
            y = i.position[1]
            self.canvas.create_oval(x*self.fieldSize, y*self.fieldSize, x*self.fieldSize+self.fieldSize, y*self.fieldSize+self.fieldSize, fill=i.color)
        x = self.collector.position[0]
        y = self.collector.position[1]
        self.canvas.create_oval(x*self.fieldSize, y*self.fieldSize, x*self.fieldSize+self.fieldSize, y*self.fieldSize+self.fieldSize, fill="black")
        self.canvas.pack()
    
    def go(self):
        self.display()
    
    def start(self):
        while True:
            self.go()
            self.window.mainloop()