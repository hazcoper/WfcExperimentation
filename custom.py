import random
import cv2
import numpy as np

from multiprocessing import Pool


class Display():

    def __init__ (self, tile_height, tile_width, xAmount, yAmount, sizeX, sizeY, filename="subway-tilesheet.png"):
        self.tile_height = tile_height
        self.tile_width = tile_width
        self.tileSet = cv2.imread(filename)
        self.xAmount, self.yAmount = xAmount, yAmount # in tile sheet, what are the dimensions, usually 3x3
        self.sizeX = sizeX
        self.sizeY = sizeY
        print(sizeX, sizeY)

    def indexShowPart(self, index):
        x = index % self.yAmount
        y = index // self.xAmount
        realX = x * self.tile_height + 1*(x+1)
        realY = y * self.tile_width + 1*(y+1)

        cv2.imshow("Image", self.tileSet[realY:realY + self.tile_height, realX:realX + self.tile_width])
        cv2.waitKey(0)
        
        pass
    
    def indexGetPart(self, index):
        x = index % self.yAmount
        y = index // self.xAmount
        realX = x * self.tile_height + 1*(x+1)
        realY = y * self.tile_width + 1*(y+1)   

        return self.tileSet[realY:realY + self.tile_height, realX:realX + self.tile_width]

    def posShowPart(self):
        pass

    def createOuput(self, matrix):
        output_shape = (self.tile_height * self.sizeX, self.tile_width * self.sizeY, 3)
        self.output = np.zeros(output_shape, np.uint8)

        for x in range(self.sizeX):
            for y in range(self.sizeY):
                tile = matrix[x][y]
                photoID = tile.imageID if  tile.isCollapsed == True else 6

                realY = y*self.tile_height
                realX = x*self.tile_height
                # print(realY*10, realX*10, realY*10+10, realX*10 +10)
                self.output[realX:realX+self.tile_height, realY:realY+self.tile_height] = self.indexGetPart(photoID)

                # cv2.imwrite("subway.png", self.output)
            
        # cv2.imwrite("subway.png", self.output)

    def save(self, filename):
        self.output[np.all(self.output == (0, 0, 255), axis=-1)] = (0,215,255)
        
        cv2.imwrite(filename, self.output)

    def viz(self):
        cv2.imshow("Image", self.output)
        cv2.waitKey(0)


class Image():
    
    def __init__(self):
        self.imageAmount = 7
        self.connections = {
            # Left, top, right, bottom
            # 0: [[0,5,6],[0,4,5,6],[0,2,3,6],[6]],
            # 1: [[1,3,4,6],[6],[1,2,5,6],[6]],
            # 2: [[1,3,4,6],[0,4,5,6],[6],[6]],
            # 3: [[6],[0,4,5,6],[1,2,5,6],[6]],
            # 4: [[6],[6],[1,2,5,6],[0,2,3,6]],
            # 5: [[1,3,4,6],[6],[6],[0,2,3,6]],
            # 6: [[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6]],
            
            # 0: [[6],[0,4,5,6],[6],[0,2,3,6]],
            # 1: [[1,3,4,6],[6],[1,2,5,6],[6]],
            # 2: [[1,3,4,6],[0,4,5,6],[6],[6]],
            # 3: [[6],[0,4,5,6],[1,2,5,6],[6]],
            # 4: [[6],[6],[1,2,5,6],[0,2,3,6]],
            # 5: [[1,3,4,6],[6],[6],[0,2,3,6]],
            # 6: [[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6]],

            # 0: [[6],[0,4,5],[6],[0,2,3]],
            # 1: [[1,3,4],[6],[1,2,5],[6]],
            # 2: [[1,3,4],[0,4,5],[6],[6]],
            # 3: [[6],[0,4,5,],[1,2,5,],[6]],
            # 4: [[6],[6],[1,2,5,],[0,2,3,]],
            # 5: [[1,3,4,],[6],[6],[0,2,3,]],
            # 6: [[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6],[0,1,2,3,4,5,6]],
        
            0: [[0,2,5],[0,4,5],[0,3],[0,2,3,4]],
            1: [[1,3,4],[1,2,3],[1,2,5],[1,3,4]],
            2: [[1,3,4],[0,4,5],[6],[6]],
            3: [[6],[0,4,5,],[1,2,5,],[6]],
            4: [[6],[6],[1,2,5,],[0,2,3,]],
            5: [[1,3,4,],[6],[6],[0,2,3,]],
            6: [[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,2,3,4,5]],
        

        }
    
    # returns a list with all the ids that connect to the given ID
    def getPossibleId(self, imageID, side):
        # 0 = Left
        # 1 = Top
        # 2 = Right
        # 3 = Bottom
        return self.connections[imageID][side]



