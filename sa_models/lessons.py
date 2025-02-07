import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'
    uuid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    tag = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    made_on_datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    files_folder_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))
    author = orm.relationship("User")

    courses = orm.relationship("CourseToLesson", back_populates="lesson", uselist=True)

    def __repr__(self):
        return f'<Lesson> {self.uuid} {self.title} {self.text}'
