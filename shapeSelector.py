import cv2
import numpy as np
import random

import os

"""
Script that will indentify the shapes and randomize their color
"""

def random_color():

    rgbl = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
    return tuple(rgbl)


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
for name in nameLis:
    try:
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


        # Finding Contours
        # Use a copy of the image e.g. edged.copy()
        # since findContours alters the image
        contours, hierarchy = cv2.findContours(auto, 
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                
        
        # Draw all contours
        # -1 signifies drawing all contours
        # cv2.drawContours(image, contours, -1, (0, 255, 0), -1)

        height = h + 2
        width = w + 2
        blank_image = np.zeros((height,width,3), np.uint8)
        # cv2.drawContours(blank_image, contours[0], -1, color=(255, 255, 255), thickness=cv2.FILLED)


        for contour in contours:
            cv2.fillPoly(blank_image, pts = [contour], color=random_color())

            cv2.imshow(" ", blank_image)
            cv2.waitKey()

        cv2.imwrite(f"output/final/colored/{name}",blank_image)
    except Exception as e:
        print(f"{name} - problem {e}")
