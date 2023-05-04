# FLASK_ENV=production python -m unittest test_models.py

import os
from unittest import TestCase
from models import db, connect_db, User, NYTList, Book, UserBooks, UserLists
from app import app

os.environ['DATABASE_URL'] = "postgresql:///bestseller-test"
app.config['WTF_CSRF_ENABLED'] = False

with app.app_context():
    db.drop_all()
    db.create_all()

class UserPagesTestCase(TestCase):
    """Tests out the page responses."""

    def setUp(self):
        """Create a test user."""

        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        with self.app_context:
            db.drop_all()
            db.create_all()

            self.testuser = User(username="usertest",
                                email="usertest@test.com",
                                password="testuser",
                                image_url=None,
                                bio=None)
            self.testuser_id = 7777
            self.testuser.user_id = self.testuser_id

            db.session.add(self.testuser)
            db.session.commit()

    def tearDown(self):
        """Clean up any resources created during the test."""

        with self.app_context:
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_landing(self):
        """Can we see the home page?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.user_id
                sess['username'] = self.testuser.username

            resp = c.get("/user-landing/usertest")
            html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('My Saved Lists', html)
 
    def test_list_search(self):
        """Can we see the lists page?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.testuser.user_id
                sess['username'] = self.testuser.username
    
            resp = c.get("/list-search")
            html = resp.get_data(as_text = True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Fiction', html)
        self.assertIn('List Search', html)


    #     resp = c.get("/book-results/combined-print-and-e-book-fiction")
    #     html = resp.get_data(as_text = True)

    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('The books on your list are shown below.', html)
    #     self.assertIn('Add Book', html)

    #     resp = c.get("/book-results/add", query_string={list_name_encoded = "combined-print-and-e-book-fiction", isbns_combined = "2352352323523"})
    #     html = resp.get_data(as_text = True)
