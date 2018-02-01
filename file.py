from flask import Flask, render_template, request
from werkzeug import secure_filename
app = Flask(__name__)

# @app.route('/upload')
# def upload_file():
#    return render_template('upload.html')


if __name__ == '__main__':
   app.run(debug = True)