import datetime
import os
import random
import re
import ssl
import uuid
from os.path import basename
from urllib.parse import urljoin
from urllib.parse import urlparse

import certifi
import requests
from bs4 import BeautifulSoup, Tag, Comment
from werkzeug.utils import secure_filename

from py_scripts.funcs_back import generate_token
from sa_models import db_session
from sa_models.courses import Course
from sa_models.kim_types import KimType
from sa_models.problems import Problem
from sa_models.users import User


def create_kim():
    db_sess = db_session.create_session()

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
    db_sess.close()


def clean_text(text):
    """Очистка текста с сохранением пробелов"""
    text = re.sub(r'[­\xad]', '', text)
    return re.sub(r'[ \t]+', ' ', text).strip()


def html_to_markdown(element, base_url):
    """Конвертация с сохранением структуры"""
    markdown = []
    last_was_block = False

    for child in element.contents:
        if isinstance(child, Comment):
            continue

        if isinstance(child, Tag):
            # Обработка абзацев
            if child.name == 'p':
                content = html_to_markdown(child, base_url).strip()
                if content:
                    if last_was_block:
                        markdown.append('\n\n')
                    markdown.append(f"\n\n{content}\n\n")
                    last_was_block = True

            # Обработка таблиц
            elif child.name == 'table':
                rows = []
                for tr in child.find_all('tr'):
                    cells = [clean_text(td.get_text()) for td in tr.find_all(['td', 'th'])]
                    if cells:
                        rows.append('| ' + ' | '.join(cells) + ' |')

                if rows:
                    separator = '|' + '|'.join(['---'] * (len(rows[0].split('|')) - 2)) + '|'
                    rows.insert(1, separator)
                    table_md = '\n'.join(rows)
                    markdown.append(f"\n\n{table_md}\n\n")
                    last_was_block = True

            # Обработка изображений
            elif child.name == 'img':
                if src := child.get('src'):
                    full_url = urljoin(base_url, src)
                    markdown.append(f"\n\n![]({full_url})\n\n")
                    last_was_block = True

            # Обработка списков
            elif child.name in ['ul', 'ol']:
                list_md = []
                for idx, li in enumerate(child.find_all('li')):
                    content = html_to_markdown(li, base_url).strip()
                    prefix = '- ' if child.name == 'ul' else f'{idx + 1}. '
                    list_md.append(f"{prefix}{content}")
                markdown.append('\n\n' + '\n'.join(list_md) + '\n\n')
                last_was_block = True

            # Обработка переносов строк
            elif child.name == 'br':
                markdown.append('\n\n')
                last_was_block = False

            # Обработка других элементов
            else:
                content = html_to_markdown(child, base_url)
                if child.name == 'b':
                    content = f'**{content}**'
                elif child.name == 'i':
                    content = f'*{content}*'
                markdown.append(' ' + content + ' ')
                last_was_block = False

        # Обработка текста
        elif isinstance(child, str):
            text = clean_text(child)
            if text:
                markdown.append(text.replace('\n', ' '))
                last_was_block = False

    return ''.join(markdown).strip()


