import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Test_variant(SqlAlchemyBase):
    __tablename__ = 'test_variant'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    uuid = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))
    author = orm.relationship("User")

    tasks = orm.relationship("ProblemToTest", back_populates="test_variant")
