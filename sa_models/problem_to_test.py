import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class ProblemToTest(SqlAlchemyBase):
    __tablename__ = 'problem_to_test'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    problem_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("problems.uuid"))
    test_variant_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("test_variant.uuid"))

    problem = orm.relationship("Problem")
    test_variant = orm.relationship("Test_variant", back_populates="tasks")

