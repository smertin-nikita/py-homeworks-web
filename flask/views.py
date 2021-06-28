from flask import request, jsonify
from flask.views import MethodView

from app import app
from validator import validate
from models import UserModel, AdvertisementModel
from schema import USER_CREATE, ADVERTISEMENT_CREATE


class UserView(MethodView):

    def get(self, user_id):
        user = UserModel.get_by_id(user_id)
        return jsonify(user.to_dict())

    @validate('json', USER_CREATE)
    def post(self):
        user = UserModel(**request.json)
        user.set_password(request.json['password'])
        user.add()
        return jsonify(user.to_dict())

    def delete(self, user_id):
        UserModel.delete_by_id(user_id)
        return jsonify({'message': 'NO_CONTENT'})


class AdvertisementView(MethodView):

    def get(self, advertisement_id):
        instance = AdvertisementModel.get_by_id(advertisement_id)
        return jsonify(instance.to_dict())

    @validate('json', ADVERTISEMENT_CREATE)
    def post(self):
        instance = AdvertisementModel(**request.json)
        instance.add()
        return jsonify(instance.to_dict())

    def delete(self, advertisement_id):
        AdvertisementModel.delete_by_id(advertisement_id)
        return jsonify({'message': 'NO_CONTENT'})
