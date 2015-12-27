import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import boto3

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
DEBUG = "NO_DEBUG" not in os.environ
# AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
# AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET')

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return "HELLO!"


@app.route('/upload_form')
def get_upload():
    return render_template("upload_form.html")


@app.route('/upload', methods=["POST"])
def upload_file():
    f = request.files['file']
    file_contents = f.read()
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        s3_bucket = os.environ.get('S3_BUCKET')
        s3 = boto3.resource('s3')
        s3.Bucket(s3_bucket).put_object(Key=filename, Body=file_contents)
        # This was for testing locally
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('success.html', filename=filename)
    else:
        return render_template('failure.html')


@app.route('/bucketlist')
def list_bucket():
    s3_bucket = os.environ.get('S3_BUCKET')
    s3 = boto3.resource('s3')
    objects = s3.Bucket(s3_bucket).objects.all()
    return render_template('bucketlist.html', objects=objects)


if __name__ == '__main__':
    app.run(debug=DEBUG)
