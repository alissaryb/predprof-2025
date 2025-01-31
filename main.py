from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_required, current_user, login_user, \
    logout_user, UserMixin
from flask_wtf.csrf import CSRFProtect

from requests import get

from forms.register import FormRegisterUser, FormLoginUser
from forms.tasks import FormAddTask, QuizForm
from forms.courses import FormAddCourse, FormAddPublication
import json
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="")


@app.route('/materials/<name>')
def download_file(name):
    return send_from_directory('materials', name)

@app.route('/random_work', methods=['GET', 'POST'])
def random_work():


    return render_template("random_work.html")

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
        with open(f'tasks/task{i}.txt', "r", encoding="utf-8") as f:
            s = f.read()
            b['text'] = s
            print(s)
        tasks.append(b)

    print(tasks)
    return render_template("practice.html", title="", tasks=tasks)


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

        return render_template("work.html", title="", tasks=tasks,
                               is_check=True, form=form,
                               users_answers=users_answers, mark=mark,
                               max_mark=len(tasks))

    return render_template("work.html", title="", tasks=tasks, is_check=False,
                           form=form, users_answers=users_answers)



@app.route('/add_publication', methods=['GET', 'POST'])
def add_publication():
    form = FormAddPublication()

    my_courses = ["1", "2", "3"]
    form.my_courses.choices = my_courses

    return render_template("add_publication.html", form=form)


@app.route('/all_courses', methods=['GET', 'POST'])
def all_courses():
    courses = [
        {"uuid": "0", "title": "Подготовка к ЕГЭ на Пупоне", "subject": "Инфа",
         "type": "public",
         "description": "Господи, это такой крутой курс. Вам он жизнено необходим. Я готов перестать есть сникерсы, ради этого курса",
         "token": "36b4b99", "made_on_datetime": 2424, "author": "ЕlnjnlnlС"},
        {"uuid": "1", "title": "Подготовка к ЕГЭ на Пупоне", "subject": "Инфа",
         "type": "public",
         "description": "Господи, это такой крутой курс. Вам он жизнено необходим. Я готов перестать есть сникерсы, ради этого курса",
         "token": "36b4b99", "made_on_datetime": 2424, "author": "Фёдоров Кирилл Евгеньевич"},
        {"uuid": "2", "title": "Подготовка к ЕГЭ на Пупоне", "subject": "Инфа",
         "type": "public",
         "description": "Господи, это такой крутой курс. Вам он жизнено необходим. Я готов перестать есть сникерсы, ради этого курса",
         "token": "36b4b99", "made_on_datetime": 2424, "author": "ЕmmjnjlnljС"}]

    return render_template("all_courses.html", title="", courses=courses)


@app.route('/course/<id>', methods=['GET', 'POST'])
def courses(id):
    courses = [{"uuid": "0", "title": "Подготовка к ЕГЭ на Пупоне", "subject": "Инфа",
         "type": "public",
         "description": "Господи, это такой крутой курс. Вам он жизнено необходим. Я готов перестать есть сникерсы, ради этого курса",
         "token": "36b4b99", "made_on_datetime": 2424, "author": "ЕlnjnlnlС"},
        {"uuid": "1", "title": "Подготовка к ЕГЭ на Пупоне", "subject": "Инфа",
         "type": "public",
         "description": "Господи, это такой крутой курс. Вам он жизнено необходим. Я готов перестать есть сникерсы, ради этого курса",
         "token": "36b4b99", "made_on_datetime": 2424, "author": "Фёдоров Кирилл Евгеньевич"},
        {"uuid": "2", "title": "Подготовка к ЕГЭ на Пупоне", "subject": "Инфа",
         "type": "public",
         "description": "Господи, это такой крутой курс. Вам он жизнено необходим. Я готов перестать есть сникерсы, ради этого курса",
         "token": "36b4b99", "made_on_datetime": 2424, "author": "ЕmmjnjlnljС"}]

    course = courses[int(id)]

    publications = [{"uuid": "0", "title": "Кейс 2", "text": "Домашка по предпрофу, вы умрете, вы умрете, вы умрете, вы умрете, вы умрете, вы умрете", "made_on_datetime": "432872", "files_folder_path": [("/materials/KE_task3_video1.mp4", "video"), ("/materials/prefixes.pptx", "other"), ("/materials/correct_ip.png", "img")], "type": "courses", "author": "Ф К Е"}, {}, {}]
    return render_template("course.html", title="", id=id, course=course, publications=publications)


