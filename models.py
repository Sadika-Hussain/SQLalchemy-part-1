"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Represents a user in the Blogly application.
    
    Attributes:
        id (int): The primary key for the user.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        image_url (str): The URL of the user's profile image.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                     nullable=False)
    
    last_name = db.Column(db.String(50),
                     nullable=False)
    
    image_url = db.Column(db.String)


    def get_full_name(self):
        """Returns the full name of the user."""
        return f'{self.first_name} {self.last_name}'
    
    def first(self):
        """Returns the first name of the user"""
        return f'{self.first_name}'
    
    def last(self):
        """Returns the last name of the user"""
        return f'{self.last_name}'

    def image(self):
        """Returns the image URL of the user"""
        return f'{self.image_url}'

    @classmethod
    def get_user_by_id(cls, id):
        """Fetches a user by their ID."""
        return cls.query.filter_by(id=id).first()

    

    

