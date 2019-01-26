class Node(object):
    def __init__(self, label, edge=None):
        self.edge = edge
        self.label = label
        self.children=[]