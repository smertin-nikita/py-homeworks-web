from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import config

app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRES_URI)
db = SQLAlchemy(app)
migrate = Migrate(app, db)