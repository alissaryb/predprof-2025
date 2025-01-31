from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, SelectField
from wtforms.validators import InputRequired, DataRequired, ValidationError, Length, Regexp
import re
import email_validator


classes = [str(i) for i in range(1, 12)]


def password_complexity(form, field):
    if not re.search(r"[A-Za-z]", field.data):
        raise ValidationError("Пароль должен содержать хотя бы одну букву.")
    if not re.search(r"[0-9]", field.data):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")


def passwords_match(form, field):
    if field.data != form.password.data:
        raise ValidationError("Пароли не совпадают")


def email_match(form, field):
    try:
        email_validator.validate_email(field.data, check_deliverability=True)
    except Exception:
        raise ValidationError("Некорректный адрес эл. почты")


class FormRegisterUser(FlaskForm):
    username = StringField('Придумайте себе никнейм', validators=[DataRequired('Обязательное поле'),
                                                                  Length(min=3)])
    email = EmailField('Введите адрес эл. почты', validators=[DataRequired('Обязательное поле'),
                                                              email_match])
    surname = StringField('Введите фамилию', validators=[DataRequired('Обязательное поле')])
    name = StringField('Введите имя', validators=[DataRequired('Обязательное поле')])
    lastname = StringField('Введите отчество', validators=[DataRequired('Обязательное поле')])
    class_num = SelectField('Выберите класс', choices=['Не выбрано', 'Учитель'] + classes)
    school = StringField('Напишите название вашей школы')
    phone_number = StringField('Введите номер телефона',
                               validators=[InputRequired('Обязательное поле'),
                                           Regexp(r'^(?:\+7\d{10}|8\d{10})$',
                                                  message="Номер телефона должен быть в формате "
                                                          "+7xxxxxxxxxx или 8xxxxxxxxxx.")])

    password = PasswordField('Введите пароль', validators=[DataRequired('Обязательное поле'),
                                                           Length(min=8), password_complexity])
    password_check = PasswordField('Повторите пароль', validators=[DataRequired('Обязательное поле'),
                                                                   Length(min=8), passwords_match])

    submit = SubmitField('Зарегистрироваться')


class FormLoginUser(FlaskForm):
    email_or_username = StringField('Введите адрес эл. почты или никнейм',
                                    validators=[DataRequired('Обязательное поле')])
    password = PasswordField('Пароль', validators=[DataRequired('Обязательное поле')])

    submit = SubmitField('Войти')
