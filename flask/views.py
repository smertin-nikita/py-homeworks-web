from flask import request, jsonify
from flask.views import MethodView

from app import app
from validator import validate
from models import User, Advertisement
from schema import USER_CREATE, ADVERTISEMENT_CREATE


class UserView(MethodView):

    def get(self, user_id):
        user = User.get_by_id(user_id)
        return jsonify(user.to_dict())

    @validate('json', USER_CREATE)
    def post(self):
        user = User(**request.json)
        user.set_password(request.json['password'])
        user.add()
        return jsonify(user.to_dict())

    def delete(self, user_id):
        User.delete_by_id(user_id)
        return jsonify({'message': 'NO_CONTENT'})


class AdvertisementView(MethodView):

    def get(self, advertisement_id):
        instance = Advertisement.get_by_id(advertisement_id)
        return jsonify(instance.to_dict())

    @validate('json', ADVERTISEMENT_CREATE)
    def post(self):
        instance = Advertisement(**request.json)
        instance.add()
        return jsonify(instance.to_dict())

    def delete(self, advertisement_id):
        Advertisement.delete_by_id(advertisement_id)
        return jsonify({'message': 'NO_CONTENT'})


app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_get'), methods=['GET', ])
app.add_url_rule('/users/', view_func=UserView.as_view('users_create'), methods=['POST', ])
app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_delete'), methods=['DELETE', ])
app.add_url_rule('/advertisements/<int:advertisement_id>', view_func=AdvertisementView.as_view('advertisements_get'), methods=['GET', ])
app.add_url_rule('/advertisements/', view_func=AdvertisementView.as_view('advertisements_create'), methods=['POST', ])
app.add_url_rule('/advertisements/<int:advertisement_id>', view_func=AdvertisementView.as_view('advertisements_delete'), methods=['DELETE', ])
