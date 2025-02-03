import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Publication(SqlAlchemyBase):
    __tablename__ = 'publications'
    uuid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    made_on_datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    tag = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))
    author = orm.relationship("User")

    courses = orm.relationship("CourseToPublication", back_populates="publication", uselist=True)

    def __repr__(self):
        return f'<Publication> {self.uuid} {self.title} {self.text}'
