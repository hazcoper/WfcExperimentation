"""
Simple script that will generate the images corresponding to the connecting tile

the connecting tile is made of two parts, the circle and the connector
we have the image of the circle and we have an image of a red connector

given a list of colors, I need to join those two with all the combinations to generate actual tiles

left to right red, up to down blue for example...
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

    for x in range(amount):
        output = cv2.rotate( image, cv2.cv2.ROTATE_90_CLOCKWISE)


    return output

def changeColor(image, color):
    """
    Receives an image and a color, and changes the non black color of the image to the received color
    does not return anything
    """

    # find what is the non black color
    presentColor = (0, 0, 255, 255)
    image[np.all(image == presentColor, axis=-1)] = color



testImage = cv2.imread("tiles/complexSubway/connecting.png")


# cv2.imshow("0", testImage)
# testImage = rotateImage(testImage, 1)
# cv2.imshow("1", testImage)
# testImage = rotateImage(testImage, 1)
# cv2.imshow("2", testImage)
# testImage = rotateImage(testImage, 1)
# cv2.imshow("3", testImage)

cv2.imshow("before", testImage)
changeColor(testImage, [20,100,30])
cv2.imshow("after", testImage)

cv2.waitKey()
# folder = "tiles/complexSubway"

# colorList = [[86, 50, 178], [125, 212, 252], [117, 170, 49], [68, 239, 162]]

# # load the circle
# circle = cv2.imread(os.path.join(folder, "circle.png"), -1)

# # load the connector
# rawConnector = cv2.imread(os.path.join(folder, "connecting.png"), -1)

# # generate new image
# height = circle.shape[0]
# width = circle.shape[1]

# output = np.zeros((height,width,3), np.uint8)

# # add the circle
# output = overlay_transparent(output, circle)
# cv2.imshow("output", output)

# # the the four connectors

# # want to add the combinations of all of the colors
# for color1 in colorList:
#     for color2 in colorList:
        
#         # dont want to do it with my self
#         if color1 == color2:
#             print("comparing with my own")
#             continue

        



# output = overlay_transparent(output, rawConnector)

# cv2.imshow("output", output)
# cv2.waitKey()
