import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class GroupToUser(SqlAlchemyBase):
    __tablename__ = 'group_to_user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    group_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("groups.uuid"))
    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))

    group = orm.relationship("Group", back_populates="users", uselist=False)
    user = orm.relationship("User", back_populates="groups", uselist=False)

    def __repr__(self):
        return f'<GroupToUser> {self.id} {self.group_uuid} {self.user_uuid}'
