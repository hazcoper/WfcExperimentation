"""
Resizes all of the images in a given directory.
used to convert the gif to video
    there where problems becuase I had images of different sizes
"""
import os
import cv2
import numpy as np

import re
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)



imageList = [os.path.join("film", x) for x in os.listdir("film") if x.split(".")[-1] == "png" and int(x.split("_")[0]) < 100]
imageList = sorted_alphanumeric(imageList)


for imagePath in imageList:

    image = cv2.imread(imagePath)

    h, w, _ = image.shape

    # create bigger Image
    height = h + 2
    width = w + 2
    big_image = np.zeros((height,width,3), np.uint8)

    # load background image as grayscale
    hh, ww, _ = big_image.shape

    # compute xoff and yoff for placement of upper left corner of resized image   
    yoff = round((hh-h)/2)
    xoff = round((ww-w)/2)

    # place the original image in the middle
    # use numpy indexing to place the resized image in the center of background image
    big_image[yoff:yoff+h, xoff:xoff+w] = image

    cv2.imwrite(imagePath, big_image)

print( imageList)