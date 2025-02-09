import datetime
import os
import uuid

from werkzeug.utils import secure_filename

from py_scripts import consts
from sa_models import db_session
from sa_models.courses import Course
from sa_models.course_to_user import CourseToUser

import string
import random

from sa_models.group_to_user import GroupToUser
from sa_models.groups import Group
from sa_models.kim_types import KimType
from sa_models.problem_to_test import ProblemToTest
from sa_models.problems import Problem
from sa_models.test_results import Test_result
from sa_models.test_to_group import TestToGroup
from sa_models.test_variant import Test_variant
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
            'made_on_datetime': f'{course.made_on_datetime.strftime('%d.%m.%Y')} в 'f'{course.made_on_datetime.strftime('%H:%M')}',
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
            'made_on_datetime': f'{course.made_on_datetime.strftime('%d.%m.%Y')} в 'f'{course.made_on_datetime.strftime('%H:%M')}',
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
        "source": task.source if task.source is not None else "Источник не указан",
        "answer": task.answer,
        "difficulty": task.difficulty,
        'files_folder_path': []
    }
    if task.files_folder_path is not None:
        for file_ in os.listdir(task.files_folder_path):
            path_ = [f'/{task.files_folder_path}{file_}', 'other']
            if file_.endswith('.png') or file_.endswith('.jpeg') or file_.endswith('.jpg') or file_.endswith(
                    '.webp') or \
                    file_.endswith('.gif'):
                path_[1] = 'img'
            if file_.endswith('.mp4') or file_.endswith('.mov') or file_.endswith('.wmv') or file_.endswith('.mkv'):
                path_[1] = 'video'
            res['files_folder_path'].append(path_)
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


def get_groups_learn(user_uuid):
    db_sess = db_session.create_session()

    all_ = db_sess.query(GroupToUser).where(GroupToUser.user_uuid == user_uuid).all()
    all_ = sorted(all_, key=lambda x: x.group.made_on_datetime, reverse=True)
    groups = []

    for group_to_user in all_:
        group = group_to_user.group
        user = group_to_user.user

        d = {
            'title': group.title,
            'description': group.description,
            'made_on_datetime': f'{group.made_on_datetime.strftime('%d.%m.%Y')} в 'f'{group.made_on_datetime.strftime('%H:%M')}',
            'uuid': group.uuid,
            'author': f'{user.surname} {user.name[0]}. {user.lastname[0]}.'
        }
        groups.append(d)

    db_sess.close()

    return groups


def get_groups_teach(user_uuid):
    db_sess = db_session.create_session()

    all_ = db_sess.query(Group).where(Group.user_uuid == user_uuid).order_by(Group.made_on_datetime.desc()).all()
    groups = []

    for group in all_:
        d = {
            'title': group.title,
            'description': group.description,
            'made_on_datetime': f'{group.made_on_datetime.strftime('%d.%m.%Y')} в 'f'{group.made_on_datetime.strftime('%H:%M')}',
            'uuid': group.uuid,
            'author': f'{group.author.surname} {group.author.name[0]}. {group.author.lastname[0]}.'
        }
        groups.append(d)

    db_sess.close()

    return groups


def make_variant_to_db(data: list[str], user_id: uuid, title: string) -> uuid:
    db_sess = db_session.create_session()
    new_uuid = str(uuid.uuid4())
    variant = Test_variant(
        uuid=new_uuid,
        user_uuid=user_id,
        title=title
    )
    db_sess.add(variant)
    db_sess.commit()

    for el in data:
        id_task = int(el)
        uuid_task = db_sess.query(Problem).where(id_task == Problem.id).first().uuid

        problem_to_test = ProblemToTest(
            problem_uuid=uuid_task,
            test_variant_uuid=new_uuid
        )
        db_sess.add(problem_to_test)
    db_sess.commit()
    db_sess.close()

    return new_uuid


def tasks_by_test_uuid(test_uuid: uuid) -> list[dict]:
    db_sess = db_session.create_session()
    test = db_sess.query(Test_variant).filter(test_uuid == Test_variant.uuid).first()
    res = list()
    for task in test.tasks:
        task_uuid = task.problem_uuid
        problem = db_sess.query(Problem).where(Problem.uuid == task_uuid).first()
        tmp = dict()
        tmp['key'] = (problem.kim_type.title, problem.kim_type_uuid)
        tmp['value'] = task_render(problem)
        res.append(tmp)
    return res


def render_variant(variant: Test_variant):
    res = {
        "id": variant.id,
        "uuid": variant.uuid,
        "title": variant.title,
        "url": f"http://{consts.HOST}:{consts.PORT}/test/{variant.uuid}"
    }
    return res


def get_variants_by_user_uuid(user_uuid: uuid):
    db_sess = db_session.create_session()
    variants = db_sess.query(Test_variant).where(Test_variant.user_uuid == user_uuid).all()
    res = list()
    for el in variants:
        res.append(render_variant(el))
    db_sess.close()
    return res


def get_json_data(filename: string) -> dict:
    import json
    with open(filename, "rt", encoding="utf8") as myfile:
        return json.load(myfile)


def give_variant_to_group(group_uuid: uuid, data: dict) -> None:
    db_sess = db_session.create_session()
    test_to_group = TestToGroup(
        test_uuid=data.get("test_uuid"),
        group_uuid=group_uuid,
        date_start=datetime.datetime.strptime(data.get("start_date"), "%d/%m/%Y") if data.get("start_date") else None,
        date_end=datetime.datetime.strptime(data.get("end_date"), "%d/%m/%Y") if data.get("end_date") else None,
        duration=int(data.get("duration")) if data.get("duration") else None,
        feedback=int(data.get("option")),
        criteria_5=int(data.get("criteria_5")) if data.get("criteria_5") else None,
        criteria_4=int(data.get("criteria_4")) if data.get("criteria_4") else None,
        criteria_3=int(data.get("criteria_3")) if data.get("criteria_3") else None,
        criteria_2=int(data.get("criteria_2")) if data.get("criteria_2") else None,
    )
    db_sess.add(test_to_group)
    db_sess.commit()
    db_sess.close()




def get_user_result_of_test_by_user_uuid(user_uuid: uuid, test_uuid: uuid, group_uuid: uuid) -> dict:
    db_sess = db_session.create_session()
    result = db_sess.query(Test_result).filter(Test_result.user_uuid == user_uuid, Test_result.group_uuid == group_uuid,
                                               Test_result.test_variant_uuid == test_uuid).first()
    user = db_sess.query(User).where(User.uuid == user_uuid).first()
    data = {
        "name": f"{user.surname} {user.name} {user.lastname}",
        "scores": result.res_scores if result else "Работа не пройдена",
        "max_scores": result.max_scores if result else "Работа не пройдена",
        "spend_time": (result.date_end - result.date_start).minutes if result and result.date_end else "Не указано"
    }
    db_sess.close()
    return data
