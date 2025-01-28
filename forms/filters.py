from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, DateField, EmailField, \
    PasswordField, URLField, TimeField, RadioField, BooleanField, SelectMultipleField, SelectField, FileField
from wtforms.validators import InputRequired, DataRequired, ValidationError, \
    Length, Regexp
from wtforms.widgets import CheckboxInput
import re

class TaskFilter(FlaskForm):


