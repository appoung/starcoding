import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Make sure the upload folder exists
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 1. 기본 경로에 대한 라우트


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')


@app.route('/project')
def project():
    return 'The project page'


@app.route('/omgwtf')
def omgwtf():
    return "스타코딩의 짱은 한병준이다"


@app.route('/fileupload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'Upload 성공'
    return render_template('fileupload.html')


if __name__ == '__main__':
    app.run(debug=True)
