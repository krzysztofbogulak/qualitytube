from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import (DataRequired, ValidationError)
import re


class PostForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    description = TextAreaField('Opis', validators=[DataRequired()])

    def isYoutube(form, field):
        yt_regexp =(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        if not re.match(yt_regexp, field.data):
            raise ValidationError('Podany link jest nieprawidłowy')

    video = TextAreaField('Wideo link', validators=[isYoutube])
    submit = SubmitField('Dodaj')