class Tile():
    def __init__(self, x, y, tileCount, name, imageID = None):
        self.pos = [x,y]

        self.imageID = None if imageID == None else imageID   # the id that the tile has collapse to
        self.possibleList = [x for x in range(tileCount)] if imageID == None else []  # the possible ids that the tile can collapse to
        self.isCollapsed = False if imageID == None else True

        self.name = name

    # receives an id and collapses to the given id
    def collapse(self, photoId):
        
        if photoId not in self.possibleList:
            print(f"tile {self.name} cant collapse to {photoId} ({possibleId})")

        self.possibleList = []
        self.imageID = photoId
        self.isCollapsed = True

    def getPossibleList(self):
        return self.possibleList
    
    # receives a possibleList and replaces the current possibleList
    def updatePossibleList(self, possibleList):
        self.possibleList = possibleList

        return

    # used when there is no other tile to collapse, will choose a random photoID from the possible list
    # there are no tiles to collapse, so I will prepare this one to collapse
    # but will not collapse it because its the loop that will collapse the tile
    def prepareRandomCollapse(self):
        self.possibleList = [random.choice(self.possibleList)]

    def __gt__(self, other):
        amount1 = len(self.possibleList) if not self.isCollapsed else 0 
        amount2 = len(other.possibleList) if not other.isCollapsed  else 0  

        return amount1 > amount2

    def __lt__(self, other):
        amount1 = len(self.possibleList) if not self.isCollapsed else 0 
        amount2 = len(other.possibleList) if not other.isCollapsed  else 0  

        return amount1 < amount2

    def __eq__(self, other):
        amount1 = len(self.possibleList) if not self.isCollapsed else 0 
        amount2 = len(other.possibleList) if not other.isCollapsed  else 0  

        return amount1 == amount2
    def __repr__(self):
        # return str(len(self.idx))
        return str(self.name)



