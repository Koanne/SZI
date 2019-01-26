from PIL import Image, ImageEnhance
import math
from skimage import data, filters, io
from matplotlib import pyplot as plt
import os
import cv2
import numpy as np
import imutils

class ImageExample(object):
    def __init__(self, fileName, decision=""):
        self.decision = decision
        self.whitePixels = 0.0
        self.grayPixels = 0.0
        self.blackPixels = 0.0
        self.greenPixels = 0.0
        self.bluePixels = 0.0
        self.redPixels = 0.0
        self.yellowPixels = 0.0
        self.darkGreenPixels = 0.0
        self.darkBrownPixels = 0.0
        self.magentaPixels = 0.0
        self.vividPixels = 0.0
        self.pixels = 0.0
        self.colors = [(0, 0, 0), (255, 255, 255), (191, 195, 201), (0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 115, 0), (150, 60, 0)]

        stri = os.getcwd()
        self.binaryImage = cv2.imread(stri + fileName, cv2.IMREAD_GRAYSCALE)
        self.transformImage()
        self.setHuMoments()
        self.colorImage = Image.open(fileName)
        self.colorImage = ImageEnhance.Brightness(self.colorImage).enhance(1.4)
        self.colorImage = ImageEnhance.Contrast(self.colorImage).enhance(1.3)
        self.changeImageColors()
        self.countPixels()

    def findNearestColor(self, pixelColor):
        closest_colors = sorted(self.colors, key=lambda color: self.getDistance(color, pixelColor))
        return closest_colors[0]
    
    def changeImageColors(self):
        pixels = self.colorImage.load()
        for i in range(self.colorImage.size[0]):
            for j in range (self.colorImage.size[1]):
                pixels[i,j] = self.findNearestColor(pixels[i,j])

    def countPixels(self):
        pixels = self.colorImage.load()
        for i in range(self.colorImage.size[0]):
            for j in range (self.colorImage.size[1]):
                if pixels[i,j] == (0, 0, 0):
                    self.blackPixels+=1
                elif pixels[i,j] == (255, 255, 255):
                    self.whitePixels+=1
                elif pixels[i,j] == (191, 195, 201):
                    self.grayPixels+=1
                elif pixels[i,j] == (0, 0, 255):
                    self.bluePixels+=1
                elif pixels[i,j] == (255, 0, 0):
                    self.redPixels+=1
                elif pixels[i,j] == (255, 255, 0):
                    self.yellowPixels+=1
                elif pixels[i,j] == (255, 0, 255):
                    self.magentaPixels+=1
                elif pixels[i,j] == (0, 115, 0):
                    self.darkGreenPixels+=1
                elif pixels[i,j] == (150, 60, 0):
                    self.darkBrownPixels+=1
                self.pixels+=1
        self.blackPixels = round((self.blackPixels / self.pixels),1)
        self.grayPixels = round((self.grayPixels / self.pixels),1)
        self.whitePixels = round((self.whitePixels / self.pixels),1)
        self.darkBrownPixels = round((self.darkBrownPixels / self.pixels),1)
        self.darkGreenPixels = round((self.darkGreenPixels / self.pixels),1)
        self.vividPixels = round((self.magentaPixels+self.bluePixels+self.yellowPixels+self.redPixels)/self.pixels,1)
    
    def getDistance(self, c1, c2):
        (r1,g1,b1) = c1
        (r2,g2,b2) = c2
        return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

    def getString(self):
        exst = ""
        exst += "black:" + str(self.blackPixels)+";"
        exst += "gray:" + str(self.grayPixels)+";"
        exst += "white:" + str(self.whitePixels)+";"
        exst += "vivid:" + str(self.vividPixels)+";"
        exst += "darkBrown:" + str(self.darkBrownPixels)+";"
        exst += "darkGreen:" + str(self.darkGreenPixels)+";"
        exst += "h1:" + str(self.huMoments[0]).replace("[","").replace("]","").replace(".","")+";"
        exst += "h2:" + str(self.huMoments[1]).replace("[","").replace("]","").replace(".","")+";"
        exst += "h3:" + str(self.huMoments[2]).replace("[","").replace("]","").replace(".","")+";"
        exst += "h4:" + str(self.huMoments[3]).replace("[","").replace("]","").replace(".","")+";"
        exst += "h5:" + str(self.huMoments[4]).replace("[","").replace("]","").replace(".","")+";"
        exst += "h6:" + str(self.huMoments[5]).replace("[","").replace("]","").replace(".","")+";"
        exst += "h7:" + str(self.huMoments[6]).replace("[","").replace("]","").replace(".","")+";"
        exst += "decision:" + self.decision
        return exst

    def transformImage(self):
        _, self.binaryImage = cv2.threshold(self.binaryImage, 128, 255, cv2.THRESH_BINARY)

    def setHuMoments(self):
        moments = cv2.moments(self.binaryImage)
        self.huMoments = cv2.HuMoments(moments)
        for i in range(0,7):
            if self.huMoments[i]!=0:
                self.huMoments[i] = abs(round(-1* math.copysign(1.0, self.huMoments[i]) * math.log10(abs(self.huMoments[i]))))
        if self.huMoments[0]<3:
            self.huMoments[0]=2
        if self.huMoments[0]>3:
            self.huMoments[0]=4
        if self.huMoments[1]<7:
            self.huMoments[1]=6
        if self.huMoments[1]>8:
            self.huMoments[1]=9
        if self.huMoments[2]<10:
            self.huMoments[2]=9
        if self.huMoments[2]>19:
            self.huMoments[2]=20
        if self.huMoments[3]<10:
            self.huMoments[3]=9
        if self.huMoments[3]>15:
            self.huMoments[3]=16
        if self.huMoments[4]<21:
            self.huMoments[4]=20
        if self.huMoments[4]>31:
            self.huMoments[4]=32
        if self.huMoments[5]<14:
            self.huMoments[5]=13
        if self.huMoments[5]>19:
            self.huMoments[5]=20
        if self.huMoments[6]<21:
            self.huMoments[6]=20
        if self.huMoments[6]>31:
            self.huMoments[6]=32
