import os

import boto3
from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from rq import Queue
from worker import conn

from utils import upload_queue, make_pdf

DEBUG = "NO_DEBUG" not in os.environ
S3_BUCKET = os.environ.get('S3_BUCKET')
PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)


@app.route('/')
def index():
    """Landing page."""
    return render_template("hello.html")


@app.route('/upload', methods=["GET", "POST"])
def upload_file():
    """Read the file and put upload in worker queue."""
    if request.method == "POST":
        filename = make_pdf()
        file_contents = open(filename, 'rb').read()
        q = Queue(connection=conn)
        q.enqueue(upload_queue, filename, file_contents)
        return render_template('success.html', filename=filename)
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
