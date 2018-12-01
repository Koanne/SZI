from tkinter import *
from MapElement import MapElement

class Collector(MapElement):

    def __init__(self):
        self.image = PhotoImage(file='collector.png')
        self.position = [0,0]
        self.maxCapacity = 10
        self.paperAmount = 0
        self.glassAmount = 0
        self.plasticAmount = 0
        self.otherAmount = 0

    def display(self):
        pass
    
    def move(self):
        pass
    
    def moveRight(self):
        self.position[0] += 1

    def moveLeft(self):
        self.position[0] += -1

    def moveUp(self):
        self.position[1] += -1

    def moveDown(self):
        self.position[0] += 1          