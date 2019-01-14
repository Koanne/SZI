from PIL import Image, ImageEnhance
from Example import Example

class GarbageClassifier(object):
    def __init__(self):
        self.examples = []
        self.amount = 10

        for i in range (1, self.amount):
            ex = Example("./photos/plastic/plastic"+str(i)+".jpg", "plastic")
            self.examples.append(ex)
        for i in range (1, self.amount):
            ex = Example("./photos/paper/paper"+str(i)+".jpg", "paper")
            self.examples.append(ex)
        for i in range (1, self.amount):
            ex = Example("./photos/glass/glass"+str(i)+".jpg", "glass")
            self.examples.append(ex)

    def buildTree(self):
        pass