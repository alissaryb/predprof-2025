from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, BooleanField, FieldList, FormField, RadioField
from wtforms.validators import InputRequired, NumberRange, DataRequired

SUBJECT = ['Английский', 'Астрономия', 'Биология', 'География', 'Информатика', 'История ', 'Литература', 'Математика', 'Обществознание', 'Русский язык', 'Физика', 'Химия']

class FormAddCourse(FlaskForm):
    title = StringField('Введите название курса', validators=[InputRequired('Обязательное поле')])
    subject = SelectField('Введите предмет изучения', choices=SUBJECT, validators=[DataRequired('Обязательное поле')])
    description = TextAreaField('Введите описание курса', validators=[InputRequired('Обязательное поле')])

    submit = SubmitField('Добавить')


class FormAddPublication(FlaskForm):
    title = StringField('Название публикации', validators=[InputRequired('Обязательное поле')])
    text = TextAreaField('Текст публикации', validators=[InputRequired('Обязательное поле')])
    my_courses = SelectField('Категория', choices=[], validators=[InputRequired('Выберите категорию')])

    submit = SubmitField('Опубликовать')