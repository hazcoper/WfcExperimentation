import imageio
import os

import re
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)



sourceFolder = "output"
filenames = [os.path.join(sourceFolder, f) for f in os.listdir(sourceFolder)]
filenames = sorted_alphanumeric(filenames)

images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave(os.path.join(sourceFolder, "movie.gif"), images)