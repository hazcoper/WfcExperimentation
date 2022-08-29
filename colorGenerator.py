"""
will grab one of the available color palette and return the given colors.

to add a new color palette, just add the link to the database
"""
import random

def HexToRgb(hexColor):
    """
    Receives a hex color in the normal format (string starting with #) and converts to rgb list
    """
    h = hexColor
    if "#" in h:
        h = h.lstrip("#")    
    
    rgbColor = list( int( h[i:i+2], 16 ) for i in (0,2,4) )
    rgbColor.reverse()
    return rgbColor

class ColorGenerator():

    def __init__(self):
        self.paletteList = []
        self.selectedPalette = None

        self.processDatabase()

    def setRandomPalette(self):
        self.selectedPalette = random.randint(0, len(self.paletteList)-1)

    def setPaletteIndex(self, index):
        if index >= len(self.paletteList):
            print(f"[ERROR] - index {index} does not exits")
            return
        self.selectedPalette = index
    
    def getRandomColor(self):
        if self.selectedPalette == None:
            print("[ERROR] - no palette has been selected")
            return
        return random.choice(self.paletteList[self.selectedPalette])

    def getPaletteIndex(self):
        return self.selectedPalette

    def processDatabase(self):
        """
        Will process and save all of the color palette available in the database
        """ 

        myFile = open("colordatabase.md", "r")
        lines = myFile.readlines()   # each line will be a link

        for line in lines:
            for part in line.split("/"):
                
                if len(part) > 16:
                    # this is the color palette

                    tempColor = ""
                    palette = []

                    for letter in part:
                        tempColor += letter
                        
                        if len(tempColor) ==  6:
                            print(" made a color: ", tempColor)
                            rgbColor = HexToRgb(tempColor)
                            palette.append( rgbColor )
                            tempColor = ""
            self.paletteList.append(palette)

            print("made this palette: ", palette)


