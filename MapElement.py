from tkinter import *

class MapElement(object):

    def __init__(self, x, y):
        self.position = [x, y]
        self.image = PhotoImage(file='grass.png')

    def action(self):
        pass

    def display(self):
        pass