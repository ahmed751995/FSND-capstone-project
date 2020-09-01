import os
from flask import Flask
from flask_cors import CORS
from .database.models import setup_db, Actor, Movie, Show

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/')
def index():
    return "hi man"

if __name__ == '__main__':
    app.run(debug=True)
