import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class CourseToLesson(SqlAlchemyBase):
    __tablename__ = 'course_to_lesson'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    course_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("courses.uuid"))
    lesson_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("lessons.uuid"))

    course = orm.relationship("Course", back_populates="lessons", uselist=False)
    lesson = orm.relationship("Lesson", back_populates="courses", uselist=False)

    def __repr__(self):
        return f'<CourseToLesson> {self.id} {self.course_uuid} {self.lesson_uuid}'
