import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    uuid = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    lastname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    class_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    school = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    reg_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    access_level = sqlalchemy.Column(sqlalchemy.String, default='user')

    courses = orm.relationship("CourseToUser", back_populates="user", uselist=True)
    groups = orm.relationship("GroupToUser", back_populates="user", uselist=True)

    def __repr__(self):
        return f'<User> {self.uuid} {self.email} {self.username}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
