from PIL import Image
import os
import numpy as np
import random as rnd
from matplotlib import cm
from matplotlib import pyplot as plt

#########################################################################################################
# Function defs
#########################################################################################################

def pprint(arr):
    for element in arr:
        print(element)

def initialPoints():
    pntOne =[]
    pntTwo = []

    for i in range(6):
        tmpVal  = rnd.randint(0,255)
        if i < 3:
            pntOne.append(tmpVal)
        else:
            pntTwo.append(tmpVal)
    return pntOne,pntTwo

def pntDistance(pOne, pTwo):
    tmpSum = 0

    for i in range(3):
        tmpSum += abs(pOne[i]-pTwo[i])

    distance = tmpSum/3

    return distance

def getImage(imName):
    DIR = os.getcwd()                           # get current directory
    img = Image.open(DIR + '\\' + imName)       # import image
    imgArr = np.asarray(img)                    # img -> array
    xPix,yPix = img.size                        # img dimensions
    totalPix = xPix*yPix                        # img size in pixels
    return img,imgArr,xPix,yPix,totalPix           

#########################################################################################################

#########################################################################################################

img,imgArr,xPix,yPix,totalPix = getImage('sunFlower.jpg')

# img.show()    #display image

kArr = {1,2,5,10,20}

p0 = []
p1 = []
avgP0,avgP1 = initialPoints()

while((p0 != avgP0) and (p1 != avgP1)):
    
    p0 = avgP0
    p1 = avgP1

    classArr = []
    numP0 = 0
    numP1 = 0

    for row in imgArr:
        classRow = []
        for pixel in row:
            if ( pntDistance(p0,pixel) <= pntDistance(p1,pixel) ):
                classRow.append([0])
                numP0 += 1
            else:
                classRow.append([1])
                numP1 += 1
        classArr.append(classRow)

    sumP0 = [0,0,0]
    sumP1 = [0,0,0]
    for i in range(yPix):

        for j in range(xPix):
        
            if classArr[i][j][0] == 0:
                sumP0[0] += int(imgArr[i][j][0])
                sumP0[1] += int(imgArr[i][j][1])
                sumP0[2] += int(imgArr[i][j][2])
                
            else:
                sumP1[0] += int(imgArr[i][j][0])
                sumP1[1] += int(imgArr[i][j][1])
                sumP1[2] += int(imgArr[i][j][2])
                
    avgP0 = [0,0,0]
    avgP1 = [0,0,0]

    avgP0[0] = sumP0[0]/numP0
    avgP0[1] = sumP0[1]/numP0
    avgP0[2] = sumP0[2]/numP0

    avgP1[0] = sumP1[0]/numP1
    avgP1[1] = sumP1[1]/numP1
    avgP1[2] = sumP1[2]/numP1

    print(avgP0,avgP1)



##########################################################################3
# saving to file
##########################################################################3

avgP0int = [0,0,0]
avgP1int = [0,0,0]

for i in range(3):
    avgP0int[i] = int(avgP0[i])
    avgP1int[i] = int(avgP1[i])

newImg = []
for i in range(yPix):
    tmpRow = []
    for j in range(xPix):
        
        if classArr[i][j][0] == 0:
            tmpRow.append(avgP0int)
        else:
            tmpRow.append(avgP1int)
    newImg.append(tmpRow)

plt.figure()
plt.imshow(newImg,cmap="gist_earth",interpolation='nearest')
plt.savefig('test.png')