from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')
app.secret_key = "teqi-Eest1-iold4"

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




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5001)