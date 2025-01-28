from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, BooleanField, FieldList, FormField, RadioField
from wtforms.validators import InputRequired, NumberRange, DataRequired

SUBJECT = ['Английский', 'Астрономия', 'Биология', 'География', 'Информатика', 'История ', 'Литература', 'Математика', 'Обществознание', 'Русский язык', 'Физика', 'Химия']

class FormAddCourse(FlaskForm):
    cours_name = StringField('Введите название курса', validators=[InputRequired('Обязательное поле')])
    description = TextAreaField('Введите описание курса', validators=[InputRequired('Обязательное поле')])
    subject = SelectField('Введите предмет изучения', choices=SUBJECT, validators=[DataRequired('Обязательное поле')])

    type = RadioField('Выберите опцию', choices=[('presentation', 'Презентация'), ('video', 'Видео'), ('metodichka', 'Методические материалы')], validators=[InputRequired('Обязательное поле')])
    link = StringField('Введите ссылку на учебный материал', validators=[InputRequired('Обязательное поле')])
    submit = SubmitField('Добавить')