class Wfc():

    def __init__(self, sizex, sizey, tileQuant, name, counter):
        global tileMatrix
        self.SIZEX, self.SIZEY = sizex, sizey
        self.tileQuant = tileQuant
        # generate all of tiles
        tileMatrix = [[Tile(x, y, tileQuant, x * sizex + y) for y in range(self.SIZEY)] for x in range(self.SIZEX)]
        self.toCollapse = [] # list of tiles that are ready to be collapse
        self.uncollapsedList = [] # list with all the tiles that are yet to be collapsed

        self.doLoop = True
        self.collapseCounter = 0

        self.name = name
        self.counter = counter

        for line in tileMatrix:
            for tile in line:
                self.uncollapsedList.append(tile)

        self.Image = Image()


        self.loop()


    def loop(self):
        # collapse all the tiles in self.toCollapse
        # if its empty collapse random tile
        while self.doLoop:
            for tile in self.toCollapse:  # this is the list of tiles that are ready to be collapsed (have only one option for photoID)
                print(f"Collapsing {tile}")
                value = self.collapseTile(tile)
                if value == -1:
                    return
                self.printTileMatrix()
            # self.randomCollapse()
            self.minCollapse()

    # choose a random tile that has not been collapsed and force it to collapse
    def randomCollapse(self):
        choosenTile = random.choice(self.uncollapsedList)
        choosenTile.prepareRandomCollapse()

        self.toCollapse.append(choosenTile)

    # will collapse the tile with the minimum amount of entropy
    def minCollapse(self):
        self.uncollapsedList.sort()
        print("UncollapsedList")
        for tile in self.uncollapsedList:
            print("    ", tile, len(tile.getPossibleList()))
        choosenTile = self.uncollapsedList[0]

        choosenTile.prepareRandomCollapse()
        self.toCollapse.append(choosenTile)



    


    # will receive a Tile, and collapse if it is ready to be collapsed
    # update the imageID, and update the neighbors
    def collapseTile(self, tile):
        if tile.isCollapsed == True:
            return
        
        if len(tile.getPossibleList()) != 1:
            return

        # has passed all the tests and is ready to be collapsed
        tile.collapse(tile.getPossibleList()[0])
        
        self.toCollapse.remove(tile)
        self.uncollapsedList.remove(tile)

        # update the neighbors
        for nTile in self.getNeighbourTileList(tile):
            if nTile[0].isCollapsed:
                #ignore tiles that have already been collapse
                continue
            self.updateTile(nTile[0], tile.imageID, nTile[1])
        
        self.collapseCounter += 1
        if self.collapseCounter == self.SIZEX*self.SIZEY:
            return -1

        

    # receives a tile and the imageID that was attributed to one of its neighbour
    # will update the imageID of the received tile to account for the change
    def updateTile(self, tile, imageID, side):
        tile.updatePossibleList(self.Image.getPossibleId(imageID, side)) 
        if len(tile.getPossibleList()) == 1:
            # means that it is ready to be collapsed, lets add to the list
            self.toCollapse.append(tile)



    def printTileMatrix(self):
        global tileMatrix

        for line in tileMatrix:
            for tile in line:
                if tile.isCollapsed:
                    print(tile.imageID, end=" ")
                else:
                    print(f"{len(tile.getPossibleList())}.", end=" ")
            print()
    

    # given the name of the tile, it will reuturn the given tile
    def indexGetTile(self, tileName):
        global tileMatrix

        for line in tileMatrix:
            for tile in line:
                if tileName == tile.name:
                    return tile

        return None

    # given a position, return the given tile
    def posGetTile(self, pos):
        global tileMatrix
        return tileMatrix[pos[0]][pos[1]]

    # Receives a tile and returns a list with all the valid neighbouring tiles
    def getNeighbourTileList(self, myTile):
        global tileMatrix
        posList = self.getVerticalNeighbour(myTile) + self.getHorizontalNeighbour(myTile) 
        tileList = [[tileMatrix[pos[0]][pos[1]], pos[2]] for pos in posList]
        return tileList

    # Recevies a tile and returns a list with the postion of the valid Horizontal neighbors
    def getHorizontalNeighbour(self, myTile):
        neighbors = []
        if myTile.pos[0] > 0:
            neighbors.append([myTile.pos[0]-1, myTile.pos[1], 1])
        if myTile.pos[0] < self.SIZEX-1:
            neighbors.append([myTile.pos[0]+1, myTile.pos[1], 3])

        return neighbors

    # Recevies a tile and returns a list with the postion of the valid Horizontal neighbors
    def getVerticalNeighbour(self, myTile):
        neighbors = []
        if myTile.pos[1] > 0:
            neighbors.append([myTile.pos[0], myTile.pos[1]-1, 0])
        if myTile.pos[1] < self.SIZEX-1 :
            neighbors.append([myTile.pos[0], myTile.pos[1]+1, 2])
        return neighbors


def run(name):
    global tileMatrix
    SIZEX = 6 # size in tiles of the final imgae
    SIZEY = 6 # size in tiles of the final image
    tileQuant = 7
    myDisplay = Display(100,100, 3,3, SIZEX, SIZEY)
    
    tileMatrix = None

    this = False 
    counter = 0 
    while this == False:
        
        
        try:
            myWfc = Wfc(SIZEX, SIZEY, tileQuant, name, counter)
            this = True
        except:
            print(" Trying again ...")

            # want to save what it generated
            myDisplay.createOuput(tileMatrix)
            myDisplay.save(f"output/{name}{counter}.png")

            counter += 1    
        
    
    myDisplay.createOuput(tileMatrix)
    # myDisplay.viz()
    
    myDisplay.save(f"output/final/{name}.png")

if __name__ == '__main__':

    name = "hello"

    # run(name)

    threadNum = 500
    pool = Pool(threadNum)
    pool.map(run, list(range(threadNum)))
    pool.close()
        
    # generate all the tiles, that can have whatever id





# def testNeighbors():
#     # generate a 50x50 board with 10 options and check the returned neighbors
#     myWfc = Wfc(50, 50, 10)
    
#     tile1 = myWfc.indexGetTile(0)  #top left 
#     tile1 = myWfc.indexGetTile(49) #top right
#     tile1 = myWfc.posGetTile([49][0])  #bottom left
#     tile1 = myWfc.posGetTile([49][49])  #bottom right
#     tile1 = myWfc.posGetTile([0][30])  #top border
#     tile1 = myWfc.posGetTile([0][0])  #bottom border
#     tile1 = myWfc.posGetTile([49][0])  #left border
#     tile1 = myWfc.posGetTile([49][0])  #right border
#     tile1 = myWfc.posGetTile([49][0])  #random
#     tile1 = myWfc.posGetTile([49][0])  #random


#     myWfc.getNeighbourList()
