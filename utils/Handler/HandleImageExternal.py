import os
import aspose.words as aw
from utils.PathSystem import *



def ReRouterExtention(ProcessesExtention):
    '''Take a file name Extention to be saved 
    in after processesd extention that is
    alloweded in a AW model'''
    if ProcessesExtention == 'SVG':
        AfterProcessesExtention = aw.SaveFormat.SVG
        
    if ProcessesExtention == 'TIFF':
        AfterProcessesExtention = aw.SaveFormat.TIFF
        
    if ProcessesExtention == 'BMP':
        AfterProcessesExtention = aw.SaveFormat.BMP
        
    if ProcessesExtention == 'JPEG':
        AfterProcessesExtention = aw.SaveFormat.JPEG
        
    if ProcessesExtention == 'GIF':
        AfterProcessesExtention = aw.SaveFormat.GIF
        
    if ProcessesExtention == 'PNG':
        AfterProcessesExtention = aw.SaveFormat.PNG
        
    return AfterProcessesExtention


def ExternalLibraryConverter(OriginalPath, Path, ProcessesExtention):
    
    #  Create document object
    Doc = aw.Document()
    # Create a document builder object
    Builder = aw.DocumentBuilder(Doc)
    # Load and insert PNG image
    Shape = Builder.insert_image(OriginalPath)
    # Specify image save format as SVG
    SaveFormat = ReRouterExtention(ProcessesExtention)
    SaveOptions = aw.saving.ImageSaveOptions(SaveFormat)
    # Save image as SVG
    Shape.get_shape_renderer().save(Path, SaveOptions)
    return


def ExtentionSplitForExternalLibraryConverter(Extention):
    '''Take a file name Extention to be Cleand up 
    from any special characters and returns a Extention name'''
    
    if Extention.startswith("."):
        Extention = Extention[1:]  # Remove the leading dot if present
    UpperCaseExtention = Extention.upper()

    return UpperCaseExtention



def GetImageExtentions(Filename):
    '''Take a file name and splits it
    not Prefix Extention to be returned'''

    PrefixExtentionSplit = os.path.splitext(Filename)
    # getting the fist part of the folder name
    Prefix = PrefixExtentionSplit[0]
    Extention = PrefixExtentionSplit[1]
    
    return Prefix, Extention

def AddNewNameAndFormatToImage(Filename, SelectedFormat, Prefix):
    '''Take a file name and a new Format and a Prefix of the file name to 
    be added as new format and the Prefix then to be joined into the folder 
    and retuens the Original Path of old image and the new Path of proccesesed image '''
    
    FilenameImg = Prefix + SelectedFormat
    OriginalPath = os.path.join(UPLOAD_FOLDER, Filename)
    Path = os.path.join(CONVER_FOLDER, FilenameImg)
    
    return OriginalPath, Path