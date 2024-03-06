from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db 

class AuthService:
    @staticmethod
    def create_user(email, password):
        # Check if user already exists
        if User.query.filter_by(user_email=email).first():
            raise ValueError('User already exists with that email.')

        # Create new user instance
        new_user = User(user_email=email)
        new_user.set_password(password)  # Hash password before storing

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def verify_user(email, password):
        # Retrieve user by email
        user = User.query.filter_by(user_email=email).first()

        # Check provided password against stored hash
        if user and user.check_password(password):
            return user

        return None  # Return None if user doesn't exist or password doesn't match

# Example usage within your Flask route
# from services.auth_service import AuthService

# @route('/login', methods=['POST'])
# def login():
#     # Assume data has 'email' and 'password' keys
#     user = AuthService.verify_user(data['email'], data['password'])
#     if user:
#         # Login successful - handle session/token creation here
#     else:
#         # Login failed - return appropriate response
