#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_required, current_user, login_user, \
    logout_user, UserMixin
from flask_wtf.csrf import CSRFProtect

from requests import get

from forms.register import FormRegisterUser, FormLoginUser
from forms.tasks import FormAddTask, QuizForm
from forms.courses import FormAddCourse
import json
import datetime

import uuid

from sa_models import db_session
from sa_models.users import User

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


@app.route(f'/{app.config["UPLOAD_FOLDER"]}/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="")


@app.route('/practice', methods=['GET', 'POST'])
def practice():
    try:
        with open('tasks.json', 'r') as json_file:
            a = json.load(json_file)
    except ValueError:
        a = {}


    tasks = []
    for i in range(len(a)):
        b = a[str(i)]
        with open(f'tasks/task{i}.txt', "r") as f:
            s = f.read()
            b['text'] = s
        tasks.append(b)

    print(tasks)
    return render_template("3.html", title="", tasks=tasks)


@app.route('/work', methods=['GET', 'POST'])
def work():
    try:
        with open('tasks.json', 'r') as json_file:
            a = json.load(json_file)
    except ValueError:
        a = {}

    users_answers = {}
    tasks = []
    for i in range(len(a)):
        b = a[str(i)]
        b['id'] = str(i)
        tasks.append(b)

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

        return render_template("work.html", title="", tasks=tasks, is_check=True, form=form, users_answers=users_answers, mark=mark, max_mark=len(tasks))

    return render_template("work.html", title="", tasks=tasks, is_check=False, form=form, users_answers=users_answers)



@app.route('/all_courses', methods=['GET', 'POST'])
def all_courses():
    courses = [{"id": "0", "cours_name": "Подготовка к ЕГЭ на Пупоне",
                "subject": "Инфа", "type": "video",
                "link": "https://rutube.ru/play/embed/9852193",
                "description": "Господи, это такой крутой курс. Вам он жизнено необходим. Я готов перестать есть сникерсы, ради этого курса"},
               {"id": "1", "cours_name": "HHHHHHHHHHHHH", "subject": "Русич",
                "type": "presentation",
                "link": "https://nsportal.ru/sites/default/files/2023/01/05/podgotovka_k_ege_2023_no1.pptx",
                "description": "Господи, это такой крутой курс."},
               {"id": "2", "cours_name": "UUUUUUUUUUUU", "subject": "Матан",
                "description": "Господи, это такой крутой курс."},
               {"id": "3", "cours_name": "IIIIIIIIII", "subject": "Физ",
                "description": "Господи, это такой крутой курс."}]

    return render_template("all_courses.html", title="", courses=courses)

@app.route('/course/<id>', methods=['GET', 'POST'])
def courses(id):
    courses = [{"id": "0", "cours_name": "Подготовка к ЕГЭ на Пупоне",
                "subject": "Инфа", "type": "video", "link": "https://rutube.ru/play/embed/9852193",
                "description": "Господи, это такой крутой курс. Вам он жизнено необходим. Я готов перестать есть сникерсы, ради этого курса"},
               {"id": "1", "cours_name": "HHHHHHHHHHHHH", "subject": "Русич",
                "type": "presentation", "link": "https://nsportal.ru/sites/default/files/2023/01/05/podgotovka_k_ege_2023_no1.pptx",
                "description": "Господи, это такой крутой курс."},
               {"id": "2", "cours_name": "UUUUUUUUUUUU", "subject": "Матан",
                "description": "Господи, это такой крутой курс."},
               {"id": "3", "cours_name": "IIIIIIIIII", "subject": "Физ",
                "description": "Господи, это такой крутой курс."}]

    course1 = courses[int(id)]
    print(id, course1['id'])
    return render_template("course.html", title="", id=id, course1=course1)




@app.route('/profile', methods=['GET'])
def profile():
    user_group = [{"token": "g4d65g", "group_name": "11 класс it"},
                  {"token": "р375gy", "group_name": "10 класс mt"}]

    return render_template("profile.html", title="Личный кабинет",
                           user={'id': '0', 'name': 'Алиса', 'surname': 'Рыбакова',
                                 'lastname': 'Рыбакова', 'email': 'a1@a.com',
                                 'phone_number': '89154559579', 'password': 'qwerty123',
                                 'class_num': 10 }, user_group=user_group, len=len(user_group))
    referer = request.base_url

    if referer == "http://127.0.0.1:8080/profile":
        return redirect('/error1')

    if name == "":
        return redirect('/error1')

    try:
        with open('users.json', 'r') as json_file:
            a = json.load(json_file)
    except ValueError:
        a = {}

    for i in range(len(a)):
        if a[str(i)]['nickname'] == name:
            user = a[str(i)]
            print(user)

            user_group = []
            return render_template("profile.html", title="Личный кабинет", user=user, user_group=user_group, len=len(user_group))

    return render_template("profile.html", title="Личный кабинет",
                           user={'id': '0', 'name': 'Алиса',
                                 'surname': 'Рыбакова', 'lastname': 'Рыбакова',
                                 'email': 'a1@a.com',
                                 'phone_number': '89154559579',
                                 'password': 'qwerty123', 'class_num': 10})
                           #user_group=user_group, len=len(user_group))


@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    arr = {1: {"correct": 10, "all": 23}, 2: {"correct": 15, "all": 15}, 3: {"correct": 1, "all": 20}, 4: {"correct": 34, "all": 100}, 5: {"correct": 22, "all": 37}, 6: {"correct": 16, "all": 56}}
    d = [i for i in range(1, len(arr)+1)]

    for i in d:
        p = arr[i]['correct'] / arr[i]['all'] * 100
        arr[i]['pr'] = p

    return render_template("statistic.html", arr=arr, d=d)


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    form = FormAddCourse()
    if form.submit.data == True:

        print(form.type.data)

        return redirect("/")
    return render_template("add_course.html", title="Добавление курса", form=form)



@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = FormAddTask()
    print(form)
    if form.submit.data == True:
        print("SUBMIT")
        try:
            with open('tasks.json', 'r') as json_file:
                a = json.load(json_file)
        except ValueError:
            a = {}

        print(a)

        id = len(a)

        task_ = {
            "id": id,
            "type": form.type.data,
            "source": form.source.data,
            "task": form.task.data,
            "ans": form.ans.data,
            "level": form.level.data
        }

        a[id] = task_
        with open("tasks.json", 'w') as json_file:
            json.dump(a, json_file)
        with open(f'tasks/task{id}.txt', 'w') as f:
            f.write(form.task.data)

        return redirect("/")
    return render_template("add_task.html", title="Добавление задания", form=form)


@app.route('/teacher_groups', methods=['GET', 'POST'])
def teacher_groups():
    courses = [{"id": "0", "num_class": 6, "token": "sh24re"},
               {"id": "1", "num_class": 10, "token": "dfs3y53"},
               {"id": "2", "num_class": 10, "token": "fdj836"}]

    return render_template("teacher_groups.html", courses=courses)


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
