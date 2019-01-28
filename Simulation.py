from tkinter import *
from random import randint
from Collector import Collector
from MapElement import MapElement
from Road import Road
from Grass import Grass
from Dump import Dump
from Bin import Bin
from State import State
from MovementLogic import MovementLogic
from GarbageClassifier import GarbageClassifier
from ImageExample import ImageExample
from Example import Example
import time
import copy
import math
from PriorityQueue import PriorityQueue
from PIL import ImageTk, Image
import tensorflow as tf
import numpy as np

class Simulation(object):

    def checkIfPositionIsEmpty(self, position):
        for i in self.mapElements:
            if i.position == position:
                return False
        return True

    def __init__(self, binsAmount):
        self.gridWidth = 20
        self.gridHeight = 9
        self.fieldSize = 64
        self.window = Tk()
        self.canvas = Canvas(self.window, width = self.fieldSize*self.gridWidth, height = self.fieldSize*self.gridHeight)
        self.binsAmount = binsAmount
        self.window.title("Simulation")
        self.collector = Collector(1, 1, 1)
        self.positionsToVisit = []
        self.mapElements = []
        self.addDumps()
        self.addRoads()
        self.addBins()
        self.addGrass()
        self.MovementLogic = MovementLogic(self.mapElements, self.gridWidth, self.gridHeight)
        self.classifier = GarbageClassifier("learningExamples.txt")

    def addDumps(self):
        types = ['plastic', 'paper', 'glass', 'other']
        n = 0
        for j in types:
            new = Dump(n, 0, j)
            n = n + 1
            self.mapElements.append(new)

    def addRoad(self, position1, position2):
        if position1[0]==position2[0]:
            for i in range(position1[1], position2[1]+1):
                if self.checkIfPositionIsEmpty([position1[0], i]):
                    element = Road(position1[0], i)
                    self.mapElements.append(element)
        elif position1[1]==position2[1]:
            for i in range(position1[0], position2[0]+1):
                if self.checkIfPositionIsEmpty([i, position1[1]]):
                    element = Road(i, position1[1])
                    self.mapElements.append(element)

    def addRoads(self):
        self.addRoad([0,1],[self.gridWidth,1])
        self.addRoad([0,4],[self.gridWidth,4])
        self.addRoad([0,7],[self.gridWidth,7])
        r = randint(1, 6)
        for i in range(0, r):
            s = randint(1, self.gridWidth-2)
            self.addRoad([s, 1],[s, self.gridHeight-2])

    def addBins(self):
        for i in range(0, self.binsAmount):
            rightPosition = False
            while not rightPosition:
                x = randint(0, self.gridWidth - 1)
                y = randint (0, self.gridHeight - 1)
                if self.checkIfPositionIsEmpty([x,y]):
                    rightPosition = True
            element = Bin(x, y)
            self.positionsToVisit.append([x,y])
            self.mapElements.append(element)

    def addGrass(self):
        for i in range (0, self.gridWidth):
            for j in range (0, self.gridHeight):
                if self.checkIfPositionIsEmpty([i,j]):
                    element = Grass(i,j)
                    self.mapElements.append(element)

    def display(self):
        for i in self.mapElements:
            x = i.position[0]
            y = i.position[1]
            self.canvas.create_image(x*self.fieldSize, y*self.fieldSize, image=i.image, anchor=NW)
        x = self.collector.state.position[0]
        y = self.collector.state.position[1]
        self.canvas.create_image(x*self.fieldSize, y*self.fieldSize, image=self.collector.image, anchor=NW)
        self.canvas.pack()

    def update(self):
        self.display()
        self.window.update_idletasks()
        self.window.update()
        time.sleep(0.5)

    def classify(self):
        for i in range (0,5):
            r = randint(1,40)
            name = "./photos/test/test"+str(r)+".jpg"
            im = ImageExample(name)
            image = ImageTk.PhotoImage(Image.open(name))
            result = self.classifier.test(im.getString())
            self.canvas.create_image(350, 100, image=image, anchor=NW)
            self.canvas.pack()
            self.window.update_idletasks()
            self.window.update()
            time.sleep(0.5)
            self.canvas.create_text(420,150,fill="black",font="Times 20",text=result)
            self.canvas.pack()
            self.window.update_idletasks()
            self.window.update()
            time.sleep(2)

    def predictDigits(self):
        sess = tf.Session()

        saver = tf.train.import_meta_graph('./src/model/my-model.meta')
        saver.restore(sess,tf.train.latest_checkpoint('./model'))
        print("Model został wczytany.")

        graph = tf.get_default_graph()
        output_layer = graph.get_tensor_by_name("output:0")
        X = graph.get_tensor_by_name("X:0")

        r = randint(0,9);
        img = np.invert(Image.open("../test_digits/house_test_" + str(r) + ".png"))

        prediction = sess.run(tf.argmax(output_layer,1), feed_dict={X: [img]})
        print ("Rozpoznanie dla testowanego obrazka:", np.squeeze(prediction))


    def start(self):
        for p in self.positionsToVisit:
            for zz in self.mapElements:
                if zz.position == p:
                    zz.searching = True
                    zz.updateImage()
            self.update()

            actions = self.MovementLogic.getActions(self.collector.state, p)
            if actions is not None:
                for i in actions:
                    print(i)
                    self.update()
                    self.collector.doAction(i)
            self.update()
            self.predictDigits()
            self.classify()
            for zz in self.mapElements:
                if zz.position == p:
                    zz.searching = False
                    zz.updateImage()
