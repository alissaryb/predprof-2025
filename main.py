#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
from functools import wraps

from flask import Flask, render_template, request, redirect, send_from_directory
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from forms.register import FormRegisterUser, FormLoginUser
from forms.tasks import FormAddTask, QuizForm
from forms.courses import FormAddCourse, FormAddPublication

import json
import uuid

from py_scripts.funcs_back import get_user_data, add_publication_database
from sa_models import db_session
from sa_models.users import User
from sa_models.courses import Course
from sa_models.problems import Problem
from sa_models.kim_types import KimType
from sa_models.course_to_user import CourseToUser
from py_scripts import funcs_back


if not os.path.exists('materials/'):
    os.mkdir('materials/')
if not os.path.exists('problems_materials/'):
    os.mkdir('problems_materials/')
if not os.path.exists('publications_materials/'):
    os.mkdir('publications_materials/')
if not os.path.exists('database/'):
    os.mkdir('database/')

app = Flask(__name__)
db_session.global_init('database/portal.db')

app.config['SECRET_KEY'] = 'wrbn2i3o4ufbnldq4nwku'
app.config['UPLOAD_FOLDER'] = 'uploads'
login_manager = LoginManager()
login_manager.init_app(app)


def login_forbidden(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        return func(*args, **kwargs)

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="")


@app.route('/materials/<name>')
def download_file(name):
    return send_from_directory('materials', name)


@app.route('/random_work', methods=['GET', 'POST'])
def random_work():
    return render_template("random_work.html")


@app.route('/work', methods=['GET', 'POST'])
def work():

    users_answers = {}
    tasks = [{""}, {""}, {""}]

    form = QuizForm()

    answers = []
    if form.submit.data:
        mark = 0
        for i in range(len(tasks)):
            key = f'user_answer_{tasks[i]["id"]}'
            users_answers[tasks[i]['id']] = request.form.get(key)
            print(tasks[i]['ans'])
            if users_answers[tasks[i]['id']] == tasks[i]['ans']:
                mark += 1
            print()

        try:
            with open('answers_users.json', 'r') as json_file:
                cur_ans_user = json.load(json_file)
        except ValueError:
            cur_ans_user = {}

        cur_ans_user[str(len(cur_ans_user))] = users_answers
        with open("answers_users.json", 'w') as json_file:
            json.dump(cur_ans_user, json_file)

        return render_template("work.html", title="", tasks=tasks,
                               is_check=True, form=form,
                               users_answers=users_answers, mark=mark,
                               max_mark=len(tasks))

    return render_template("work.html", title="", tasks=tasks, is_check=False, form=form, users_answers=users_answers)

@login_required
@app.route('/profile', methods=['GET'])
def profile():
    # TODO: спроси Алису про user_group
    user_group = [{"token": "g4d65g", "group_name": "11 класс it"},
                  {"token": "р375gy", "group_name": "10 класс mt"}]
    user_data = get_user_data(current_user)
    return render_template("profile.html", title="Личный кабинет", user=user_data)
    # return render_template("profile.html", title="Личный кабинет",
    #                        user={'id': '0', 'name': 'Алиса', 'surname': 'Рыбакова',
    #                              'lastname': 'Рыбакова', 'email': 'a1@a.com',
    #                              'phone_number': '89154559579', 'password': 'qwerty123',
    #                              'class_num': 10 }, user_group=user_group, len=len(user_group))



@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    arr = {1: {"correct": 10, "all": 23}, 2: {"correct": 15, "all": 15},
           3: {"correct": 1, "all": 20}, 4: {"correct": 34, "all": 100},
           5: {"correct": 22, "all": 37}, 6: {"correct": 16, "all": 56}}
    d = [i for i in range(1, len(arr) + 1)]

    for i in d:
        p = arr[i]['correct'] / arr[i]['all'] * 100
        arr[i]['pr'] = p

    return render_template("statistic.html", arr=arr, d=d)

@app.route('/my_grops', methods=['GET', 'POST'])
def my_grops():
    return render_template("my_grops.html")


@app.route('/teacher_groups', methods=['GET', 'POST'])
def teacher_groups():
    courses = [{"id": "0", "num_class": 6, "token": "sh24re"},
               {"id": "1", "num_class": 10, "token": "dfs3y53"},
               {"id": "2", "num_class": 10, "token": "fdj836"}]

    return render_template("teacher_groups.html", courses=courses)


