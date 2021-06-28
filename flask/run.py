from flask_restful import Api

import resources
from app import app


if __name__ == '__main__':
    api = Api(app)

    api.add_resource(resources.UserRegistration, '/users')
    api.add_resource(resources.UserLogin, '/login')
    api.add_resource(resources.UserLogoutAccess, '/logout/access')
    api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(resources.TokenRefresh, '/token/refresh')
    api.add_resource(resources.SecretResource, '/secret')

    app.run()
