import sqlalchemy

from .db_session import SqlAlchemyBase


class KimType(SqlAlchemyBase):
    __tablename__ = 'kim_types'
    uuid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.Title, nullable=False)
    points = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    kim_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __repr__(self):
        return f'<KimType> {self.uuid} {self.title}'
