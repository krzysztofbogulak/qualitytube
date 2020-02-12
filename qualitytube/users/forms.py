from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from qualitytube.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Użytkownik',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Powtórz hasło',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Stwórz konto')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ten użytkownik już istnieje w bazie')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten adres email już istnieje w bazie')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj dane')
    submit = SubmitField('Zaloguj')


class UpdateAccountForm(FlaskForm):
    username = StringField('Użytkownik',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Aktualizuj zdjęcie', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Aktualizuj')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Ten użytkownik już istnieje w bazie')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ten adres email już istnieje w bazie')
