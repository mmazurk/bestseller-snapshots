from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """form for user to register"""

    email = StringField('Enter your email', validators=[InputRequired()])
    username = StringField('Enter a short username', validators=[InputRequired()])
    password = PasswordField('Enter Password', validators=[InputRequired()])
    image_url = StringField('Image URL', validators=[InputRequired()])
    bio = StringField('Short Bio', validators=[InputRequired()])
