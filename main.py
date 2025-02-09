#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
from functools import wraps

from flask import Flask, render_template, request, redirect, send_from_directory, session, url_for
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename

from forms.groups import FormAddGroups
from forms.register import FormRegisterUser, FormLoginUser
from forms.tasks import FormAddTask, QuizForm
from forms.courses import FormAddCourse, FormAddLesson

import json
import uuid
import markdown2

from py_scripts.funcs_back import get_user_data, add_lesson_database, get_kim_dict, get_tasks
from py_scripts.funcs_back import get_user_data,  get_kim_dict, get_tasks, make_variant_to_db, \
    tasks_by_test_uuid, get_variants_by_user_uuid
from sa_models import db_session
from sa_models.course_to_lesson import CourseToLesson
from sa_models.group_to_user import GroupToUser
from sa_models.groups import Group
from sa_models.lessons import Lesson
from sa_models.test_results import Test_result
from sa_models.users import User
from sa_models.courses import Course
from sa_models.problems import Problem
from sa_models.kim_types import KimType
from sa_models.course_to_user import CourseToUser
from py_scripts import funcs_back, consts



if not os.path.exists('problems_materials/'):
    os.mkdir('problems_materials/')
if not os.path.exists('lessons_materials/'):
    os.mkdir('lessons_materials/')
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


@app.errorhandler(401)
def e401(code):
    return redirect('/login')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="")


@app.route('/lessons_materials/<material_uuid>/<filename>', methods=['GET'])
def download_file_lesson(material_uuid, filename):
    return send_from_directory(f'lessons_materials/{material_uuid}', filename)


@app.route('/problems_materials/<material_uuid>/<filename>', methods=['GET'])
def download_file_problem(material_uuid, filename):
    return send_from_directory(f'problems_materials/{material_uuid}', filename)


@app.route('/random_work', methods=['GET', 'POST'])
@login_required
def random_work():
    data = get_kim_dict()
    session.pop("tasks", None)
    session.pop("results", None)
    return render_template("random_work.html", data=data)


@app.route('/work', methods=['GET', 'POST'])
@login_required
def work():
    if 'submit_answers' not in request.form and "results" in session:
        session["results"].clear()
    if request.method == 'POST':
        if 'tasks' not in session:
            form_data = dict()
            for key, val in request.form.to_dict().items():
                form_data[key.split("_")[1]] = int(val)
            tasks = get_tasks(form_data)
            session['tasks'] = tasks
        if 'submit_answers' in request.form:
            correct_count = 0
            all_count = 0
            total_score = 0
            all_score = 0
            results = list()
            db_sess = db_session.create_session()

            for el in session['tasks']:
                kim_title = el["key"][0]
                kim_uuid = el["key"][1]
                points = db_sess.query(KimType).where(kim_uuid == KimType.uuid).first().points
                results.append({
                    "key": (kim_title, kim_uuid),
                    "value": list()})
                for task in el["value"]:
                    user_answer = request.form.get(f"answer_{kim_uuid}_{task['uuid']}", "").strip()
                    is_correct = (user_answer.lower() == task['answer'].lower())

                    if is_correct:
                        correct_count += 1
                        total_score += points
                    all_count += 1
                    all_score += points
                    results[-1]["value"].append(
                        {**task, 'user_answer': user_answer, 'is_correct': is_correct})

                    session['results'] = results
                    session['correct_count'] = correct_count
                    session['total_score'] = total_score
                    session['all_count'] = all_count
                    session['all_score'] = all_score

    tasks = session.get('results') if session.get("results") else session.get("tasks")
    results = bool(session.get("results"))
    correct_count = session.get('correct_count')
    total_score = session.get('total_score')
    all_score = session.get("all_score")
    all_count = session.get("all_count")
    print(tasks)
    for i in range(len(tasks)):
        print(tasks[i])
        print()



    print(results)
    print(correct_count)
    print(total_score)
    print(all_score)
    print(all_count)

    return render_template('work2.html',
                           tasks=session.get('results') if session.get("results") else session.get("tasks"),
                           results=bool(session.get("results")),
                           correct_count=session.get('correct_count'),
                           total_score=session.get('total_score'),
                           all_score=session.get("all_score"),
                           all_count=session.get("all_count"))


