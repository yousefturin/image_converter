from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from utils.ImageSize import GetImageSize


def ConvertPNGToPDF(OriginalPath, Path):
    '''Take an image from its path and 
    the new path to be saved in as PDF'''
    ImageWidth, ImageHeight = GetImageSize(OriginalPath)
    c = canvas.Canvas(Path, pagesize=letter)
    c.drawImage(OriginalPath, 0, 0, width=ImageWidth, height=ImageHeight)
    c.showPage()
    c.save()
    return