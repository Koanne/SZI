from tkinter import *
from MapElement import MapElement

class Dump(MapElement):
    def __init__(self, x, y, type):
        self.position = [x,y]
        self.type = type 
        if type == 'paper':
            self.image = PhotoImage(file='paper.png')
        elif type == 'plastic':
            self.image = PhotoImage(file='plastic.png')
        elif type == 'glass':
            self.image = PhotoImage(file='glass.png')
        else:
            self.image = PhotoImage(file='other.png')

    def action(self):
        pass

    def display(self):
        pass