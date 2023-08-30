import os
import time
import base64

import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, redirect, request, flash, jsonify, send_file
from werkzeug.utils import secure_filename
import aspose.words as aw


from utils.PathSystem import *


app = Flask(__name__, static_url_path="/static")

app.secret_key = "teqi-Eest1-iold4"

ALLOWED_EXTENSIONS = set(
    [
        ".png",
        ".jpeg",
        ".jpg",
        ".gif",
        ".tiff",
        ".pdf",
        ".heic",
        ".bmp",
        ".svg",
        ".ico",
    ]
)


class ResourceNotFoundError(Exception):
    pass


class InternalServerError(Exception):
    pass


@app.errorhandler(ResourceNotFoundError)
def handle_resource_not_found(e):
    return render_template("error.html", error=e), 404


@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    return render_template("error.html", error=e), 500


@app.route("/")
def home():
    try:
        return render_template("main.html")
    except:
        raise ResourceNotFoundError("Resource page not found")


# checking if the file are under the allowed format
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    try:
        if request.method == "POST":
            File = request.files["file"]
            SelectedFormat = request.form["selected_format"]
            print(SelectedFormat)
            try:
                Filename = secure_filename(File.filename)
                app.logger.info(f"{Filename}")
                File.save(os.path.join(UPLOAD_FOLDER, Filename))
                HandlerImage(SelectedFormat, Filename)
                time.sleep(3)
                # the processing is done, send a response indicating success
                ResponseData = {"success": True}
                return jsonify(ResponseData), 200
            except:
                raise ResourceNotFoundError("Image Resource could not be processed")
        else:
            raise ResourceNotFoundError("Image Resource could not be retuned")
    except:
        return render_template("main.html")
    
    
def ReRouterExtention(ProcessesExtention):
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
    if Extention.startswith("."):
        Extention = Extention[1:]  # Remove the leading dot if present
    UpperCaseExtention = Extention.upper()
    return UpperCaseExtention


def HandlerImage(SelectedFormat, Filename):
    PrefixExtentionSplit = os.path.splitext(Filename)
    # getting the fist part of the folder name
    Prefix = PrefixExtentionSplit[0]
    Extention = PrefixExtentionSplit[1]
    ProcessesSelectedFormat = ExtentionSplitForExternalLibraryConverter(SelectedFormat)
    print(ProcessesSelectedFormat)
    # Add the new name and format to the image
    FilenameImg = Prefix + SelectedFormat
    OriginalPath = os.path.join(UPLOAD_FOLDER, Filename)
    Path = os.path.join(CONVER_FOLDER, FilenameImg)
    # Works!
    if SelectedFormat == ".svg":
        if Extention == ".png" or ".jpg" or ".jpeg":
            ExternalLibraryConverter(OriginalPath, Path, ProcessesSelectedFormat)
        else:
            raise ResourceNotFoundError("Image Resource could not be retuned")
    # Not working idk wtf is going on with it it was working
    elif SelectedFormat == ".pdf":
        ExternalLibraryConverter(OriginalPath, Path, ProcessesSelectedFormat)
    # Works!
    elif SelectedFormat == ".png":
        ExternalLibraryConverter(OriginalPath, Path, ProcessesSelectedFormat)

    # Works!
    elif SelectedFormat == ".jpeg":
        # Specify image save format as GIF
        ExternalLibraryConverter(OriginalPath, Path, ProcessesSelectedFormat)

    elif SelectedFormat == ".jpg":
        raise InternalServerError(
            "The request can not be done at the moment please try again in a few moments"
        )
    # Works!
    elif SelectedFormat == ".gif":
        ExternalLibraryConverter(OriginalPath, Path, ProcessesSelectedFormat)
    # Works!
    elif SelectedFormat == ".tiff":
        ExternalLibraryConverter(OriginalPath, Path, ProcessesSelectedFormat)

    elif SelectedFormat == ".heic":
        raise InternalServerError(
            "The request can not be done at the moment please try again in a few moments"
        )
    # Works!
    elif SelectedFormat == ".bmp":
        ExternalLibraryConverter(OriginalPath, Path, ProcessesSelectedFormat)

    elif SelectedFormat == ".ico":
        raise InternalServerError(
            "The request can not be done at the moment please try again in a few moments"
        )
    else:
        raise ResourceNotFoundError(
            "Image Resource Format is incorrect to be Proccessed"
        )
    return


@app.route("/download_file", methods=["POST"])
def download_file():
    if request.method == "POST":
        try:
            _filename = request.json.get("image_name")
            if _filename:
                _filename = secure_filename(
                    _filename
                )  # Apply same filename sanitization
                file_path = os.path.join(CONVER_FOLDER, _filename)
                with open(file_path, "rb") as f:
                    data = f.read()
                data = base64.b64encode(data).decode("utf-8")
                return jsonify({"success": True, "data": data})
            else:
                return jsonify({"error": "Image name not provided"}), 400
        except:
            return jsonify({"error": "An error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
