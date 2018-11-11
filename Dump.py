from MapElement import MapElement

class Dump(MapElement):
    def __init__(self, x, y, type):
        self.position = [x,y]
        self.type = type 
        if type == 'paper':
            self.color = 'blue'
        elif type == 'plastic':
            self.color = 'yellow'
        elif type == 'glass':
            self.color = 'green'
        else:
            self.color = 'brown'

    def action(self):
        pass

    def display(self):
        pass