from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """This sets up a connection between a Flask application and a database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """This class represents a user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(300))
    bio = db.Column(db.String(200))

    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

    def __repr__(self):
        """Show info about object"""
        u = self
        return f"<User id={u.user_id}, username={u.username}"


class Note(db.Model):

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


class NYT_List(db.Model):

    __tablename__ = "nyt_lists"

    # in the API this is also called list_id
    list_id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(30), nullable=False)
    oldest_published_date = db.Column(db.Date)
    newest_published_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))


class Book(db.Model):

    __tablename__ = "books"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    isbn_10 = db.Column(db.String(10))
    isbn_13 = db.Column(db.String(13))
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.String(200))
    review_url = db.Column(db.String(200))
    amazon_url = db.Column(db.String(200))
    description = db.Column(db.Text)
    publisher = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


class User_List(db.Model):

    __tablename__ = "user_lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_name = db.Column(db.String(30), nullable=False)
    list_description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
