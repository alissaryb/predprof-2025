import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Problem(SqlAlchemyBase):
    __tablename__ = 'problems'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    uuid = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    files_folder_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    difficulty = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    kim_type_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("kim_types.uuid"))
    kim_type = orm.relationship("KimType")

    def __repr__(self):
        return f'<Problem> {self.uuid} {self.text}'
