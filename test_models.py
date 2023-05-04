# FLASK_ENV=production python -m unittest test_models.py

import os
from unittest import TestCase
from models import db, connect_db, User, NYTList, Book, UserBooks, UserLists
from app import app

os.environ['DATABASE_URL'] = "postgresql:///bestseller-test"

with app.app_context():
    db.drop_all()
    db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

    def tearDown(self):
        """tear down"""

        with app.app_context():
            User.query.delete()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="this_is_an_image_url",
            bio="I am a test user hooray."
        )

        with app.app_context():
            db.session.add(u)
            db.session.commit()
            res = User.query.get(1)

        self.assertEqual(len(res.bio), 24)
        self.assertEqual(res.email, "test@test.com")
