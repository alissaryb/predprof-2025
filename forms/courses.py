from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField, widgets, URLField
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import InputRequired, DataRequired, Optional, StopValidation, ValidationError
from flask_wtf.file import FileAllowed, FileRequired

from py_scripts.funcs_back import get_title_courses_by_user_uuid, get_courses_teach


SUBJECTS = ['Информатика', 'Фронтенд', 'Бэкенд', 'Анализ данных', 'DevOps', 'Программирование',
            'Промышленная разработка', 'Искусственный интеллект']


class FormAddCourse(FlaskForm):
    title = StringField('Введите название курса', validators=[InputRequired('Обязательное поле')])
    description = TextAreaField('Введите описание курса', validators=[InputRequired('Обязательное поле')])
    video_url = TextAreaField('Введите код вставки видео (ВК Видео, Rutube, YouTube)',
                              validators=[InputRequired('Обязательное поле')])
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


class FormAddLesson(FlaskForm):
    title = StringField('Тема', validators=[InputRequired('Обязательное поле')])
    description = StringField('Напишите краткое описание урока', validators=[InputRequired('Обязательное поле')])
    tag = StringField('Напишите ключевые слова через запятую', validators=[InputRequired('Обязательное поле')])
    lesson_file = FileField('Прикрепите файл с конспектом формата MarkdownV2',
                            validators=[FileRequired('Обязательное поле'), FileAllowed(['md'])])
    files = FileField('Прикрепите материалы у уроку', validators=[Optional()], render_kw={"multiple": True})
    my_courses = MultiCheckboxField("На какие курсы опубликовать урок?", validators=[MultiCheckboxAtLeastOne()])

    submit = SubmitField('Опубликовать')

    def __init__(self, user_uuid, *args, **kwargs):
        super(FormAddLesson, self).__init__(*args, **kwargs)
        self.my_courses.choices = [(values.get("uuid"), values.get("title")) for values in get_courses_teach(user_uuid)]
