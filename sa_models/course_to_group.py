import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class CourseToGroup(SqlAlchemyBase):
    __tablename__ = 'course_to_group'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    course_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("courses.uuid"))
    group_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("groups.uuid"))

    course = orm.relationship("Course", back_populates="groups", uselist=False)
    group = orm.relationship("Group", back_populates="courses", uselist=False)

    def __repr__(self):
        return f'<CourseToGroup> {self.id} {self.course_uuid} {self.group_uuid}'
