from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
# Ensure your imports are correctly referencing your project structure
from api.auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Register blueprints for modular routes, auth_bp contains our auth routes
app.register_blueprint(auth_bp, url_prefix='/auth')

# Import models after db initialization to avoid circular imports
from models.user import User

if __name__ == '__main__':
    with app.app_context():
        # This ensures tables are created within the app context
        db.create_all()
    app.run(debug=True)