def parse_problems(url):
    base_url = "https://inf-ege.sdamgia.ru"
    print('Getting...')
    response = requests.get(url, verify=certifi.where())
    print('Parsing...')
    open('t.html', mode='wb').write(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')
    problems = []

    i = 0
    for block in soup.find_all('div', class_='prob_maindiv'):
        try:
            # Тип задания
            prob_nums = block.find('span', class_='prob_nums')
            task_type = re.search(r'Тип\s*(\d+)', prob_nums.get_text()).group(1)

            # Текст задания
            pbody = block.find('div', class_='pbody')
            task_md = html_to_markdown(pbody, base_url)

            # Материалы
            materials = set()
            for tag in pbody.find_all(['img', 'a']):
                if tag.name == 'img' and (src := tag.get('src')):
                    materials.add(urljoin(base_url, src))
                elif tag.name == 'a' and (href := tag.get('href')):
                    materials.add(urljoin(base_url, href))

            # Источник
            source = None
            if source_a := block.select_one('.attr1 a[href^="/test?id="]'):
                source = clean_text(source_a.get_text())

            # Ответ
            answer = None
            if answer_div := block.find('div', class_='answer'):
                answer_text = clean_text(answer_div.get_text())
                answer = re.search(r'Ответ:\s*([^\s]+)', answer_text).group(1)

            problems.append({
                'type': int(task_type),
                'text': task_md.strip('Ответ:'),
                'materials': list(materials),
                'source': source,
                'answer': answer
            })
        except Exception as e:
            print(f"Ошибка обработки: {e}")
            continue
        print(f'{i} problem parsed')
        i += 1

    return problems


def courses(user_uuid, db_sess):
    arr = [
        {
            'uuid': str(uuid.uuid4()),
            'title': "Подготовка к ЕГЭ по Информатике",
            'subject': 'Информатика',
            'description': 'Подготовка к экспертами ЕГЭ на 100 баллов!',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "PyQT | Создание приложений",
            'subject': 'Промышленная разработка',
            'description': 'Научим разрабатывать собственные оконные приложения на Python',
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
            'title': "Django | Начала бэкенд-разработки",
            'subject': 'Бэкенд',
            'description': 'Начальное погружение в Django',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Структуры данных в C++",
            'subject': 'Алгоритмы',
            'description': 'Подготовка к олимпиадам по олимпиадному программированию',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Администратор Kubernetes",
            'subject': 'DevOps',
            'description': 'Освоение Kubernetes с нуля',
            'token': generate_token(),
            'made_on_datetime': datetime.datetime.now(),
            "user_uuid": user_uuid
        },
        {
            'uuid': str(uuid.uuid4()),
            'title': "Здравствуй, ИИ!",
            'subject': 'Искусственный интеллект',
            'description': 'Введение в линейную алгебру и машинное обучение',
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
            video_url='<iframe width="720" height="405" src="https://rutube.ru/play/embed/3cb648b12534b67cf019b7ec01171d3c/" frameBorder="0" allow="clipboard-write; autoplay" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>'
        )
        db_sess.add(course)
    db_sess.commit()


def create_user(db_sess):
    user = User()
    user.uuid = str(uuid.uuid4())
    user.email = 'example@yandex.ru'
    user.name = "Nikita"
    user.surname = "Mulyar"
    user.username = "nikm"
    user.lastname = "Mikhailovich"
    user.class_number = 11
    user.school = 'Л2Ш'
    user.set_password("1234567a")
    user.access_level = 'user'
    user.phone_number = '89999999999'
    db_sess.add(user)
    db_sess.commit()
    return user.uuid


def main():
    LEVEL = ['Очевидная', 'Очень легкая', 'Легкая', 'Средняя', 'Тяжелая', 'Очень тяжелая', 'Гроб']
    url = "https://inf-ege.sdamgia.ru/test?id=17583978&print=true"
    results = parse_problems(url)

    db_session.global_init('database/portal.db')
    create_kim()
    db_sess = db_session.create_session()
    user_uuid = create_user(db_sess)
    courses(user_uuid, db_sess)

    i = 0
    context = ssl.create_default_context(cafile=certifi.where())

    for problem in results:
        print('Processing', i)
        kim_type = db_sess.query(KimType).where(KimType.kim_id == problem['type']).first()

        if kim_type is None:
            print(f'Skipped', i, problem['type'])
            i += 1
            continue

        new_uuid = str(uuid.uuid4())
        new_problem = Problem()
        new_problem.uuid = new_uuid
        new_problem.text = problem['text']
        new_problem.source = problem['source']
        new_problem.answer = problem['answer']
        new_problem.difficulty = random.choice(LEVEL)
        new_problem.kim_type_uuid = kim_type.uuid

        pth = f'problems_materials/{new_uuid}/'

        for link in problem['materials']:
            try:
                RESPONSE = requests.get(link, verify=certifi.where())
                content_disp = RESPONSE.headers.get("Content-Disposition")

                if content_disp and "filename=" in content_disp:
                    filename = content_disp.split("filename=")[-1].strip('"')
                else:
                    content_type = RESPONSE.headers.get("Content-Type", "unknown")
                    extension = content_type.split("/")[-1].split(";")[0]
                    filename = f"file_{urlparse(url).query.split('=')[-1]}.{extension}"

                filename = secure_filename(basename(filename))

                if not os.path.exists(pth):
                    os.mkdir(pth)
                    new_problem.files_folder_path = pth
                with open(f'problems_materials/{new_uuid}/{filename}', mode='wb') as f:
                    f.write(RESPONSE.content)
            except Exception:
                print(f'Failed file {link}', i)

        db_sess.add(new_problem)
        db_sess.commit()
        i += 1

    db_sess.close()
