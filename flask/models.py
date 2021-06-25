import hashlib
from datetime import datetime

from sqlalchemy import exc

import config
import errors
from app import db


class BaseModelMixin:

    @classmethod
    def get_by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        if obj:
            return obj
        else:
            raise errors.NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            raise errors.BadRequest(e.orig.pgerror)

    @classmethod
    def delete_by_id(cls, obj_id):
        cls.query.get(obj_id)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            raise errors.BadRequest(e.message)

    def to_dict(self):
        raise NotImplementedError


class User(db.Model, BaseModelMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    advertisements = db.relationship('Advertisement', backref='user')

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

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            "email": self.email
        }


class Advertisement(db.Model, BaseModelMixin):
    """Объявление."""

    __tablename__ = 'advertisement'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.Text, index=True)
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
