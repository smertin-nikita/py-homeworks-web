from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import config
import resources

app = Flask(__name__)
app.config.from_mapping(config.CONFIG)
db = SQLAlchemy(app)

api = Api(app)

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
