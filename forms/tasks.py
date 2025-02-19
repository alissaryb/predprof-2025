from optparse import Option

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, BooleanField, FileField, FieldList, FormField
from wtforms.validators import InputRequired, NumberRange, DataRequired, Optional

LEVEL = ['Очевидная', 'Очень легкая', 'Легкая', 'Средняя', 'Тяжелая', 'Очень тяжелая', 'Гроб']
TYPE = ["1. Анализ информационных моделей", "2. Таблицы истинности логических выражений", "3. Поиск и сортировка в базах данных",
        "4. Кодирование и декодирование данных. Условие Фано", "5. Анализ алгоритмов для исполнителей", "6. Циклические алгоритмы для Исполнителя",
        "7. Кодирование графической и звуковой информации", "8. Комбинаторика", "9. Обработка числовой информации в электронных таблицах",
        "10. Поиск слова в текстовом документе", "11. Вычисление количества информации", "12. Алгоритмы для исполнителей с циклами и ветвлениями",
        "13. IP адреса и маски", "14. Позиционные системы счисления", "15. Истинность логического выражения",
        "16. Вычисление значения рекурсивной функции", "17. Обработка целочисленных данных. Проверка делимости", "18. Динамическое программирование в электронных таблицах",
        "19-21. Теория игр", "22. Многопоточные вычисления", "23. Динамическое программирование (количество программ)", "24. Обработка символьных строк",
        "25. Обработка целочисленных данных. Поиск делителей", "26. Обработка данных с помощью сортировки", "27. Анализ данных"]

class FormAddTask(FlaskForm):
    type = SelectField('Введите тип задания', choices=TYPE, validators=[InputRequired('Обязательное поле')])
    source = StringField('Введите источник задачи')
    task = TextAreaField('Введите условие задачи', validators=[InputRequired('Обязательное поле')])
    ans = StringField('Введите ответ задачи', validators=[InputRequired('Обязательное поле')])
    level = SelectField('Выбирите сложность задачи', choices=LEVEL, validators=[InputRequired('Обязательное поле')])
    files = FileField('Прикрепите файлы к заданию', validators=[Optional()], render_kw={"multiple": True})
    submit = SubmitField('Добавить')


class QuizForm(FlaskForm):
    show_answer = BooleanField('Показать ответы')
    submit = SubmitField('Проверить')