@app.route('/profile', methods=['GET', 'POST'])
@app.route('/profile/<name>', methods=['GET', 'POST'])
def profile(name=""):
    user_group = [{"token": "g4d65g", "group_name": "11 класс it"},
                  {"token": "р375gy", "group_name": "10 класс mt"}]

    return render_template("profile.html", title="Личный кабинет",
                           user={'id': '0', 'name': 'Алиса',
                                 'surname': 'Рыбакова', 'lastname': 'Рыбакова',
                                 'email': 'a1@a.com',
                                 'phone_number': '89154559579',
                                 'password': 'qwerty123', 'class_num': 10},
                           user_group=user_group, len=len(user_group))
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
            return render_template("profile.html", title="Личный кабинет",
                                   user=user, user_group=user_group,
                                   len=len(user_group))

    return render_template("profile.html", title="Личный кабинет",
                           user={'id': '0', 'name': 'Алиса',
                                 'surname': 'Рыбакова', 'lastname': 'Рыбакова',
                                 'email': 'a1@a.com',
                                 'phone_number': '89154559579',
                                 'password': 'qwerty123', 'class_num': 10})
    # user_group=user_group, len=len(user_group))


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


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    form = FormAddCourse()
    if form.submit.data == True:
        print(form.type.data)

        return redirect("/")
    return render_template("add_course.html", title="Добавление курса",
                           form=form)


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
    return render_template("add_task.html", title="Добавление задания",
                           form=form)


@app.route('/teacher_groups', methods=['GET', 'POST'])
def teacher_groups():
    courses = [{"id": "0", "num_class": 6, "token": "sh24re"},
               {"id": "1", "num_class": 10, "token": "dfs3y53"},
               {"id": "2", "num_class": 10, "token": "fdj836"}]

    return render_template("teacher_groups.html", courses=courses)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegisterUser()
    if form.submit.data:
        try:
            with open('users.json', 'r') as json_file:
                a = json.load(json_file)
        except ValueError:
            a = {}

        id = str(len(a))

        user = {
            "id": id,
            "name": form.name.data,
            "surname": form.surname.data,
            "lastname": form.lastname.data,
            "email": form.email.data,
            "phone_number": form.phone_number.data,
            "password": form.password.data,
            "class_num": form.class_num.data,
        }

        a[id] = user
        with open("users.json", 'w') as json_file:
            json.dump(a, json_file)

        return redirect('/login')

    return render_template("register.html", title="Регистрация", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLoginUser()
    # if current_user.is_authenticated:
    #     return render_template('index.html', title="")
    if form.submit.data:
        try:
            with open('users.json', 'r') as json_file:
                a = json.load(json_file)
        except ValueError:
            a = {}

        cur_user = form.email.data
        cur_pas = form.password.data
        for i in range(len(a)):
            if a[str(i)]['email'] == cur_user or a[str(i)][
                'email'] == cur_user:
                if a[str(i)]['password'] == cur_pas:
                    return redirect("/profile/" + a[str(i)]['nickname'])
                else:
                    return render_template("login.html", title="Авторизация",
                                           form=form,
                                           message="Неверный пароль")

        return render_template("login.html", title="Авторизация", form=form,
                               message="Такого пользователя не существует")

    return render_template("login.html", title="Авторизация", form=form)


@app.route('/error1', methods=['GET', 'POST'])
def error1():
    return render_template("error.html",
                           err="Такого пользователя не существует")


if __name__ == "__main__":
    # with open("tasks.json", 'w') as json_file:
    # json.dump({}, json_file)
    app.run(port=8080, host="127.0.0.1")