@app.route('/course/<course_uuid>/add_publication', methods=['GET', 'POST'])
@login_required
def add_publication(course_uuid):
    form = FormAddPublication(current_user.uuid)
    if form.validate_on_submit():
        files = request.files.getlist(form.files.name)
        add_publication_database(form, current_user.uuid, files,  course_uuid)

        return redirect(f'/page_course/{course_uuid}')

    return render_template("add_publication.html", form=form)


@app.route('/practice', methods=['GET'])
def practice():
    db_sess = db_session.create_session()

    all_tasks = db_sess.query(Problem).all()

    problems = []
    for problem in all_tasks:
        data = {
            'level': problem.difficulty,
            'num_type': problem.kim_type.kim_id,
            'text_type': problem.kim_type.title,
            'uuid': problem.uuid,
            'text': problem.text,
            'ans': problem.answer,
            'files_folder_path': []
        }
        if problem.files_folder_path is not None:
            for file_ in  os.listdir(problem.files_folder_path):
                path_ = [f'/{problem.files_folder_path}{file_}', 'other']
                if file_.endswith('.png') or file_.endswith('.jpeg') or file_.endswith('.jpg') or file_.endswith('.webp') or \
                    file_.endswith('.gif'):
                    path_[1] = 'img'
                data['files_folder_path'].append(path_)
        problems.append(data)

    return render_template("practice.html", title="", tasks=problems)


@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = FormAddTask()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        kimtype = db_sess.query(KimType).where(KimType.title == form.type.data).first()

        new_problem = Problem()
        new_uuid = str(uuid.uuid4())
        new_problem.uuid = new_uuid
        new_problem.text = form.task.data
        new_problem.source = form.source.data
        new_problem.answer = form.ans.data
        new_problem.difficulty = form.level.data
        new_problem.kim_type_uuid = kimtype.uuid

        files = request.files.getlist(form.files.name)
        if len(files) > 0:
            for file in files:
                if file.filename == '':
                    continue

                pth = f'problems_materials/{new_uuid}/'
                if not os.path.exists(pth):
                    os.mkdir(pth)
                    new_problem.files_folder_path = pth

                filename = secure_filename(file.filename)
                file.save(pth + filename)

        db_sess.add(new_problem)
        db_sess.commit()
        db_sess.close()

        return redirect("/")

    return render_template("add_task.html", title="Добавление задания",
                           form=form)


@app.route('/page_course/<course_uuid>', methods=['GET'])
@login_required
def course_by_uuid(course_uuid):
    db_sess = db_session.create_session()

    course = db_sess.query(Course).where(Course.uuid == course_uuid).first()

    if course is None:
        db_sess.close()
        return render_template("error.html", title="Курс не найден", err='Курс не найден')

    is_registered = db_sess.query(CourseToUser).where(CourseToUser.user_uuid == current_user.uuid,
                                                      CourseToUser.course_uuid == course_uuid).first()
    is_author = (course.author.id == current_user.id)
    # TODO: как передавать-то дальше
    if is_registered is None and not is_author:
        db_sess.close()
        return render_template("error.html", title="Вы не зарегистрированы на курс",
                               err='Вы не зарегистрированы на курс')

    course_data = {
        'uuid': course_uuid,
        'title': course.title,
        'subject': course.subject,
        'description': course.description,
        'token': course.token,
        'made_on_datetime': course.made_on_datetime.strftime('%d.%m.%Y'),
        'author': f'{course.author.surname[0]} {course.author.name[0]}. {course.author.lastname[0]}.',
        'author_uuid': course.author.uuid
    }

    all_tags = []
    publications = course.publications
    print(publications)
    for note in publications:
        note_data = {
            'uuid': note.uuid,
            'title': note.title,
            'text': note.text,
            'made_on_datetime': note.made_on_datetime.strftime('%d.%m.%Y'),
            'tag': note.tag,
            'files_folder_path': []
        }
        if note.files_folder_path is not None:
            for file_ in  os.listdir(note.files_folder_path):
                path_ = [f'/{note.files_folder_path}{file_}', 'other']
                if file_.endswith('.png') or file_.endswith('.jpeg') or file_.endswith('.jpg') or file_.endswith('.webp') or \
                    file_.endswith('.gif'):
                    path_[1] = 'img'
                if file_.endswith('.mp4') or file_.endswith('.mov') or file_.endswith('.wmv') or file_.endswith('.mkv'):
                    path_[1] = 'video'
                note_data['files_folder_path'].append(path_)
        all_tags.append(note_data['tag'])
        publications.append(note_data)

    db_sess.close()

    return render_template("page_course.html", title="Страница курса", course=course_data,
                           publications=publications)


