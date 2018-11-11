from MapElement import MapElement

class Bin(object):
    def __init__(self, x, y):
        self.position = [x,y]
        self.color = 'red'
        self.state = 'full'

    def action(self):
        pass

    def display(self):
        pass