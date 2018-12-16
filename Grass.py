from tkinter import *

from MapElement import MapElement

class Grass(MapElement):
    def __init__(self, x, y):
        self.position = [x,y]
        self.image = PhotoImage(file='grass.png')

    def action(self):
        pass
    
    def isPassable(self):
        return True

    def getCost(self):
        return 4