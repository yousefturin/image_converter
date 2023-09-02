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
from utils.HandleImageExternal import *
from utils.ValidationExtention import *


app = Flask(__name__, static_url_path="/static")

app.secret_key = "teqi-Eest1-iold4"


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


@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    
    try:
        if request.method == "POST":
            File = request.files["file"]
            SelectedFormat = request.form["selected_format"]
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
    
    



def SendImageForRequestFormatCheck(SelectedFormat,Extention, OriginalPath,Path,ProcessesSelectedFormat):
    '''Take a selected format and the extention and old path of teh joined image and the new path
    of the proccessed and takes the cleaned up format of the new image then checkes the 
    selected format to be then convered base on it and the old format of the image'''
    
    
    
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



def HandlerImage(SelectedFormat, Filename):
    
    # Getting the fist part of the folder name.
    Prefix, Extention  =  GetImageExtentions(Filename)
    # Remove the # Remove the leading dot if present in SelectedFormat.
    ProcessesSelectedFormat = ExtentionSplitForExternalLibraryConverter(SelectedFormat)
    # Add the new name and format to the image.
    OriginalPath, Path = AddNewNameAndFormatToImage(Filename, SelectedFormat,Prefix)
    # Send the SelectedFormat and Extention and the OriginalPath, Path and the SelectedFormat
    # after cleaning to be proccesed base on the SelectedFormat.
    SendImageForRequestFormatCheck(SelectedFormat, Extention, OriginalPath, Path, ProcessesSelectedFormat)
    
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
