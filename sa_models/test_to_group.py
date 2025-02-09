import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class TestToGroup(SqlAlchemyBase):
    __tablename__ = 'test_to_group'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    test_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("test_variant.uuid"))
    group_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("groups.uuid"))
    date_start = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    date_end = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    feedback = sqlalchemy.Column(sqlalchemy.Integer)
    criteria_5 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    criteria_4 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    criteria_3 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    criteria_2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    test = orm.relationship("Test_variant")
    group = orm.relationship("Group", back_populates="tests", uselist=False)