@login_required
@app.route('/profile', methods=['GET'])
def profile():
    user_data = get_user_data(current_user)
    return render_template("profile.html", title="Личный кабинет", user=user_data)


@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    arr = {1: {"correct": 10, "all": 23}, 2: {"correct": 15, "all": 15},
           3: {"correct": 1, "all": 20}, 4: {"correct": 34, "all": 100},
           5: {"correct": 22, "all": 37}, 6: {"correct": 16, "all": 56}}
    d = [i for i in range(1, len(arr) + 1)]

    for i in d:
        p = arr[i]['correct'] / arr[i]['all'] * 100
        arr[i]['pr'] = p
    print(arr)

    values = [10, 70, 34, 52, 25, 88]
    return render_template("statistic.html", arr=arr, d=d, values=values)


@app.route('/group/<group_uuid>/invite', methods=['GET'])
@login_required
def group_invite(group_uuid):
    db_sess = db_session.create_session()

    group = db_sess.query(Group).where(Group.uuid == group_uuid).first()

    if group is None:
        db_sess.close()
        return render_template("error.html", title="Группа не найдена", err='Курс не найдена')

    is_registered = db_sess.query(GroupToUser).where(GroupToUser.user_uuid == current_user.uuid,
                                                      GroupToUser.group_uuid == group_uuid).first()
    is_author = group.author.uuid == current_user.uuid

    if is_author or is_registered:
        db_sess.close()
        return redirect(f'page_group/{group_uuid}')

    new_relation = GroupToUser(user_uuid=current_user.uuid, group_uuid=group_uuid)
    db_sess.add(new_relation)
    db_sess.commit()
    db_sess.close()
    return redirect(f'/page_group/{group_uuid}')


@app.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():
    form = FormAddGroups()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        new_uuid = str(uuid.uuid4())
        new_group = Group()
        new_group.title = form.title.data
        new_group.description = form.description.data
        new_group.uuid = new_uuid
        new_group.token = funcs_back.generate_token()
        new_group.user_uuid = current_user.uuid

        db_sess.add(new_group)
        db_sess.commit()

        db_sess.close()

        return redirect(f"/page_group/{new_uuid}")

    return render_template("add_group.html", title="Создание группы", form=form)


@app.route('/my_groups', methods=['GET'])
@login_required
def my_groups():
    student_groups = funcs_back.get_groups_learn(current_user.uuid)
    teacher_groups = funcs_back.get_groups_teach(current_user.uuid)

    return render_template("my_groups.html", teacher_groups=teacher_groups,
                           student_groups=student_groups, title="Мои группы")


@app.route('/page_group/<group_uuid>', methods=['GET'])
@login_required
def group_by_uuid(group_uuid):
    db_sess = db_session.create_session()

    group = db_sess.query(Group).where(Group.uuid == group_uuid).first()

    if group is None:
        db_sess.close()
        return render_template("error.html", title="Группа не найдена", err='Группа не найдена')

    is_registered = db_sess.query(GroupToUser).where(GroupToUser.group_uuid == group_uuid,
                                                      GroupToUser.user_uuid == current_user.uuid).first()

    is_author = group.author.uuid == current_user.uuid
    if is_registered is None and not is_author:
        db_sess.close()
        return render_template("error.html", title="Группа не найдена", err='Группа не найдена')

    group_data = {
        'title': group.title,
        'link': f'/group/{group_uuid}/invite',
        'description': group.description,
        'author': f'{group.author.surname} {group.author.name[0]}. {group.author.lastname[0]}.',
        'made_on_datetime': f'{group.made_on_datetime.strftime('%d.%m.%Y')} в 'f'{group.made_on_datetime.strftime('%H:%M')}',
        'members_group': []
    }

    for relation in group.users:
        member = relation.user
        d = {
            'uuid': member.uuid,
            'email': member.email,
            'username': member.username,
            'fio': f'{member.surname} {member.name} {member.lastname}',
            'school': member.school,
            'class_num': member.class_number
        }
        group_data['members_group'].append(d)

    db_sess.close()
    print(group_data)

    return render_template("page_group.html", title="Страница группы", group=group_data)


