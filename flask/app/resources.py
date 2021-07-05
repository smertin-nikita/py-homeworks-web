from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest, Forbidden

from app import api
from models import UserModel, AdvertisementModel
from schema import USER_CREATE, ADVERTISEMENT_CREATE
from validator import validate


class User(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', help='This field cannot be blank', required=True)
        self.parser.add_argument('password', help='This field cannot be blank', required=True)


class UserList(User):

    def get(self):
        users = UserModel.all()
        return jsonify([user.to_dict() for user in users])

    @validate('json', USER_CREATE)
    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_attr({'username': data.get('username')}):
            raise BadRequest(f"User {data['username']} already exists")

        user = UserModel(**data)
        user.set_password(data['password'])
        user.add()
        return jsonify(user.to_dict())


class UserToken(User):
    def post(self):
        data = self.parser.parse_args()
        current_user = UserModel.find_by_attr({'username': data.get('username')})

        if not current_user:
            raise BadRequest(f"User {data['username']} doesn't exist")

        if current_user.check_password(data.get('password')):
            access_token = create_access_token(identity=current_user.id)
            return {
                'message': f'Please, do not show it third party',
                'access_token': access_token,
            }
        else:
            raise BadRequest(f"Wrong password")


class Advertisement(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', help='This field cannot be blank', required=True)
        self.parser.add_argument('description', type=str, location='json')
        super().__init__()


class AdvertisementList(Advertisement):
    @jwt_required()
    def get(self):
        advertisements = AdvertisementModel.all()
        return jsonify([advertisement.to_dict() for advertisement in advertisements])

    @jwt_required()
    @validate('json', ADVERTISEMENT_CREATE)
    def post(self):
        data = self.parser.parse_args()

        if AdvertisementModel.find_by_attr({'title': data.get('title')}):
            raise BadRequest(f"Advertisement {data['title']} already exists")

        data['creator_id'] = get_jwt_identity()

        obj = AdvertisementModel(**data)
        obj.add()
        return jsonify(obj.to_dict())


class AdvertisementInstance(Advertisement):

    @jwt_required()
    def get(self, obj_id):
        advertisement = AdvertisementModel.get_by_id(obj_id)
        return jsonify(advertisement.to_dict())

    @jwt_required()
    def put(self, obj_id):
        data = self.parser.parse_args()
        current_user_id = get_jwt_identity()

        advertisement = AdvertisementModel.get_by_id(obj_id)

        if advertisement.creator_id == current_user_id:
            advertisement.put(data)
        else:
            raise Forbidden

        return jsonify(advertisement.to_dict())

    @jwt_required()
    def delete(self, obj_id):
        current_user_id = get_jwt_identity()
        advertisement = AdvertisementModel.get_by_id(obj_id)

        if advertisement.creator_id == current_user_id:
            AdvertisementModel.delete_by_id(obj_id)
        else:
            raise Forbidden

        return jsonify({'message': 'NO_CONTENT'})


api.add_resource(UserList, '/users', '/users/')
api.add_resource(UserToken, '/users/token', '/users/token/')
api.add_resource(AdvertisementList, '/advertisements', '/advertisements/')
api.add_resource(AdvertisementInstance, '/advertisements/<int:obj_id>', '/advertisements/<int:obj_id>/')

