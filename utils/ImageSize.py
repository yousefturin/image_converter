import os
from PIL import Image



def GetImageSize(OriginalPath):
    '''Take an image from its path and 
    returns the width and size of that image'''
    with Image.open(OriginalPath) as img:
        ImageWidth, ImageHeight = img.size
    return ImageWidth, ImageHeight