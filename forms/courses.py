from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField, widgets
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import InputRequired, DataRequired, Optional, StopValidation

from py_scripts.funcs_back import get_title_courses_by_user_uuid, get_courses_teach

SUBJECTS = ['Информатика', 'Математика', 'Русский язык']


class FormAddCourse(FlaskForm):
    title = StringField('Введите название курса', validators=[InputRequired('Обязательное поле')])
    description = TextAreaField('Введите описание курса', validators=[InputRequired('Обязательное поле')])
    subject = SelectField('Введите предмет изучения', choices=SUBJECTS,
                          validators=[DataRequired('Обязательное поле')])

    submit = SubmitField('Создать')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultiCheckboxAtLeastOne():
    def __init__(self, message=None):
        if not message:
            message = 'Должен быть выбран хотя бы один курс'
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)


class FormAddPublication(FlaskForm):
    title = StringField('Название публикации', validators=[InputRequired('Обязательное поле')])
    tag = StringField('Напишите ключевые слова через запятую', validators=[InputRequired('Обязательное поле')])
    text = TextAreaField('Текст публикации', validators=[])
    my_courses = MultiCheckboxField("На какие курсы опубликовать публикацию?", validators=[MultiCheckboxAtLeastOne()])
    files = FileField('Выберите файлы', validators=[Optional()], render_kw={"multiple": True})

    submit = SubmitField('Опубликовать')

    def __init__(self, user_uuid, *args, **kwargs):
        super(FormAddPublication, self).__init__(*args, **kwargs)
        self.my_courses.choices = [(values.get("uuid"), values.get("title")) for values in get_courses_teach(user_uuid)]
