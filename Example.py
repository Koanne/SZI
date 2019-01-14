from PIL import Image, ImageEnhance
import math

class Example(object):
    def __init__(self, fileName, decision):
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
        self.pixels = 0.0
        self.colors = [(0, 0, 0), (255, 255, 255), (191, 195, 201), (0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 115, 0), (94, 37, 0)]

        self.image = Image.open(fileName)
        self.transformedImage = ImageEnhance.Brightness(self.image).enhance(1.4)
        self.transformedImage = ImageEnhance.Contrast(self.transformedImage).enhance(1.3)
        self.changeImageColors()
        self.countPixels()

    def findNearestColor(self, pixelColor):
        # if pixelColor in self.colors:
        #     return pixelColor
        # x = convert_color(pixelColor, LabColor)
        # newColors = []
        # for i in self.colors:
        #     newColors.append(convert_color(i, LabColor))
        # n = min(newColors, key=lambda fc:delta_e_cie2000(x, fc))
        # m = convert_color(n, sRGBColor)
        # pixelColor = m
        # return pixelColor
        closest_colors = sorted(self.colors, key=lambda color: self.distance(color, pixelColor))
        return closest_colors[0]
    
    def changeImageColors(self):
        pixels = self.transformedImage.load()
        for i in range(self.transformedImage.size[0]):
            for j in range (self.transformedImage.size[1]):
                pixels[i,j] = self.findNearestColor(pixels[i,j])

    def countPixels(self):
        pixels = self.transformedImage.load()
        for i in range(self.transformedImage.size[0]):
            for j in range (self.transformedImage.size[1]):
                if pixels[i,j] == (0, 0, 0):
                    self.blackPixels+=1
                elif pixels[i,j] == (255, 255, 255):
                    self.whitePixels+=1
                elif pixels[i,j] == (191, 195, 201):
                    self.grayPixels+=1
                elif pixels[i,j] == (0, 255, 0):
                    self.greenPixels+=1
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
                elif pixels[i,j] == (94, 37, 0):
                    self.darkBrownPixels+=1
    
    def distance(self, c1, c2):
        (r1,g1,b1) = c1
        (r2,g2,b2) = c2
        return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

    def getString(self):
        exst = ""
        exst += "black:" + str(self.blackPixels)
        exst += "gray:" + str(self.grayPixels)
        exst += "white:" + str(self.whitePixels)
        exst += "red:" + str(self.redPixels)
        exst += "green:" + str(self.greenPixels)
        exst += "blue:" + str(self.bluePixels)
        exst += "magenta:" + str(self.magentaPixels)
        exst += "yellow:" + str(self.yellowPixels)
        exst += "darkGreen:" + str(self.darkGreenPixels)
        exst += "darkBrown:" + str(self.darkBrownPixels)
        exst += "decision: " + self.decision
        return exst

