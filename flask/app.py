from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import config

app = Flask(__name__.split('.')[0])
app.config.from_mapping(config.CONFIG)
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

import resources, models

