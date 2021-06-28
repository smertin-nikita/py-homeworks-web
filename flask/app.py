from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import config

app = Flask(__name__)
app.config.from_mapping(config.CONFIG)
db = SQLAlchemy(app)


