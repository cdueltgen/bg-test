from flask import Flask

app = Flask(__name__)

# pull debug True/False from env


@app.route('/')
def index():
    return "HELLO!"

if __name__ == '__main__':
    app.run(debug=True)
