# backend/models/user.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from email_validator import validate_email, EmailNotValidError


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """Represents a user in the system."""
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user') # Roles: 'user' or 'admin'

    bookings = db.relationship('Booking', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_username(username):
        """Validates the username format."""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long."
        return True, ""
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }

    def __repr__(self):
        return f'<User {self.username}>'

