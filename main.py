#!/usr/bin/python3

from PIL import Image
import os
import numpy as np
import random as rnd
from matplotlib import cm
from matplotlib import pyplot as plt
import argparse
from os import path

#########################################################################################################
# Argument Parsing
#########################################################################################################
def parse_args():
    parser = argparse.ArgumentParser()

    #required args
    parser.add_argument('input_path', metavar='I',\
                        help='the path to the original image to perform k-means seperation on')
    parser.add_argument('n_pts', metavar='K', type=int, nargs='+',\
                        help='a list of numbers of means to use; for each k, one output will'\
                            +' be generated')

    #optional args
    parser.add_argument('--output', '-o', default='{0}-with-{1}-means',\
                        help='the format for the names of the output files, in python syntax;'\
                            +' {0} will be sustituted for the name of the input file and'\
                            +' {1} will be substituted for the the value of k used')

    return parser.parse_args()

#########################################################################################################
# Function defs
#########################################################################################################

def pprint(arr):
    for element in arr:
        print(element)

def initialPoints(k):
    pnts = []

    for i in range(k):
        tmpPnt = []
        for j in range(3):
            tmpVal  = rnd.randint(0,255)
            tmpPnt.append(tmpVal)
        pnts.append(tmpPnt)

    return pnts

def pntDistance(pOne, pTwo):
    tmpSum = 0

    for i in range(3):
        tmpSum += abs(pOne[i]-pTwo[i])

    distance = tmpSum/3

    return distance

def getImage(imName):
    img = Image.open(imName)                    # import image
    imgArr = np.asarray(img)                    # img -> array
    xPix,yPix = img.size                        # img dimensions
    totalPix = xPix*yPix                        # img size in pixels
    return img,imgArr,xPix,yPix,totalPix           

#########################################################################################################

#########################################################################################################

args = parse_args()

input_path = args.input_path
output_format = args.output

#seperate out the directory and file names of the input file
input_name, img_extension = os.path.basename(input_path).split('.')[:2]
img_dir = os.path.dirname(input_path)

img,imgArr,xPix,yPix,totalPix = getImage(input_path)

for K in args.n_pts:
    points = []

    for i in range(K):
        points.append([])

    avgs = initialPoints(K)

    while(points != avgs):
        classCnts = []
        sums = []
        distances = []

        for i in range(K):
            points[i] = avgs[i]
            classCnts.append(0)
            sums.append([0,0,0])
            distances.append(0)

        classArr = []
        
        for row in imgArr:
            classRow = []
            for pixel in row:
                for i in range(K):
                    distances[i] = pntDistance(points[i],pixel)     # find distance from pixel to each point
               
                mDist = min(distances)                              # find closest point
                mDistIdx = distances.index(mDist)                   # get index of that point
                classRow.append(mDistIdx)                           # store index of closest point
                classCnts[mDistIdx] += 1                            # increase counts

            classArr.append(classRow)
        print("CLASS COUNTS: ",end = "")
        print(classCnts)
        # pprint(classArr)
        
        for i in range(yPix):

            for j in range(xPix):
            
                val = classArr[i][j]
                sums[val][0] += int(imgArr[i][j][0])
                sums[val][1] += int(imgArr[i][j][1])
                sums[val][2] += int(imgArr[i][j][2])
        
        print("SUMS: ",end="")
        print(sums)

        for i in range(K):
            try:
                avgs[i][0] = int(sums[i][0]/classCnts[i])
                avgs[i][1] = int(sums[i][1]/classCnts[i])
                avgs[i][2] = int(sums[i][2]/classCnts[i])
            except:
                avgs[i] = [0,0,0]

        print("AVERAGES: ",end="")
        print(avgs)


    ##########################################################################3
    # saving to file
    ##########################################################################3

    newImg = []
    for i in range(yPix):
        tmpRow = []
        for j in range(xPix):
            tmpRow.append(avgs[classArr[i][j]])
          
        newImg.append(tmpRow)

    plt.figure()
    plt.imshow(newImg,cmap="gist_earth",interpolation='nearest')
    
    #the name of the output file is given by the output format defined by the user,
    #and has the same extension as the input file
    output_img = '{}.{}'.format(output_format.format(input_name, K), img_extension)

    #the output file should be saved in the same directory as the input file
    plt.savefig(os.path.join(img_dir, output_img))
