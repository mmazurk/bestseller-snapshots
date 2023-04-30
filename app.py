from flask import Flask, session, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from api_secret import API_KEY
from booklist import List
import requests, pdb, json

key = API_KEY
API_BASE_URL = "https://api.nytimes.com/svc/books/v3/"

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
        email = form.email.data
        username = form.username.data
        password = User.register(username, form.password.data).password
        if(form.image_url.data): 
            image_url = form.image_url.data
        else:
            image_url = "https://images.unsplash.com/photo-1457140072488-87e5ffde2d77?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"
        if(form.bio.data):
            bio = form.bio.data
        else:
            bio = "Bio goes here."
        user = User(email = email, username = username, password = password, image_url = image_url, bio = bio)
        db.session.add(user)
        db.session.commit()
        return redirect("/")

    else:
        return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_user():
    """login existing user"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if(User.authenticate(username, password)):
            return render_template("user-landing.html")
        else:
            flash("Incorrect username or password")
            return render_template("login.html", form = form)
    
    else:
        return render_template("login.html", form = form)

@app.route("/list-search")
def search_lists():
    """search through book lists"""

    #TODO: Finish writing booklist.py and then pass the results to the page
    booklist = List()

    return render_template("list-search.html", booklist=booklist)

@app.route("/book-results/<list_name_encoded>")
def show_list(list_name_encoded):
    """search through book lists"""

    ##TODO add the logic for showing the book lists

    return render_template("book-results.html")
