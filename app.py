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
UPLOAD_FOLDER ='C:/my_file/image_converter/static/uploads'

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
    if request.method == 'POST':
        file = request.files['file'] 

        if 'file' not in request.files:
            flash('No Image Part')
            return redirect(request.url)
        else:
            if file.filename == '':
                flash('No Selected Image')
                return redirect(request.url)
            if file.filename != '':
                if file and allowed_file(file.filename):
                    try:
                        filename = secure_filename(file.filename)
                        app.logger.info(f'{filename}')
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        return render_template('main.html',filename=filename)
                    except:
                        raise ResourceNotFoundError("Image Resource could not be processed")         
                elif file.filename not in ALLOWED_EXTENSIONS :
                    flash('Allowed image types are \n (png, jpg, jpeg, gif)')
                    return redirect(request.url)           
                else:
                    raise ResourceNotFoundError("Image Resource could not be retuned") 
            else:
                raise ResourceNotFoundError("Image Resource could not be retuned")  
    else:
            return render_template('main.html')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5001)