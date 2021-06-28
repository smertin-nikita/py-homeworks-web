from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from app import api
from models import UserModel, AdvertisementModel
from schema import USER_CREATE, ADVERTISEMENT_CREATE
from validator import validate

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserList(Resource):

    def get(self):
        users = UserModel.all()
        return jsonify([user.to_dict() for user in users])

    @validate('json', USER_CREATE)
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_attr({'username': data.get('username')}):
            raise BadRequest(f"User {data['username']} already exists")

        user = UserModel(**data)
        user.set_password(data['password'])
        user.add()
        return jsonify(user.to_dict())


class UserToken(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_attr({'username': data.get('username')})

        if not current_user:
            raise BadRequest(f"User {data['username']} doesn't exist")

        if current_user.check_password(data.get('password')):
            access_token = create_access_token(identity=data['username'])
            return {
                'message': f'Please, do not show it third party',
                'access_token': access_token,
            }
        else:
            raise BadRequest(f"Wrong password")


adver_parser = reqparse.RequestParser()
adver_parser.add_argument('title', help='This field cannot be blank', required=True)


class AdvertisementList(Resource):
    @jwt_required()
    def get(self):
        advertisements = AdvertisementModel.all()
        return jsonify([advertisement.to_dict() for advertisement in advertisements])

    @jwt_required()
    @validate('json', ADVERTISEMENT_CREATE)
    def post(self):
        data = adver_parser.parse_args()

        if AdvertisementModel.find_by_attr({'title': data.get('title')}):
            raise BadRequest(f"Advertisement {data['title']} already exists")

        data['creator_id'] = get_jwt_identity()

        obj = AdvertisementModel(**data)
        obj.add()
        return jsonify(obj.to_dict())


class Advertisement(Resource):
    @jwt_required()
    def get(self, obj_id):
        advertisement = AdvertisementModel.get_by_id(obj_id)
        return jsonify(advertisement.to_dict())

    @jwt_required()
    def put(self, obj_id):
        data = adver_parser.parse_args()
        current_user = get_jwt_identity()

        advertisement = AdvertisementModel.get_by_id(obj_id)

        if advertisement.get('creator_id') == current_user:
            pass
        return jsonify(advertisement.to_dict())

    @jwt_required()
    def delete(self, advertisement_id):
        AdvertisementModel.delete_by_id(advertisement_id)
        return jsonify({'message': 'NO_CONTENT'})


api.add_resource(UserList, '/users', '/users/')
api.add_resource(UserToken, '/users/token', '/users/token/')
api.add_resource(AdvertisementList, '/advertisements', '/advertisements/')
api.add_resource(Advertisement, '/advertisements/<int:obj_id>')

