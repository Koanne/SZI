class State(object):

    def __init__(self, x, y, rotation):
        self.position = [x, y]
        self.rotation = rotation
        self.action=""
        self.parent = None
        self.cost = 0