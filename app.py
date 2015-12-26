import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

# pull debug True/False from env?
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('success.html', filename=filename)
    else:
        return render_template('failure.html')

if __name__ == '__main__':
    app.run(debug=True)
