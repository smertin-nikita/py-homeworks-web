import hashlib
from datetime import datetime

from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy import exc

import config
from app import db


class BaseModelMixin:

    @classmethod
    def all(cls):
        objs = cls.query.all()
        if objs:
            return objs
        else:
            raise NotFound

    @classmethod
    def get_by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            raise BadRequest(str(e.orig))

    @classmethod
    def find_by_attr(cls, kwargs):
        return cls.query.filter_by(**kwargs).first()


    @classmethod
    def delete_by_id(cls, obj_id):
        cls.query.get(obj_id)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            raise BadRequest

    def to_dict(self):
        raise NotImplementedError


class UserModel(db.Model, BaseModelMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False, default='')
    password = db.Column(db.String(128))
    advertisements = db.relationship('AdvertisementModel', backref='user')

    def __str__(self):
        return '<User {}>'.format(self.username)

    def __repr__(self):
        return str(self)

    def set_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.CONFIG["SALT"]}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.CONFIG["SALT"]}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()

    # @classmethod
    # def find_by_username(cls, username):
    #     return cls.query.filter_by(username=username).first()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            "email": self.email
        }


class AdvertisementModel(db.Model, BaseModelMixin):
    """Объявление."""

    __tablename__ = 'advertisement'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.Text, index=True, nullable=False, default='')
    creator_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __str__(self):
        return '<Advertisement {}>'.format(self.title)

    def __repr__(self):
        return str(self)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            "description": self.description,
            'creator_id': self.creator_id,
            'created_on': self.created_on

        }
