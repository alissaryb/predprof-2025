import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Course(SqlAlchemyBase):
    __tablename__ = 'courses'
    uuid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, default='Нет описания.')
    token = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    made_on_datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))
    author = orm.relationship("User")

    users = orm.relationship("CourseToUser", back_populates="course", uselist=True)
    lessons = orm.relationship("CourseToLesson", back_populates="course", uselist=True)
    groups = orm.relationship("CourseToGroup", back_populates="course", uselist=True)

    def __repr__(self):
        return f'<Course> {self.uuid} {self.title} {self.subject}'
