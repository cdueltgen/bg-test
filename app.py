import os

import boto3
from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from rq import Queue
from worker import conn

from utils import upload_queue

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
DEBUG = "NO_DEBUG" not in os.environ
S3_BUCKET = os.environ.get('S3_BUCKET')
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)


def allowed_file(filename):
    """Determine if the uploaded file is an uploadable type."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Moved to utils.py
# def upload_queue(filename, file_contents):
#     s3 = boto3.resource('s3')
#     s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=file_contents)
#     return


@app.route('/')
def index():
    """Landing page."""
    return render_template("hello.html")


@app.route('/upload_form')
def get_upload():
    """Render the upload form."""
    return render_template("upload_form.html")


@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    """Read the file and put upload in worker queue."""
    if request.method == "POST":
        f = request.files['file']
        file_contents = f.read()
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            q = Queue(connection=conn)
            q.enqueue(upload_queue, filename, file_contents)
            # moved to utils.py
            # s3 = boto3.resource('s3')
            # s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=file_contents)
            return render_template('success.html', filename=filename)
        else:
            return render_template('failure.html')
    else:
        return redirect('/bucketlist')


@app.route('/bucketlist')
def list_bucket():
    """Ask s3 for a list of things in the bucket."""
    s3 = boto3.resource('s3')
    objects = s3.Bucket(S3_BUCKET).objects.all()
    return render_template('bucketlist.html', objects=objects)


if __name__ == '__main__':
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
