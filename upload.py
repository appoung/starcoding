import os
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
...

# 파일 업로드

filename = ""


@app.route('/fileupload', methods=['POST'])
def file_upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('./uploads', filename))
    return 'Upload 성공'
