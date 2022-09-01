"""
Simple script that will generate the images corresponding to the connecting tile

the connecting tile is made of two parts, the circle and the connector
we have the image of the circle and we have an image of a red connector

given a list of colors, I need to join those two with all the combinations to generate actual tiles

left to right red, up to down blue for example...


need to change this to also generete the other tiles needed ( the base tiles in all the available colors)

"""

import os
import cv2
import numpy as np


def overlay_transparent(bg_img, img_to_overlay_t):
    # Extract the alpha mask of the RGBA image, convert to RGB 
    b,g,r,a = cv2.split(img_to_overlay_t)
    overlay_color = cv2.merge((b,g,r))

    mask = cv2.medianBlur(a,5)

    # Black-out the area behind the logo in our original ROI
    img1_bg = cv2.bitwise_and(bg_img.copy(),bg_img.copy(),mask = cv2.bitwise_not(mask))

    # Mask out the logo from the logo image.
    img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)


    print("doing function")

    # Update the original image with our new ROI
    bg_img = cv2.add(img1_bg, img2_fg)
    return bg_img

def rotateImage(image, amount):
    """
    receives an image and an amount corresponding to the number of times to rotate it by 90 degress, 
    returns the rotated image
    rotates clockwise
    """
    output = image.copy()
    for x in range(amount):
        output = cv2.rotate( output, cv2.cv2.ROTATE_90_CLOCKWISE)


    return output

def changeColor(image, color, special=False):
    """
    Receives an image and a color, and changes the non black color of the image to the received color
    does not return anything
    """

    # find what is the non black color
    presentColor = (0, 0, 255, 255)
    if special:
        presentColor = (0, 16, 255, 255)   # need to fix the connector red tile to not have this problem

    output = image.copy()

    output[np.all(output == presentColor, axis=-1)] = color

    return output


def generateConnectors():
    """
    Generates all the connectors for the given color list
    """
    counter = 0
    # load the circle
    circle = cv2.imread(os.path.join(folder, "circle.png"), -1)

    # load the connector
    rawConnector = cv2.imread(os.path.join(folder, "connecting.png"), -1)

    # generate new image
    height = circle.shape[0]
    width = circle.shape[1]

    output = np.zeros((height,width,3), np.uint8)

    # add the circle
    output = overlay_transparent(output, circle)
    cv2.imshow("output", output)

    # the the four connectors

    # want to add the combinations of all of the colors
    for color1 in colorList:
        for color2 in colorList:
            
            # dont want to do it with my self
            if color1 == color2:
                print("comparing with my own")
                continue

            list1 = {0,1,2,3}
            setList = []

            for side1 in list1:
                for side2 in list1:
                    createSet = {side1, side2}
                    extraSet = list1.difference(createSet)
                    
                    if side1 == side2:
                        continue  # dont want to compare with my self
                    if createSet in setList:
                        continue  # dont want to repeat combinations

                    setList.append(createSet)


                    createList = list(createSet)
                    extraList = list(extraSet)

                    color1_raw = changeColor(rawConnector, color1, True)
                    color2_raw = changeColor(rawConnector, color2, True)

                    color1_1 = rotateImage(color1_raw, createList[0])
                    color1_2 = rotateImage(color1_raw, createList[1])
                    color2_1 = rotateImage(color2_raw, extraList[0])
                    color2_2 = rotateImage(color2_raw, extraList[1])
                    
                    output = overlay_transparent(output, color1_1)
                    output = overlay_transparent(output, color1_2)
                    output = overlay_transparent(output, color2_1)
                    output = overlay_transparent(output, color2_2)
                    
                    cv2.imwrite(f"{folder}/{counter}_connector.png", output)
                    # cv2.imshow("output", output)
                    # cv2.waitKey()
                    counter+= 1


def generateBaseTiles():
    """
    generate the base tiles in all the available colors
    """

    default1Name = "leftToUp.png"
    default2Name = "vertical.png"

    default1 = cv2.imread(os.path.join(folder, default1Name), -1)
    default2 = cv2.imread(os.path.join(folder, default2Name), -1)

    counter = 0
    for color in colorList:
        new1 = changeColor(default1, color)
        new2 = changeColor(default2, color)

        cv2.imwrite(os.path.join(folder, f"{counter}_{default1Name}"), new1 )
        cv2.imwrite(os.path.join(folder, f"{counter}_{default2Name}"), new2 )
        counter += 1
        

# cv2.waitKey()
folder = "tiles/complexSubway"
colorList = [[86, 50, 178], [125, 212, 252], [117, 170, 49], [68, 239, 162]]
colorList = [[255, 178, 61], [218, 237, 255], [48, 184, 255], [66, 36, 255]]

for color in colorList:
    color.append(255) #  add the alpha channel

generateBaseTiles()
generateConnectors()