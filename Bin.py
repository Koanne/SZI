from tkinter import *

from MapElement import MapElement

class Bin(MapElement):
    def __init__(self, x, y):
        self.position = [x,y]
        self.image = PhotoImage(file='house.png')
        self.state = 'full'
        self.searching = False

    def action(self):
        pass

    def isPassable(self):
        return False

    def updateImage(self):
        if self.searching:
            self.image = PhotoImage(file='houseUpdate.png')
        else:
            self.image = PhotoImage(file='house.png')
