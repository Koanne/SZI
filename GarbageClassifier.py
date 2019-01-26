from PIL import Image, ImageEnhance
from Example import Example
from Node import Node
from graphviz import Digraph
import math
import copy

class GarbageClassifier(object):
    def __init__(self, fileName):
        self.examples = []
        f = open(fileName,"r")
        for line in f:
            if line!="":
                ex = Example(line.replace("\n",""))
                self.examples.append(ex)
        self.attributes = dict()
        self.attributes["black"]=["0.0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"]
        self.attributes["gray"]=["0.0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"]
        self.attributes["white"]=["0.0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"]
        self.attributes["darkGreen"]=["0.0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"]
        self.attributes["darkBrown"]=["0.0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"]
        self.attributes["vivid"]=["0.0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9"]
        self.attributes["h1"]=["2","3","4"]
        self.attributes["h2"]=["6","7","8","9"]
        self.attributes["h3"]=["9","10","11","12","13","14","15","16","17","18","19","20"]
        self.attributes["h4"]=["9","10","11","12","13","14","15","16"]
        self.attributes["h5"]=["20","21","22","23","24","25","26","27","28","29","30","31","32"]
        self.attributes["h6"]=["13","14","15","16","17","18","19","20"]
        self.attributes["h7"]=["20","21","22","23","24","25","26","27","28","29","30","31","32"]
        self.getTree()
        self.printWholeTree()
    
    def getTree(self):
        self.tree = self.buildTree(self.examples,"PLASTIC",self.attributes)
    
    def buildTree(self, pExamples, default, pAttributes):
        if len(pExamples)==0:
            return Node(default)
        oneClassOnly, className = self.checkIfOneClassOnly(pExamples)
        if oneClassOnly:
            return Node(className)
        if len(pAttributes)==0:
            return Node(self.getMostCommonClass(pExamples))
        newDefault = self.getMostCommonClass(pExamples)
        minEntAttr = ""
        minEnt = 1000
        for attr in pAttributes:
            x = self.countAttributeEntropy(attr, pExamples)
            if x<minEnt:
                minEnt = x
                minEntAttr = attr
        
        node = Node(minEntAttr)
        for v in pAttributes[minEntAttr]:
            newExamples = []
            for ex in pExamples:
                if ex.attributes[minEntAttr]==v:
                    newExamples.append(ex)
            newAttributes = copy.deepcopy(pAttributes)
            del newAttributes[minEntAttr]
            n = self.buildTree(newExamples, newDefault, newAttributes)
            n.edge = v
            node.children.append(n)
        return node

    def countAttributeEntropy(self, attribute, pExamples):
        ent = 0.0
        for v in self.attributes[attribute]:
            plastic = 0.0
            glass = 0.0
            paper = 0.0
            all = 0.0
            partent = 0.0
            for ex in pExamples:
                if ex.attributes[attribute]==v:
                    if ex.decision=="PLASTIC":
                        plastic+=1.0
                    elif ex.decision=="GLASS":
                        glass+=1.0
                    else:
                        paper+=1.0
                    all+=1
            if all!=0:
                if plastic!=0:
                    partent+=(plastic/all)*math.log2(all/plastic)
                if paper!=0:
                    partent+=(paper/all)*math.log2(all/paper)
                if glass!=0:
                    partent+=(glass/all)*math.log2(all/glass)
                ent+=partent*(all/len(pExamples))
        return ent
    
    def checkIfOneClassOnly(self, pExamples):
        c = pExamples[0].decision
        for ex in pExamples:
            if ex.decision!=c:
                return [False, c]
        return [True, c]

    def getMostCommonClass(self, pExamples):
        plastic = 0
        paper = 0
        glass = 0
        for ex in pExamples:
            if ex.decision == "PAPER":
                paper+=1
            if ex.decision == "PLASTIC":
                plastic+=1
            if ex.decision == "GLASS":
                glass+=1
        maximum = max([paper, glass, plastic])
        if plastic==maximum:
            return "PLASTIC"
        elif paper==maximum:
            return "PAPER"
        elif glass==maximum:
            return "GLASS"
    
    def test(self, exString):
        ex = Example(exString)
        t = self.tree
        while len(t.children)!=0:
            v = ex.attributes[t.label]
            for c in t.children:
                if c.edge==v:
                    t = c
        return t.label
        
    def printTree(self, t, s, f):
        if len(t.children)!=0:
            for i in range(0, len(t.children)):
                f.edge(t.label +s, t.children[i].label+s+str(i), label=t.children[i].edge)
                self.printTree(t.children[i], s+str(i), f)
            
    def printWholeTree(self):
        f = Digraph('GarbageClassifier', filename='gc.gv')
        self.printTree(self.tree, "0", f)
        f.view()