from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__.split('.')[0])
app.config.from_mapping(config.CONFIG)
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)


@app.route('/')
def index():
    return 'Hello'

