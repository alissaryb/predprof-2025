import datetime

from sa_models import db_session
from sa_models.courses import Course
from sa_models.kim_types import KimType
import uuid

from sa_models.users import User

db_session.global_init('database/portal.db')
db_sess = db_session.create_session()

def generate_token():
    import string
    import random
    s = string.ascii_letters + string.digits
    return ''.join(random.choice(s) for _ in range(6))


def kim():
    arr = [
        ('1. Анализ информационных моделей', 1, 1),
        ('2. Таблицы истинности логических выражений', 2, 1),
        ('3. Поиск и сортировка в базах данных', 3, 1),
        ('4. Кодирование и декодирование данных. Условие Фано', 4, 1),
        ('5. Анализ алгоритмов для исполнителей', 5, 1),
        ('6. Циклические алгоритмы для Исполнителя', 6, 1),
        ('7. Кодирование графической и звуковой информации', 7, 1),
        ('8. Комбинаторика', 8, 1),
        ('9. Обработка числовой информации в электронных таблицах', 9, 1),
        ('10. Поиск слова в текстовом документе', 10, 1),
        ('11. Вычисление количества информации', 11, 1),
        ('12. Алгоритмы для исполнителей с циклами и ветвлениями', 12, 1),
        ('13. IP адреса и маски', 13, 1),
        ('14. Позиционные системы счисления', 14, 1),
        ('15. Истинность логического выражения', 15, 1),
        ('16. Вычисление значения рекурсивной функции', 16, 1),
        ('17. Обработка целочисленных данных. Проверка делимости', 17, 1),
        ('18. Динамическое программирование в электронных таблицах', 18, 1),
        ('19-21. Теория игр', 19, 1),
        ('22. Многопоточные вычисления', 22, 1),
        ('23. Динамическое программирование (количество программ)', 23, 1),
        ('24. Обработка символьных строк', 24, 1),
        ('25. Обработка целочисленных данных. Поиск делителей', 25, 1),
        ('26. Обработка данных с помощью сортировки', 26, 2),
        ('27. Анализ данных', 27, 2)
    ]

    for i in arr:
        kt = KimType()
        kt.title = i[0]
        kt.kim_id = i[1]
        kt.uuid = str(uuid.uuid4())
        kt.points = i[2]
        db_sess.add(kt)
    db_sess.commit()
def courses(user_uuid):
    arr = [
        {
            'uuid': str(uuid.uuid4()),
            'title': "Ассинхронность в Python",
            'subject': 'Программирование',
            'description': 'Первый курс по ассинхронному программированиию на Python',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid":user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Полный курс по React",
            'subject': 'Фронтенд',
            'description': 'Добро пожаловать в Боль и СТРАДАНИЯ',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Excel - Базовый уровень",
            'subject': 'Информатика',
            'description': 'Начальное погружение в Excel',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Backend разработка на Django",
            'subject': 'Backend',
            'description': 'Начальное погружение в Django',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "SQL-практикум",
            'subject': 'Базы данных',
            'description': 'Начальное погружение в SQL',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Администратор Kubernetes",
            'subject': 'Devops',
            'description': 'Освоение Kubernetes с нуля',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Здравствуй, ИИ! Первый курс",
            'subject': 'Искусственный интеллект',
            'description': 'Первое освоение ИИ',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Кумир для самых маленьких",
            'subject': 'Информатика',
            'description': 'Начнем программировать еще школьниками!',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
    ]
    for el in arr:
        course = Course(
            uuid=el['uuid'],
            title=el['title'],
            subject=el['subject'],
            description=el['description'],
            token=el['token'],
            made_on_datetime=el['made_on_datetime'],
            user_uuid=el['user_uuid'],
            video_url='<iframe width="720" height="405" src="https://rutube.ru/play/embed/8ac7d1439fcfddb601bec871059a09d6/" frameBorder="0" allow="clipboard-write; autoplay" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>'
        )
        db_sess.add(course)
    db_sess.commit()
def new_user():
    user = User()
    user.uuid = str(uuid.uuid4())
    user.email = 'example@yandex.ru'
    user.name = "Matthew"
    user.surname = "Matthew"
    user.username = "Hellow"
    user.lastname = "Hellowich"
    user.class_number = 11
    user.school = '112'
    user.set_password("q1w2e3r4")
    user.access_level = 'user'
    user.phone_number = '89999999999'
    db_sess.add(user)
    db_sess.commit()
    return user.uuid



new_user_uuid = new_user()
# kim()
courses(new_user_uuid)

db_sess.close()
