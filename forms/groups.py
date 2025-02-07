from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField, widgets
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import InputRequired, DataRequired, Optional, StopValidation
from flask_wtf.file import FileAllowed, FileRequired


from py_scripts.funcs_back import get_title_courses_by_user_uuid, get_courses_teach

SUBJECTS = ['Информатика', 'Математика', 'Русский язык']


class FormAddGroups(FlaskForm):
    title = StringField('Введите название курса', validators=[InputRequired('Обязательное поле')])
    description = TextAreaField('Введите описание курса', validators=[InputRequired('Обязательное поле')])
    submit = SubmitField('Создать')