@app.route(f'/page_course/<course_uuid>/page_lesson/<lesson_uuid>', methods=['GET'])
@login_required
def lesson_page(course_uuid, lesson_uuid):
    db_sess = db_session.create_session()

    exists = db_sess.query(CourseToLesson).where(CourseToLesson.course_uuid == course_uuid,
                                                 CourseToLesson.lesson_uuid == lesson_uuid).first()

    if exists is None:
        db_sess.close()
        return render_template("error.html", title="Курс или урок не найдены",
                               err='Курс или урок не найдены')

    course_uuid = exists.course_uuid
    is_author = exists.course.author.uuid == current_user.uuid
    is_registered = db_sess.query(CourseToUser).where(CourseToUser.user_uuid == current_user.uuid,
                                                      CourseToUser.course_uuid == course_uuid).first()

    if not is_author and is_registered is None:
        db_sess.close()
        return render_template("error.html", title="Вы не зарегистрированы на курс",
                               err='Вы не зарегистрированы на курс')

    markdowner = markdown2.Markdown(extras=['fenced-code-blocks', 'highlightjs-lang', 'latex', "language-prefix",
    "tables"])

    lesson = exists.lesson
    lesson_data = {
        'course_uuid': course_uuid,
        'lesson_uuid': lesson_uuid,
        'title': lesson.title,
        'description': lesson.description,
        'text': markdowner.convert(lesson.text),
        'author': f'{lesson.author.surname} {lesson.author.name[0]}. {lesson.author.lastname[0]}.',
        'made_on_datetime': f'{lesson.made_on_datetime.strftime('%d.%m.%Y')} в 'f'{lesson.made_on_datetime.strftime('%H:%M')}',
        'files_folder_path': []
    }

    if lesson.files_folder_path is not None:
        for file_ in os.listdir(lesson.files_folder_path):
            path_ = [f'/{lesson.files_folder_path}{file_}', 'other']
            if file_.endswith('.png') or file_.endswith('.jpeg') or file_.endswith('.jpg') or file_.endswith(
                    '.webp') or \
                    file_.endswith('.gif'):
                path_[1] = 'img'
            if file_.endswith('.mp4') or file_.endswith('.mov') or file_.endswith('.wmv') or file_.endswith('.mkv'):
                path_[1] = 'video'
            lesson_data['files_folder_path'].append(path_)

    files = lesson_data['files_folder_path']
    return render_template("page_lesson.html", lesson=lesson_data, files=files)


@app.route('/add_lesson', methods=['GET', 'POST'])
@login_required
def add_lesson():
    form = FormAddLesson(current_user.uuid)
    if form.validate_on_submit():
        files = request.files.getlist("files")
        lesson_text = request.files.get("lesson_file").stream.read().decode("utf8")
        add_lesson_database(form, current_user.uuid, files, lesson_text)

        return redirect("/my_courses")

    return render_template("add_publication.html", form=form,
                           title="Создание урока")


@app.route('/practice', methods=['GET'])
@login_required
def practice():
    db_sess = db_session.create_session()

    all_tasks = db_sess.query(Problem).all()
    markdowner = markdown2.Markdown(extras=['fenced-code-blocks', 'highlightjs-lang', 'latex', "language-prefix",
    "tables"])

    problems = []
    for problem in all_tasks:
        data = {
            'level': problem.difficulty,
            'num_type': problem.kim_type.kim_id,
            'text_type': problem.kim_type.title,
            'source': problem.source,
            'uuid': problem.id,
            'text': markdowner.convert(problem.text),
            'ans': problem.answer,
            'files_folder_path': []
        }

        if problem.files_folder_path is not None:
            for file_ in os.listdir(problem.files_folder_path):
                path_ = [f'/{problem.files_folder_path}{file_}', 'other']
                if file_.endswith('.png') or file_.endswith('.jpeg') or file_.endswith('.jpg') or file_.endswith(
                        '.webp') or \
                        file_.endswith('.gif'):
                    path_[1] = 'img'
                if file_.endswith('.mp4') or file_.endswith('.mov') or file_.endswith('.wmv') or file_.endswith('.mkv'):
                    path_[1] = 'video'
                data['files_folder_path'].append(path_)
            data['files_folder_path'] = sorted(data['files_folder_path'], key=lambda x: (x[1] != 'other', x))
        problems.append(data)

    for i in problems:
        print(i)
        print()

    return render_template("practice.html", title="", tasks=problems)


