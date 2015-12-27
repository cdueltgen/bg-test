import os
from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
import boto3
from rq import Queue
from worker import conn
from utils import upload_queue

# UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
DEBUG = "NO_DEBUG" not in os.environ
S3_BUCKET = os.environ.get('S3_BUCKET')
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def upload_queue(filename, file_contents):
#     s3 = boto3.resource('s3')
#     s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=file_contents)
#     return


@app.route('/')
def index():
    return render_template("hello.html")


@app.route('/upload_form')
def get_upload():
    return render_template("upload_form.html")


@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files['file']
        file_contents = f.read()
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            q = Queue(connection=conn)
            q.enqueue(upload_queue, filename, file_contents)
            # upload_queue(filename, file_contents)
            # s3 = boto3.resource('s3')
            # s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=file_contents)
            # This was for testing locally
            # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('success.html', filename=filename)
        else:
            return render_template('failure.html')
    else:
        return redirect('/bucketlist')


@app.route('/bucketlist')
def list_bucket():
    s3 = boto3.resource('s3')
    objects = s3.Bucket(S3_BUCKET).objects.all()
    return render_template('bucketlist.html', objects=objects)


if __name__ == '__main__':
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
