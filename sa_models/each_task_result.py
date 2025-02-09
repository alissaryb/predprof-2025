import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class EachTaskResult(SqlAlchemyBase):
    __tablename__ = 'each_task_result'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    test_variant_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("test_variant.uuid"), nullable=True)
    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))
    kim_type_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("kim_types.uuid"))
    group_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("groups.uuid"), nullable=True)
    tester_user = orm.relationship("User")

    correct = sqlalchemy.Column(sqlalchemy.Boolean)
