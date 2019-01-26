class Example(object):
    def __init__(self, exampleString):
        
        self.attributes = dict()
        self.decision = ""
        info = exampleString.split(';')
        for i in info:
            attr, value = i.split(":")
            if attr=="decision":
                self.decision=value
            else:
                self.attributes[attr]=value