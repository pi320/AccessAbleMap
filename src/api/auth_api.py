# contain the routes for handling user authentication, including 
#       -   user registration, 
#       -   login, and 
#       -   password encryption
from flask import Blueprint, request, jsonify
from models.user import User
from app import db  # This should be replaced with actual import from your database module

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = AuthService.create_user(email=data['email'], password=data['password'])
        return jsonify(user.to_dict()), 201  # Respond with the new user's data, excluding the password hash
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # # Ensure the email is not already in use
    # if User.query.filter_by(email=email).first() is not None:
    #     return jsonify({'error': 'Email already in use'}), 400

    # new_user = User(email=email)
    # new_user.set_password(password)

    # db.session.add(new_user)
    # db.session.commit()

    # return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = AuthService.verify_user(email=data['email'], password=data['password'])
    if user:
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401