@app.route('/add_work', methods=['GET'])
@login_required
def add_work():
    db_sess = db_session.create_session()

    all_tasks = db_sess.query(Problem).all()

    problems = []
    for problem in all_tasks:
        data = {
            'level': problem.difficulty,
            'num_type': problem.kim_type.kim_id,
            'text_type': problem.kim_type.title,
            'source': problem.source,
            'uuid': problem.id,
            'text': problem.text.replace('\n', '<br>'),
            'ans': problem.answer,
            'files_folder_path': []
        }

        if problem.files_folder_path is not None:
            for file_ in os.listdir(problem.files_folder_path):
                path_ = [f'/{problem.files_folder_path}{file_}', 'other']
                if file_.endswith('.png') or file_.endswith('.jpeg') or file_.endswith('.jpg') or file_.endswith(
                        '.webp') or \
                        file_.endswith('.gif'):
                    path_[1] = 'img'
                if file_.endswith('.mp4') or file_.endswith('.mov') or file_.endswith('.wmv') or file_.endswith('.mkv'):
                    path_[1] = 'video'
                data['files_folder_path'].append(path_)
            data['files_folder_path'] = sorted(data['files_folder_path'], key=lambda x: (x[1] != 'other', x))
        problems.append(data)

    feedback = {1: 'Полная', 2: 'Частичная', 3: 'Только баллы', 4: 'Отсутствие обратной связи'}

    return render_template("add_work.html", title="", tasks=problems, feedback=feedback)


@login_required
@app.route('/make_variant', methods=['POST'])
def make_variant():
    selected = request.form.getlist('test_tasks')
    if not selected and request.form.get("button"):
        selected = request.form.get("button").split(";")
    test_uuid = make_variant_to_db(selected, current_user.uuid, request.form.get('title'))
    return redirect(url_for('test_page', test_uuid=test_uuid, feedback=request.form.get('option')))

@login_required
@app.route('/test/<test_uuid>', methods=['GET', 'POST'])
def test_page(test_uuid):
    feedback = int(request.args.get('feedback', 0))
    tasks = tasks_by_test_uuid(test_uuid)
    kwargs = dict()
    kwargs['result'] = 0
    kwargs['feedback'] = feedback
    if request.method == 'POST':
        kwargs['correct_count'] = kwargs['total_score'] = kwargs['all_count'] = kwargs['all_score'] = 0
        db_sess = db_session.create_session()

        for ind, task in enumerate(tasks):
            kim_uuid = task["key"][1]
            points = db_sess.query(KimType).where(kim_uuid == KimType.uuid).first().points

            user_answer = request.form.get(f"answer_{kim_uuid}_{task['value']['uuid']}", "").strip()
            is_correct = (user_answer.lower() == task['value']['answer'].lower())

            if is_correct:
                kwargs['correct_count'] += 1
                kwargs['total_score'] += points
            kwargs['all_count'] += 1
            kwargs['all_score'] += points
            tasks[ind]['value']['user_answer'] = user_answer
            tasks[ind]['value']['is_correct'] = is_correct
        kwargs['result'] = 1


        test_result = Test_result(
            test_variant_uuid=test_uuid,
            user_uuid=current_user.uuid,
            res_scores=kwargs['total_score'],
            max_scores=kwargs['all_score']
        )
        db_sess.add(test_result)
        db_sess.commit()
        db_sess.close()
    return render_template('work3.html', title='Вариант', tasks=tasks, **kwargs)

