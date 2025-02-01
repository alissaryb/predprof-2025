from sa_models import db_session
from sa_models.courses import Course
from sa_models.course_to_user import CourseToUser

import string
import random


def get_courses_learn(user_uuid):
    db_sess = db_session.create_session()

    all_ = db_sess.query(CourseToUser).where(CourseToUser.user_uuid == user_uuid).all()
    all_ = sorted(all_, key=lambda x: x.course.made_on_datetime)
    courses = []

    for course_to_user in all_:
        course = course_to_user.course
        user = course_to_user.user

        d = {
            'title': course.title,
            'subject': course.subject,
            'token': course.token,
            'description': course.description,
            'made_on_datetime': course.made_on_datetime.strftime('%d.%m.%Y'),
            'uuid': course.uuid,
            'author': f'{user.surname} {user.name[0]}. {user.lastname[0]}.'
        }
        courses.append(d)

    db_sess.close()

    return courses


def get_courses_teach(user_uuid):
    db_sess = db_session.create_session()

    all_ = db_sess.query(Course).where(Course.user_uuid == user_uuid).order_by(Course.made_on_datetime).all()
    courses = []

    for course in all_:
        d = {
            'title': course.title,
            'subject': course.subject,
            'token': course.token,
            'description': course.description,
            'made_on_datetime': course.made_on_datetime.strftime('%d.%m.%Y'),
            'uuid': course.uuid,
            'author': f'{course.author.surname} {course.author.name[0]}. {course.author.lastname[0]}.'
        }
        courses.append(d)

    db_sess.close()

    return courses


def generate_token():
    s = string.ascii_letters + string.digits
    return ''.join(random.choice(s) for _ in range(6))
