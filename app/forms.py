from wtforms import StringField, SubmitField, BooleanField, ValidationError, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from .models import User


class LoginForm(FlaskForm):
    username = StringField('Login', validators=(DataRequired(),))
    password = PasswordField('Password', validators=(DataRequired(),))
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Login', validators=(DataRequired(),))
    email = StringField('Email', validators=(DataRequired(), Email()))
    password = PasswordField('Password', validators=(DataRequired(),))
    repeat_password = PasswordField('Repeat password', validators=(DataRequired(), EqualTo('password')))
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Please use a different email')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password is too short')
        if len(password.data) > 30:
            raise ValidationError('Password is too long')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=(DataRequired(),))
    about_me = TextAreaField('About me', validators=(Length(min=0, max=140),))
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if self.original_username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(f'{username.data} is already taken. Please use a different username')

