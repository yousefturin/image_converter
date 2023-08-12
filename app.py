import os
import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, redirect, request, flash
from werkzeug.utils import secure_filename


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
                return render_template('main.html',filename=filename)
            except:
                raise ResourceNotFoundError("Image Resource could not be processed")                  
        else:
            raise ResourceNotFoundError("Image Resource could not be retuned")
    except:     
            return render_template('main.html')
    
def conver_image(selected_format,filename):
    if selected_format == '.pdf':
        print(filename)
        original_path = os.path.join(UPLOAD_FOLDER, filename)
        print(original_path)
        pdf_path = os.path.join(CONVER_FOLDER, filename)
        img_to_pdf = Image.open(original_path)
        img_to_pdf.save(pdf_path, 'PDF', resolution=100.0, save_all=True)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5001)