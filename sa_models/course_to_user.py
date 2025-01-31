import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class CourseToUser(SqlAlchemyBase):
    __tablename__ = 'course_to_user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    course_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("courses.uuid"))
    user_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.uuid"))

    course = orm.relationship("Course", back_populates="users", uselist=False)
    user = orm.relationship("User", back_populates="courses", uselist=False)

    def __repr__(self):
        return f'<CourseToUser> {self.id} {self.course_uuid} {self.user_uuid}'
