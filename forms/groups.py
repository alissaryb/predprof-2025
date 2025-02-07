from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField, widgets
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import InputRequired, DataRequired, Optional, StopValidation


class FormAddGroups(FlaskForm):
    title = StringField('Введите название группы', validators=[InputRequired('Обязательное поле')])
    description = TextAreaField('Введите описание группы', validators=[InputRequired('Обязательное поле')])
    submit = SubmitField('Создать')
