import os
import uuid

from werkzeug.utils import secure_filename

from sa_models import db_session
from sa_models.courses import Course
from sa_models.course_to_user import CourseToUser

import string
import random

from sa_models.kim_types import KimType
from sa_models.problems import Problem
from sa_models.lessons import Lesson
from sa_models.users import User
from sa_models.course_to_lesson import CourseToLesson


def get_courses_learn(user_uuid):
    db_sess = db_session.create_session()

    all_ = db_sess.query(CourseToUser).where(CourseToUser.user_uuid == user_uuid).all()
    all_ = sorted(all_, key=lambda x: x.course.made_on_datetime, reverse=True)
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

    all_ = db_sess.query(Course).where(Course.user_uuid == user_uuid).order_by(Course.made_on_datetime.desc()).all()
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


def add_lesson_database(form, user_uuid, files, lesson_text) -> None:
    db_sess = db_session.create_session()

    new_uuid = str(uuid.uuid4())
    new_lesson = Lesson(
        uuid=new_uuid,
        title=form.title.data,
        description=form.description.data,
        text=lesson_text,
        tag=form.tag.data,
        user_uuid=user_uuid
    )

    if len(files) > 0:
        for file in files:
            if file.filename == '':
                continue

            pth = f'lessons_materials/{new_uuid}/'
            if not os.path.exists(pth):
                os.mkdir(pth)
                new_lesson.files_folder_path = pth

            filename = secure_filename(file.filename)
            file.save(pth + filename)

    db_sess.add(new_lesson)

    for course_uuid in form.my_courses.data:
        new_relation = CourseToLesson()
        new_relation.course_uuid = course_uuid
        new_relation.lesson_uuid = new_uuid
        db_sess.add(new_relation)

    db_sess.commit()
    db_sess.close()


# TODO: сделать сортировку для 1921
def get_kim_dict():
    db_sess = db_session.create_session()
    all_kim = db_sess.query(KimType).order_by(KimType.kim_id).all()
    res = dict()
    for el in all_kim:
        res[el.kim_id] = (el.title, el.uuid)
    return res


def task_render(task: Problem):
    res = {
        "uuid": task.uuid,
        "text": task.text if task.text is not None else "Нет описания",
        "files_folder_path": task.files_folder_path,
        "source": task.source if task.source is not None else "Источник не указан",
        "answer": task.answer,
        "difficulty": task.difficulty
    }
    return res


def get_tasks(data) -> list[dict]:
    db_sess = db_session.create_session()
    res = list()
    for key, val in data.items():
        tmp = list()
        tasks = db_sess.query(Problem).filter(Problem.kim_type_uuid == key).limit(val).all()
        for el in tasks:
            tmp.append(task_render(el))
        if tmp:
            title = db_sess.query(KimType.title).filter(KimType.uuid == key).first()[0]
            res.append({"key": (title, key), "value": tmp.copy()})
    db_sess.close()
    return res
