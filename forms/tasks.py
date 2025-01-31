from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, BooleanField, FieldList, FormField
from wtforms.validators import InputRequired, NumberRange


LEVEL = ['Для овощей', 'Очень легкая', 'Легкая', 'Средняя', 'Тяжелая', 'Очень тяжелая', 'Гроб']


class FormAddTask(FlaskForm):
    type = IntegerField('Введите тип задания', validators=[InputRequired('Обязательное поле'), NumberRange(min=1, max=27)])
    source = StringField('Введите источник задачи')
    task = TextAreaField('Введите условие задачи', validators=[InputRequired('Обязательное поле')])
    ans = StringField('Введите ответ задачи', validators=[InputRequired('Обязательное поле')])
    level = SelectField('Выбирите сложность задачи', choices=LEVEL, validators=[InputRequired('Обязательное поле')])
    submit = SubmitField('Добавить')


class QuizForm(FlaskForm):
    show_answer = BooleanField('Показать ответы')
    submit = SubmitField('Проверить')
