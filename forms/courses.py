from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, BooleanField, FieldList, FormField, RadioField
from wtforms.validators import InputRequired, NumberRange, DataRequired


SUBJECTS = ['Информатика', 'Математика', 'Русский язык']


class FormAddCourse(FlaskForm):
    title = StringField('Введите название курса', validators=[InputRequired('Обязательное поле')])
    description = TextAreaField('Введите описание курса', validators=[InputRequired('Обязательное поле')])
    subject = SelectField('Введите предмет изучения', choices=SUBJECTS,
                          validators=[DataRequired('Обязательное поле')])

    submit = SubmitField('Создать')


class FormAddPublication(FlaskForm):
    title = StringField('Название публикации', validators=[InputRequired('Обязательное поле')])
    text = TextAreaField('Текст публикации', validators=[InputRequired('Обязательное поле')])
    my_courses = SelectField('Категория', choices=[], validators=[InputRequired('Выберите категорию')])

    submit = SubmitField('Опубликовать')
