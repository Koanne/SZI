from tkinter import *
from MapElement import MapElement
from State import State

class Collector(MapElement):

    def __init__(self, x, y, rotation):
        self.image = PhotoImage(file='collector2.png')
        self.maxCapacity = 10
        self.paperAmount = 0
        self.glassAmount = 0
        self.plasticAmount = 0
        self.otherAmount = 0
        self.state = State(x,y, rotation) # 0 - N, 1 - E, 2 - S, 3 - W
        self.states = []

    def updateImage(self):
        self.newImgName = "collector" + str(self.state.rotation) + ".png"
        self.image = PhotoImage(file=self.newImgName)

    def turnLeft(self):
        self.state.rotation = (self.state.rotation-1+4) % 4
        self.updateImage()

    def turnRight(self):
        self.state.rotation = (self.state.rotation+1) % 4
        self.updateImage()

    def goAhead(self):
        if self.state.rotation==0:
            self.state.position[1] += -1
        elif self.state.rotation==1:
            self.state.position[0] += 1
        elif self.state.rotation==2:
            self.state.position[1] += 1
        else:
            self.state.position[0] += -1