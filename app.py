from flask import Flask, session, redirect, render_template, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, NYTList, Book, UserBooks, UserLists
from forms import RegisterForm, LoginForm
from booklist import List
import requests
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("NYT_API_KEY")
API_BASE_URL = "https://api.nytimes.com/svc/books/v3/"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "whoaasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    # db.drop_all()
    db.create_all()

# object to store API call so we don't make it multiple times
booklist = List()


@app.route("/")
def start_page():
    """redirect a user to the register page"""

    username = session.get('username')

    if (username):
        session.pop('username')
        session.pop('user_id')

    return render_template("startpage.html")


@app.route("/logout")
def logout_user():
    """log a user out and return to the start page"""

    session.pop('user_id')
    session.pop('username')
    return redirect('/')


@app.route("/register", methods=['GET', 'POST'])
def register_user():
    """registration page for new user"""

    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = User.register(username, form.password.data).password
        if (form.image_url.data):
            image_url = form.image_url.data
        else:
            image_url = "https://images.unsplash.com/photo-1457140072488-87e5ffde2d77?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"
        if (form.bio.data):
            bio = form.bio.data
        else:
            bio = "Bio goes here."
        user = User(email=email, username=username,
                    password=password, image_url=image_url, bio=bio)
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
        user = User.authenticate(username, password)
        if (user):
            session['user_id'] = user.user_id
            session['username'] = username
            return redirect(f"/user-landing/{username}")
        else:
            flash("Incorrect username or password")
            return render_template("login.html", form=form)

    else:
        return render_template("login.html", form=form)


@app.route("/user-landing")
def redirect_to_page():
    """redirects user to home page"""

    username = session.get('username')
    return redirect(f"/user-landing/{username}")


@app.route("/user-landing/<username>")
def show_user_page(username):
    """Users home page"""

    if not username == session.get('username'):
        return redirect("/")

    user_id = session.get('user_id')

    list_result = db.session.query(NYTList.list_name, NYTList.list_name_encoded).join(
        UserLists, NYTList.list_id == UserLists.list_id, isouter=True).filter(UserLists.user_id == user_id).all()

    if (list_result):
        favorited_lists = [(item[0], item[1]) for item in list_result]
    else:
        favorited_lists = []

    book_result = db.session.query(Book.title, Book.author, Book.description, Book.image_url, Book.book_id).join(
        UserBooks, Book.book_id == UserBooks.book_id, isouter=True).filter(UserBooks.user_id == user_id).all()

    if (book_result):
        favorited_books = book_result
    else:
        favorited_books = []

    user = User.query.get(user_id)

    return render_template("user-landing.html", user=user, username=username, favorited_lists=favorited_lists, favorited_books=favorited_books)


@app.route("/list-search")
def search_lists():
    """search through book lists"""

    user_id = session.get('user_id')

    result = db.session.query(NYTList.list_name_encoded).join(
        UserLists, NYTList.list_id == UserLists.list_id, isouter=True).filter(UserLists.user_id == user_id).all()

    if (result):
        list_of_favorites = [item[0] for item in result]
    else:
        list_of_favorites = []

    # booklist is from an object I created at the top
    return render_template("list-search.html", booklist=booklist, list_of_favorites=list_of_favorites)


@app.route("/book-results")
def show_list():
    """search through book lists"""

    list_name_encoded = request.args.get('list_name_encoded')
    date = request.args.get('date')

    res = requests.get(
        f"{API_BASE_URL}lists/{date}/{list_name_encoded}.json", params={'api-key': key})
    data = res.json()
    display_name = data['results']['display_name']
    list_name_encoded = data['results']['list_name_encoded']
    published_date = data['results']['published_date']
    books = data['results']['books']

    # now see which books the user has already favorited

    user_id = session.get('user_id')
    book_result = db.session.query(Book.isbns_combined, Book.title, Book.author, Book.description, Book.image_url, Book.book_id).join(
        UserBooks, Book.book_id == UserBooks.book_id, isouter=True).filter(UserBooks.user_id == user_id).all()

    if (book_result):
        favorited_books = book_result
    else:
        favorited_books = []

    favorite_list = [item[0] for item in favorited_books]

    return render_template("book-results.html", display_name=display_name, list_name_encoded=list_name_encoded, published_date=published_date, books=books, favorite_list=favorite_list)


@app.route("/list-search/add/<list_name_encoded>")
def add_list(list_name_encoded):
    """Saves list to user profile"""

    username = session.get('username')
    list_object = next(
        (obj for obj in booklist.data if obj['list_name_encoded'] == list_name_encoded), None)

    # Check and see if this list is already favorited
    current_list = NYTList.query.filter(
        NYTList.list_name_encoded == list_name_encoded).first()
    user = User.query.filter(User.username == username).first()

    if not (current_list):
        new_list = NYTList(list_name=list_object['list_name'], list_name_encoded=list_object['list_name_encoded'],
                           oldest_published_date=list_object['oldest_published_date'], newest_published_date=list_object['newest_published_date'])
        db.session.add(new_list)
        db.session.commit()

    user_id = session.get('user_id')
    list_id = NYTList.query.filter(
        NYTList.list_name_encoded == list_name_encoded).first().list_id
    entry = UserLists(user_id=user_id, list_id=list_id)
    db.session.add(entry)
    db.session.commit()
    return redirect(f"/list-search")


@app.route("/book-results/add")
def add_book():
    """Saves book to user profile"""

    list_name_encoded = request.args.get('list_name_encoded')
    isbns_combined = request.args.get('isbns_combined')
    book_title = request.args.get('title')
    author = request.args.get('author')
    description = request.args.get('description')
    image_url = request.args.get('image_url')

    if not (list_name_encoded and book_title):
        return render_template("secret.html")

    # Is this book in the database; if not, add
    book = Book.query.filter(Book.isbns_combined == isbns_combined).first()
    if not (book):
        new_book = Book(isbns_combined=isbns_combined, title=book_title,
                        author=author, description=description, image_url=image_url)
        db.session.add(new_book)
        db.session.commit()

    user_id = session.get('user_id')
    book_id = Book.query.filter(
        Book.isbns_combined == isbns_combined).first().book_id
    entry = UserBooks(user_id=user_id, book_id=book_id)
    db.session.add(entry)
    db.session.commit()

    return redirect(f"/book-results?list_name_encoded={list_name_encoded}")


@app.route("/list-search/remove")
def remove_list():
    """removes a list from the user"""

    username = session.get('username')
    user_id = session.get('user_id')
    list_name_encoded = request.args.get('list_name_encoded')
    origin = request.args.get('origin')

    if (list_name_encoded):
        list_id = NYTList.query.filter(
            NYTList.list_name_encoded == list_name_encoded).first().list_id
        UserLists.query.filter(UserLists.user_id == user_id).filter(
            UserLists.list_id == list_id).delete()
        db.session.commit()

        if (origin == "landing"):
            return redirect(f"/user-landing/{username}")
        if (origin == "lists"):
            return redirect("/list-search")
    else:
        return render_template("secret.html")


@app.route("/book-search/remove")
def remove_book():
    """ removes a book from the user"""

    username = session.get('username')
    user_id = session.get('user_id')
    book_id = request.args.get('book_id')

    if (book_id):
        UserBooks.query.filter(UserBooks.user_id == user_id).filter(
            UserBooks.book_id == book_id).delete()
        db.session.commit()
        return redirect(f"/user-landing/{username}")
    else:
        return render_template("secret.html")

# ZaK: In production you typically wouldn't make a ton of API calls;
# You would use a cache server for the API data; a service like redis
# It will call the API when you are beyond the limit
