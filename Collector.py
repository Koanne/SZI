from MapElement import MapElement

class Collector(MapElement):

    def __init__(self):
        self.color = 'black'
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