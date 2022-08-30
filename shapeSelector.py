import cv2
import numpy as np
import random
from matplotlib import pyplot as plt

from colorGenerator import ColorGenerator

import os

"""
Script that will indentify the shapes and randomize their color
"""
IS_RANDOM = False # choose palette coloring vs random
cg = ColorGenerator()


def random_color():
    global cg

    if IS_RANDOM:
        rgbl = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
        return tuple(rgbl)

    return cg.getRandomColor()

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


name = "hello.png"

nameLis  = [f for f in os.listdir("output/final") if os.path.isfile(os.path.join("output/final", f))]
# nameLis = ["0.png"]
for name in nameLis:
    try:
        cg.setRandomPalette()
        
        # load the image
        path = os.path.join("output/final", name)
        image = cv2.imread(path)
        h, w, _ = image.shape

        # create bigger Image
        height = h + 2
        width = w + 2
        big_image = np.zeros((height,width,3), np.uint8)

        # place the original image in the middle


        # load background image as grayscale
        hh, ww, _ = big_image.shape

        # compute xoff and yoff for placement of upper left corner of resized image   
        yoff = round((hh-h)/2)
        xoff = round((ww-w)/2)

        # use numpy indexing to place the resized image in the center of background image
        big_image[yoff:yoff+h, xoff:xoff+w] = image


        #convert it to grayscale, and blur it slightly

        gray = cv2.cvtColor(big_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)



        # apply Canny edge detection using a wide threshold, tight
        # threshold, and automatically determined threshold
        wide = cv2.Canny(blurred, 10, 200)
        tight = cv2.Canny(blurred, 225, 250)
        auto = auto_canny(blurred)

        # cv2.imshow("auto", auto)
        # cv2.imshow("wide", wide)
        # cv2.imshow("tight", tight)
        # cv2.waitKey()

        # Finding Contours
        # Use a copy of the image e.g. edged.copy()
        # since findContours alters the image
        contours, hierarchy = cv2.findContours(auto, 
            cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        

                
        
        # Draw all contours
        # -1 signifies drawing all contours
        # cv2.drawContours(image, contours, -1, (0, 255, 0), -1)

        height = h + 2
        width = w + 2
        blank_image = np.zeros((height,width,3), np.uint8)


        # maybe i can just draw this in order from the biggest to the smallest, ignoring the extra ones

        myList = [[x, cv2.contourArea(contours[x])] for x in range(len(contours))]
        myList = (sorted(myList, key=lambda x:x[1], reverse=True))

        for index in myList:
            counter = index[0]
            h = hierarchy[0][counter]
            

            # dont want to draw contours with hierarchy (-1 -1 -1 x)
            if h[0] == h[1] and h[1] == h[2] and h[2] == -1:
                continue
          
            # check to see if the place where I am placing the shape is black or not
            # if its not black, it means that it is the inside of another shape so I want to use the black color
            if np.any(blank_image[contours[counter][0][0][1], contours[counter][0][0][0]] != 0):
                cv2.fillPoly(blank_image, pts = [contours[counter]], color=(0,0,0))
                continue

            cv2.fillPoly(blank_image, pts = [contours[counter]], color=random_color())
            # cv2.imshow(" ", blank_image)
            # cv2.waitKey()

            # print()
 
        cv2.imwrite(f"output/final/colored/{name}-{cg.getPaletteIndex()}",blank_image)
    except Exception as e:
        print(f"{name} - problem {e}")
