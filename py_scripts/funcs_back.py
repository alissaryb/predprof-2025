import os
import uuid

from werkzeug.utils import secure_filename

from sa_models import db_session
from sa_models.courses import Course
from sa_models.course_to_user import CourseToUser

import string
import random

from sa_models.publications import Publication
from sa_models.users import User


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


def get_user_data(user: User) -> dict[str, str]:
    user_data = {
        "surname": user.surname,
        "name": user.name,
        "lastname": user.lastname,
        "class_num": user.class_number,
        "email": user.email,
        "phone_number": user.phone_number
    }
    return user_data


def get_title_courses_by_user_uuid(user_uuid: int) -> list[str]:
    db_sess = db_session.create_session()
    courses = [el[0] for el in db_sess.query(Course.title).where(user_uuid == Course.user_uuid).all()]
    return courses


def add_publication_database(form, user_uuid, files) -> None:
    db_sess = db_session.create_session()

    new_uuid = str(uuid.uuid4())
    new_publication = Publication(
        uuid=new_uuid,
        title=form.title.data,
        text=form.text.data,
        tag=form.my_courses.data,
        user_uuid=user_uuid)

    if len(files) > 0:
        for file in files:
            if file.filename == '':
                continue

            pth = f'publications_materials/{new_uuid}/'
            if not os.path.exists(pth):
                os.mkdir(pth)
                new_publication.files_folder_path = pth

            filename = secure_filename(file.filename)
            file.save(pth + filename)

    db_sess.add(new_publication)

    db_sess.commit()
    db_sess.close()
