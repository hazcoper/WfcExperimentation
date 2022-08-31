from wfc import WaveFunctionCollapse
from custom import Display
import numpy as np
import cv2

CONFIG = {
    "clean_edges": False,
    "overlapping": False,
    "color_divider": 1,
    "tiles": [
        {
            "filename": "./tiles/newSubway/vertical.png",
            "rotate90": True,
            "rotate180": False,
            "rotate270": False,
            "flip_vertical": False,
            "flip_horizontal": False,
        },
        {
            "filename": "./tiles/newSubway/leftToUp.png",
            "rotate90": True,
            "rotate180": True,
            "rotate270": True,
            "flip_vertical": False,
            "flip_horizontal": False,
        },
        {
            "filename": "./tiles/newSubway/blank.png",
            "rotate90": True,
            "rotate180": True,
            "rotate270": True,
            "flip_vertical": False,
            "flip_horizontal": False,
        },
    ]
}

OUTPUT_FILE = "subway.png"
TILESHEET_FILE = "subway-tilesheet.png"


def main():
    wfc = WaveFunctionCollapse(silent = False)
    wfc.load_config(CONFIG)
    wfc.create_tilesheet(TILESHEET_FILE)

def show(image, imageName=""):
    cv2.imshow(imageName, image)
    cv2.waitKey()
    cv2.destroyAllWindows()

def generateConnections():
    """
    Look at the tiles and establish the connections  between them
    """

    # each square has four sides
    # for each square
    #    for each side
    #       for each other square
    #          compare middle of side of square 1 to sqaure 2, if they have the same color then they match

    sideList = {"left": [49, 0], "top": [0, 49], "right": [49, 99], "bottom": [99, 49]}

    # need to be able to iterate over all of the tiles
    myDisplay = Display(100,100, 3,3, 10, 10)
    numberOfTile = myDisplay.xAmount * myDisplay.yAmount

    outputDict = {}

    for index in range(numberOfTile):
        print(f"This is the tile {index}")
        tile = myDisplay.indexGetPart(index)
        
        #check to see if image is black
        if index > 5:
            print("THIS TILE IS BLACKKKK")
            continue

        cv2.imshow("main", tile)
        connections = [[], [], [], []] # left top right bottom

        left1 = tile[sideList["left"][0],sideList["left"][1]]
        top1 = tile[sideList["top"][0],sideList["top"][1]]
        right1 = tile[sideList["right"][0],sideList["right"][1]]
        bottom1 = tile[sideList["bottom"][0],sideList["bottom"][1]]


        for index2 in range(numberOfTile):
            print(f"    Comparisson tile {index2} to tile {index}")
            tile2 = myDisplay.indexGetPart(index2)


            #check to see if image is black
            if index2 > 5:
                print("THIS TILE IS BLACKKKK")
                continue

            cv2.imshow("compare", tile2)


            left2 = tile2[sideList["left"][0],sideList["left"][1]]
            top2 = tile2[sideList["top"][0],sideList["top"][1]]
            right2 = tile2[sideList["right"][0],sideList["right"][1]]
            bottom2 = tile2[sideList["bottom"][0],sideList["bottom"][1]]

            print(left1, left2)
            print(top1, top2)
            print(right1, right2)
            print(bottom1, bottom2)

            # if any of the sides are equal, it connects
            if np.all(left1 == right2):
                # means that the left side connects
                connections[0].append(index2)
                print("      connects left")

            if np.all(top1 == bottom2):
                # means that the left side connects
                connections[1].append(index2)
                print("      connects top")

            if np.all(right1 == left2):
                # means that the left side connects
                connections[2].append(index2)
                print("      connects right")


            if np.all(bottom1 == top2):
                # means that the left side connects
                connections[3].append(index2)
                print("      connects bottom")

            cv2.waitKey()
            
        print("This is the connections ", connections)
        outputDict[index] = connections
    
    print(outputDict)
                



if __name__ == "__main__":
    main()
    generateConnections()
