from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, DateField, EmailField, \
    PasswordField, URLField, TimeField, RadioField, BooleanField, SelectMultipleField, SelectField, FileField
from wtforms.validators import InputRequired, DataRequired, ValidationError, \
    Length, Regexp
from wtforms.widgets import CheckboxInput
import re

CLASSES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

def password_complexity(form, field):
    if not re.search(r"[A-Za-z]", field.data):
        raise ValidationError("Пароль должен содержать хотя бы одну букву.")
    if not re.search(r"[0-9]", field.data):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")


def passwords_match(form, field):
    if field.data != form.password.data:
        raise ValidationError("Пароли не совпадают")


class FormRegisterUser(FlaskForm):
    name = StringField('Введите имя', validators=[DataRequired('Обязательное поле')])
    surname = StringField('Введите фамилию', validators=[DataRequired('Обязательное поле')])
    lastname = StringField('Введите отчество', validators=[InputRequired()])

    email = EmailField('Введите адрес эл. почты', validators=[DataRequired('Обязательное поле')])
    phone_number = StringField('Введите номер телефона', validators=[InputRequired('Обязательное поле'), Regexp(r'^(?:\+7\d{10}|8\d{10})$', message="Номер телефона должен быть в формате +7xxxxxxxxxx или 8xxxxxxxxxx.")])

    password = PasswordField('Введите пароль', validators=[DataRequired(), Length(min=8), password_complexity])
    password_check = PasswordField('Повторите пароль', validators=[DataRequired('Обязательное поле'), Length(min=8), passwords_match])

    class_num = SelectField('Класс обучения', choices=CLASSES, validators=[DataRequired('Обязательное поле')])

    submit = SubmitField('Регистрация')
    reset = SubmitField('Сбросить')


class FormLoginUser(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('Введите адрес эл. почты', validators=[DataRequired('Обязательное поле')])

    submit = SubmitField('Войти')
    reset = SubmitField('Сбросить')
