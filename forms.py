from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """form for user to register"""

    # TODO: need to use an email validator for this
    email = StringField('Enter your email', validators=[InputRequired()])
    username = StringField('Enter a short username', validators=[InputRequired()])
    password = PasswordField('Enter Password', validators=[InputRequired()])
    image_url = StringField('Image URL')
    bio = StringField('Short Bio')

class LoginForm(FlaskForm):
    """form to log in to the site"""

    username = StringField('Enter a short username', validators=[InputRequired()])
    password = PasswordField('Enter Password', validators=[InputRequired()])

class UserList(FlaskForm):
    """form for users to enter """

    list_name = StringField('Enter a name for this list', validators=[InputRequired()])
    list_description = TextAreaField('Notes about this list') 

class BookNotes(FlaskForm):
    """form for users to enter book notes""" 

    note_content = TextAreaField('Notes about this book', validators=[InputRequired()])

