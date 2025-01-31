import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'
    uuid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, default='Нет описания.')
    token = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    made_on_datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))
    author = orm.relationship("User")

    courses = orm.relationship("CourseToGroup", back_populates="group", uselist=True)
    users = orm.relationship("GroupToUser", back_populates="group", uselist=True)

    def __repr__(self):
        return f'<Course> {self.uuid} {self.title}'
