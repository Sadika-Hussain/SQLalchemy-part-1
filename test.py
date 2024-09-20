import unittest
from flask import Flask
from models import db, User
from app import app  

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'  # Use a test database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(unittest.TestCase):
    def setUp(self):
        """Add test user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User", image_url = 'https://example.com/image.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def teardown(self):
        db.session.rollback()

    def test_home_redirect(self):
        """Test the home route redirects to /users."""
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)  # Check for redirect
            self.assertEqual(response.location, 'http://localhost/users')  # Check redirect location

    def test_list_users(self):
        """Test the list of users page."""
        with app.test_client() as client:
            response = client.get('/users')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)  # Check if the sample user is displayed


    def test_add_user(self):
        """Test adding a new user."""
        with app.test_client() as client:
            response = client.post('/users/new', data={
                'firstname': 'New',
                'lastname': 'User',
                'url': 'http://example.com/newuser.jpg'
            })
            self.assertEqual(response.status_code, 302)  # Check for redirect
            self.assertEqual(User.query.count(), 2)  # Check user count

    def test_user_detail(self):
        """Test user detail page."""
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test User', response.data)  # Check if user details are displayed

    def test_edit_user(self):
        """Test editing a user."""
        with app.test_client() as client:
            response = client.post(f'/users/{self.user_id}/edit', data={
                'firstname': 'Updated',
                'lastname': 'User',
                'url': 'http://example.com/updateduser.jpg'
            })
            self.assertEqual(response.status_code, 302)  # Check for redirect
            updated_user = User.query.get(self.user_id)
            self.assertEqual(updated_user.first_name, 'Updated')  # Check if user details were updated

    def test_delete_user(self):
        """Test deleting a user."""
        with app.test_client() as client:
            response = client.post(f'/users/{self.user_id}/delete')
            self.assertEqual(response.status_code, 302)  # Check for redirect
            self.assertIsNone(User.query.get(self.user_id))  # Check if user is deleted