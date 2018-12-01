from tkinter import *

from MapElement import MapElement

class Bin(MapElement):
    def __init__(self, x, y):
        self.position = [x,y]
        self.image = PhotoImage(file='house.png')
        self.state = 'full'

    def action(self):
        pass

    def display(self):
        pass