import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Test_result(SqlAlchemyBase):
    __tablename__ = 'test_result'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    test_variant_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("test_variant.uuid"))
    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))
    group_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("groups.uuid"), nullable=True)
    tester_user = orm.relationship("User")

    res_scores = sqlalchemy.Column(sqlalchemy.Integer)
    max_scores = sqlalchemy.Column(sqlalchemy.Integer)
    date_end = sqlalchemy.Column(sqlalchemy.DateTime)
    date_start = sqlalchemy.Column(sqlalchemy.DateTime)



    test_work = orm.relationship("Test_variant")

