# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
from detect import image_prepare, detect
from waitress import serve

# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/yolov1', methods=['GET'])
def yolov1():
    return render_template('yolov1.html')


@app.route('/yolov2', methods=['GET'])
def yolov2():
    return render_template('yolov2.html')


@app.route('/yolov3', methods=['GET'])
def yolov3():
    return render_template('yolov3.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、jpg、jpeg、bmp"})

        basepath = os.path.dirname(__file__)

        upload_path = os.path.join(basepath, 'static\\\\images', secure_filename(f.filename))

        f.save(upload_path)

        input_imgs = image_prepare(upload_path)

        infer_time = detect(input_imgs, upload_path, f.filename)

        return render_template('detect_complete.html', userinput=str(infer_time), filename=f.filename)

    return render_template('upload.html')


if __name__ == '__main__':
    # Running Local
    app.run(host='0.0.0.0', port=5000, debug=True)
    # Running remote
    # serve(app)
