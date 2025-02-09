import os
import random
import ssl
import uuid

import certifi
import cloudscraper
import requests
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag, Comment
from urllib.parse import urljoin
from werkzeug.utils import secure_filename
from os.path import basename

from sa_models import db_session
from sa_models.problems import Problem
from sa_models.kim_types import KimType


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


if __name__ == "__main__":
    LEVEL = ['Очевидная', 'Очень легкая', 'Легкая', 'Средняя', 'Тяжелая', 'Очень тяжелая', 'Гроб']
    url = "https://inf-ege.sdamgia.ru/test?id=17583978&print=true"
    results = parse_problems(url)

    db_session.global_init('database/portal.db')
    db_sess = db_session.create_session()

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
