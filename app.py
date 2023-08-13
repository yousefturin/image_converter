import os
import time
import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, redirect, request, flash, jsonify
from werkzeug.utils import secure_filename
import aspose.words as aw


from utils.PathSystem import *





app = Flask(__name__, static_url_path='/static')

app.secret_key = "teqi-Eest1-iold4"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


class ResourceNotFoundError(Exception):
    pass

class InternalServerError(Exception):
    pass


@app.errorhandler(ResourceNotFoundError)
def handle_resource_not_found(e):
    return render_template('error.html', error=e), 404

@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    return render_template('error.html', error=e), 500

@app.route('/')
def home():
        try:
                return render_template('main.html')
        except:
                raise ResourceNotFoundError("Resource page not found")
        
# checking if the file are under the allowed format
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image',methods=['GET','POST'])
def upload_image():
    try:
        if request.method == 'POST':
            file = request.files['file']
            selected_format = request.form['selected_format']
            print(selected_format)
            try:
                filename = secure_filename(file.filename)
                app.logger.info(f'{filename}')
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                conver_image(selected_format,filename)
                time.sleep(3)
                # the processing is done, send a response indicating success
                response_data = {'success': True}
                return jsonify(response_data), 200
            except:
                raise ResourceNotFoundError("Image Resource could not be processed")                  
        else:
            raise ResourceNotFoundError("Image Resource could not be retuned")
    except:     
            return render_template('main.html')
    
def conver_image(selected_format,filename):
    ext_filename = os.path.splitext(filename)
    # getting the fist part of the folder name
    prefix = ext_filename[0]
    extention = ext_filename[1]
    # Add the new name and format to the image
    filename_pdf = prefix + selected_format
    original_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_path = os.path.join(CONVER_FOLDER, filename_pdf)
    print(pdf_path)

    if selected_format =='.pdf':
        print(filename)
        if extention =='.png':
            filename_pdf_jpg = prefix + '.jpg'
            pdf_jpg_path = os.path.join(CONVER_FOLDER, filename_pdf_jpg)
            print(pdf_jpg_path)
            img_to_jpg = Image.open(original_path)
            img_to_jpg.save(pdf_jpg_path)
            
        img_to_pdf = Image.open(pdf_jpg_path)
        img_to_pdf.save(pdf_path,resolution=100.0)

    if selected_format =='.svg':
        #  Create document object
        doc = aw.Document()
        # Create a document builder object
        builder = aw.DocumentBuilder(doc)
        # Load and insert PNG image
        shape = builder.insert_image(original_path)
        # Specify image save format as SVG
        saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)
        # Save image as SVG
        shape.get_shape_renderer().save(pdf_path, saveOptions)

    return


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5001)