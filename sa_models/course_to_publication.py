import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class CourseToPublication(SqlAlchemyBase):
    __tablename__ = 'course_to_publication'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    course_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("courses.uuid"))
    publication_uuid = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("publications.uuid"))

    course = orm.relationship("Course", back_populates="publications", uselist=False)
    publication = orm.relationship("Publication", back_populates="courses", uselist=False)

    def __repr__(self):
        return f'<CourseToPublication> {self.id} {self.course_uuid} {self.publication_uuid}'
