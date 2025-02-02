import sqlalchemy

from .db_session import SqlAlchemyBase


class Difficulty(SqlAlchemyBase):
    __tablename__ = 'difficulties'
    uuid = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f'<Difficulty> {self.uuid} {self.title}'
