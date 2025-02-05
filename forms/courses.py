from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import InputRequired, DataRequired, Optional

from py_scripts.funcs_back import get_title_courses_by_user_uuid

SUBJECTS = ['Информатика', 'Математика', 'Русский язык']


class FormAddCourse(FlaskForm):
    title = StringField('Введите название курса', validators=[InputRequired('Обязательное поле')])
    description = TextAreaField('Введите описание курса', validators=[InputRequired('Обязательное поле')])
    subject = SelectField('Введите предмет изучения', choices=SUBJECTS,
                          validators=[DataRequired('Обязательное поле')])

    submit = SubmitField('Создать')


class FormAddPublication(FlaskForm):
    title = StringField('Название публикации', validators=[InputRequired('Обязательное поле')])
    text = TextAreaField('Текст публикации', validators=[])
    my_courses = SelectField('Категория', choices=[current_user.courses if current_user else "Нет курсов"],
                             validators=[InputRequired('Выберите категорию')])
    files = FileField('Выберите файлы', validators=[Optional()], render_kw={"multiple": True})

    submit = SubmitField('Опубликовать')

    def __init__(self, user_uuid, *args, **kwargs):
        super(FormAddPublication, self).__init__(*args, **kwargs)
        self.my_courses.choices = get_title_courses_by_user_uuid(user_uuid)
