from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,PasswordField
from wtforms.validators import InputRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Poster', validators=[InputRequired(), FileRequired(), FileAllowed(['jpg','jpeg', 'png', 'gif', 'tiff', 'ai', 'raw', 'eps', 'webp', 'avif', 'svg'], 'Images only')])
    register = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    login = SubmitField('Login')

class PostForm(FlaskForm):
    photo = StringField('Photo', validators=[InputRequired()])
    caption = TextAreaField('Caption', validators=[InputRequired()])
    submit = SubmitField('Submit')   