from PIL import Image

from utils.ImageSize import GetImageSize

def ConvertPNGToICO(OriginalPath, Path, ProcessesSelectedFormat):
    '''Take an image from its path and 
    the new path to be saved in as ICO'''
    # Get the original image dimensions
    ImageWidth, ImageHeight = GetImageSize(OriginalPath)
    img = Image.open(OriginalPath)
    # Convert the image to an ICO file with the same size
    img.save(Path, format=ProcessesSelectedFormat, sizes=[(ImageWidth, ImageHeight)])