@app.route('/my_variants')
@login_required
def my_variants():
    variants = get_variants_by_user_uuid(current_user.uuid)
    return render_template("my_variants.html", variants=variants)



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

        files = request.files.getlist("files")
        if len(files) > 0:
            for file in files:
                print(file)
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

    return render_template("add_task.html", title="Добавление задания", form=form)


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

    is_author = course.author.uuid == current_user.uuid
    if is_registered is None and not is_author:
        new_relation = CourseToUser()
        new_relation.user_uuid = current_user.uuid
        new_relation.course_uuid = course_uuid
        db_sess.add(new_relation)
        db_sess.commit()
        db_sess.close()
        return redirect(f'/page_course/{course_uuid}')

    course_data = {
        'uuid': course_uuid,
        'title': course.title,
        'subject': course.subject,
        'description': course.description,
        'token': course.token,
        'made_on_datetime': f'{course.made_on_datetime.strftime('%d.%m.%Y')} в 'f'{course.made_on_datetime.strftime('%H:%M')}',
        'author': f'{course.author.surname} {course.author.name[0]}. {course.author.lastname[0]}.',
        'author_uuid': course.author.uuid,
        'iframe': course.video_url
    }

    all_tags = []
    lessons = []
    course_lessons = course.lessons
    for note_ in course_lessons:
        note = note_.lesson
        note_data = {
            'uuid': note.uuid,
            'title': note.title,
            'description': note.description,
            'made_on_datetime': f'{note.made_on_datetime.strftime('%d.%m.%Y')} в '
                                f'{note.made_on_datetime.strftime('%H:%M')}',
            'tag': ', '.join([i.strip().lower() for i in note.tag.split(',')]),
            'SORT_KEY': note.made_on_datetime
        }
        all_tags.append(note_data['tag'])
        lessons.append(note_data)

    lessons = sorted(lessons, key=lambda x: x['SORT_KEY'], reverse=True)
    db_sess.close()

    return render_template("page_course.html", title="Страница курса", course=course_data,
                           lessons=lessons)


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
        new_course.video_url = form.video_url.data
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
    courses_data_by_uuid = {}
    for course in all_:
        courses_data_by_uuid[course.uuid] = False

    if current_user.is_authenticated:
        registered_courses_uuids = (funcs_back.get_courses_teach(current_user.uuid) +
                                    funcs_back.get_courses_learn(current_user.uuid))
        for course in registered_courses_uuids:
            courses_data_by_uuid[course['uuid']] = True

    courses = []
    for course in all_:
        d = {
            'title': course.title,
            'subject': course.subject,
            'token': course.token,
            'description': course.description,
            'author': f'{course.author.surname} {course.author.name[0]}. {course.author.lastname[0]}.',
            'made_on_datetime': f'{course.made_on_datetime.strftime('%d.%m.%Y')} в '
                                f'{course.made_on_datetime.strftime('%H:%M')}',
            'uuid': course.uuid,
            'author_uuid': course.author.uuid
        }
        courses.append(d)

    db_sess.close()

    return render_template("all_courses.html", title="Каталог курсов", courses=courses,
                           courses_data_by_uuid=courses_data_by_uuid)


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
        user.email = form.email.data.lower()
        user.name = form.name.data.lower().capitalize()
        user.surname = form.surname.data.lower().capitalize()
        user.username = form.username.data
        user.lastname = form.lastname.data.lower().capitalize()
        user.class_number = form.class_num.data if form.class_num.data != 'Учитель' else None
        user.school = form.school.data
        user.set_password(form.password.data)
        user.access_level = 'user' if form.class_num.data != 'Учитель' else 'teacher'
        user.phone_number = form.phone_number.data
        db_sess.add(user)
        db_sess.commit()

        db_sess.close()

        return redirect('/login')

    return render_template("register.html", title="Регистрация", form=form)


@app.route('/login', methods=['GET', 'POST'])
@login_forbidden
def login():
    form = FormLoginUser()
    if form.validate_on_submit():
        email_or_username = form.email_or_username.data
        psw = form.password.data
        db_sess = db_session.create_session()

        exists = db_sess.query(User).where(User.email == email_or_username.lower()).first()
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
    app.run(port=consts.PORT, host=consts.HOST, threaded=True)
