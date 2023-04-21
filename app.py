from flask import Flask, session, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm

app = Flask(__name__)
app.app_context().push()

## TODO 
## Need to figure out how to configure app.app_context() correctly 
## So we don't have problems on Heroku


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bestseller'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "whoaasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def start_page():
    """redirect a user to the register page"""

    return render_template("startpage.html")


@app.route("/register", methods=['GET', 'POST'])
def register_user():
    """registration page for new user"""

    form = RegisterForm()

    if form.validate_on_submit():
        return "good job!"

    else:
        return render_template('register.html', form=form)