@app.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    form = FormAddCourse()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        new_uuid = str(uuid.uuid4())
        new_course = Course()
        new_course.title = form.title.data
        new_course.description = form.description.data
        new_course.subject = form.subject.data
        new_course.uuid = new_uuid
        new_course.token = funcs_back.generate_token()
        new_course.user_uuid = current_user.uuid

        db_sess.add(new_course)
        db_sess.commit()

        db_sess.close()

        return redirect(f"/page_course/{new_uuid}")

    return render_template("add_course.html", title="Создание курса", form=form)


@app.route('/all_courses', methods=['GET'])
def all_courses():
    db_sess = db_session.create_session()

    all_ = db_sess.query(Course).order_by(Course.made_on_datetime).all()
    registered_courses_uuids = []
    if current_user.is_authenticated:
        registered_courses_uuids = (funcs_back.get_courses_teach(current_user.uuid) +
                                    funcs_back.get_courses_learn(current_user.uuid))
        for i in range(len(registered_courses_uuids)):
            registered_courses_uuids[i] = registered_courses_uuids[i]['uuid']

    courses = []
    for course in all_:
        d = {
            'title': course.title,
            'subject': course.subject,
            'token': course.token,
            'description': course.description,
            'author': f'{course.author.surname} {course.author.name[0]}. {course.author.lastname[0]}.',
            'made_on_datetime': course.made_on_datetime.strftime('%d.%m.%Y'),
            'uuid': course.uuid,
        }
        courses.append(d)

    db_sess.close()

    return render_template("all_courses.html", title="Каталог курсов", courses=courses,
                           registered_courses_uuids=registered_courses_uuids)


@app.route('/my_courses', methods=['GET'])
@login_required
def my_courses():
    student_courses = funcs_back.get_courses_learn(current_user.uuid)
    teacher_courses = funcs_back.get_courses_teach(current_user.uuid)

    return render_template("my_courses.html", teacher_courses=teacher_courses,
                           student_courses=student_courses, title="Мои курсы")


@app.route('/register', methods=['GET', 'POST'])
@login_forbidden
def register():
    form = FormRegisterUser()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        exists = db_sess.query(User).where(User.username == form.username.data).first()
        if exists is not None:
            db_sess.close()
            return render_template("register.html", title="Регистрация", form=form,
                                   message="Аккаунт с таким никнеймом уже зарегистрирован")

        user = User()
        user.uuid = str(uuid.uuid4())
        user.email = form.email.data
        user.name = form.name.data
        user.surname = form.surname.data
        user.username = form.username.data
        user.lastname = form.lastname.data
        user.class_number = form.class_num.data
        user.school = form.school.data
        user.set_password(form.password.data)
        user.access_level = 'user'
        user.phone_number = form.phone_number.data
        db_sess.add(user)
        db_sess.commit()

        login_user(user, remember=True)

        db_sess.close()

        return redirect('/')

    return render_template("register.html", title="Регистрация", form=form)


@app.route('/login', methods=['GET', 'POST'])
@login_forbidden
def login():
    form = FormLoginUser()
    if form.validate_on_submit():
        email_or_username = form.email_or_username.data
        psw = form.password.data
        db_sess = db_session.create_session()

        exists = db_sess.query(User).where(User.email == email_or_username).first()
        exists2 = db_sess.query(User).where(User.username == email_or_username).first()
        if exists is None and exists2 is None:
            db_sess.close()
            return render_template("login.html", title="Авторизация", form=form,
                                   message="Такого пользователя не существует")

        if exists is None and exists2 is not None:
            exists = exists2

        if not exists.check_password(psw):
            db_sess.close()
            return render_template("login.html", title="Авторизация", form=form,
                                   message="Неверный пароль")

        login_user(exists, remember=True)
        db_sess.close()
        return redirect("/")

    return render_template("login.html", title="Авторизация", form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1", threaded=True)
